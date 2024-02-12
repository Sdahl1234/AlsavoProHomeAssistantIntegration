"""Alsavo Pro pool heat pump integration."""
from datetime import timedelta
import logging

import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .AlsavoPyCtrl import AlsavoPro
from .const import DOMAIN, SERIAL_NO

PLATFORMS = [
    Platform.CLIMATE,
    Platform.SENSOR,
]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config):  # noqa: D103
    """Async setup."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the Alsavo Pro heater."""
    name = entry.data.get(CONF_NAME)
    serial_no = entry.data.get(SERIAL_NO)
    ip_address = entry.data.get(CONF_IP_ADDRESS)
    port_no = entry.data.get(CONF_PORT)
    password = entry.data.get(CONF_PASSWORD)

    data_handler = AlsavoPro(name, serial_no, ip_address, port_no, password)
    await data_handler.update()
    data_coordinator = AlsavoProDataCoordinator(hass, data_handler)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN][entry.entry_id] = data_coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_update_entry))

    # for platform in ('sensor', 'climate'):
    #    hass.async_create_task(
    #        hass.config_entries.async_forward_entry_setup(entry, platform)
    #    )

    return True


async def async_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class AlsavoProDataCoordinator(DataUpdateCoordinator):
    """Coordinator."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, data_handler) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=DOMAIN,  # "AlsavoPro",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=15),
        )
        self.data_handler = data_handler

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.unique_id),
            },
            manufacturer="Swim & Fun",
            serial_number=self.config_entry.data.get(SERIAL_NO),  # "1234",
            # model=self.data_handler.devicetype,
            name=self.name,  # self.system["name"],
            sw_version=self.data_handler.sw_code,  # 404,  # self.system.get("softwareversion"),
            hw_version=self.data_handler.hw_code,
        )

    @property
    def unique_id(self) -> str:
        """Return the system descriptor."""
        entry = self.config_entry
        if entry.unique_id:
            return entry.unique_id
        assert entry.entry_id
        return entry.entry_id

    async def _async_update_data(self):
        _LOGGER.debug("_async_update_data")
        try:
            async with async_timeout.timeout(10):
                await self.data_handler.update()
                return self.data_handler
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.debug(f"_async_update_data timed out {ex}")  # noqa: G004
