"""Sensor for AlsavPro."""

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant

from . import AlsavoProDataCoordinator
from .const import DOMAIN
from .entity import AlsavoProEntity


async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Entry setup."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Water In",
                "°C",
                16,
                False,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Water Out",
                "°C",
                17,
                False,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Ambient",
                "°C",
                18,
                False,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Cold pipe",
                "°C",
                19,
                False,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "heating pipe",
                "°C",
                20,
                False,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "IPM module",
                "°C",
                21,
                False,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Exhaust temperature",
                "°C",
                23,
                False,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Heating mode target",
                "°C",
                1,
                True,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Cooling mode target",
                "°C",
                2,
                True,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.TEMPERATURE,
                "Auto mode target",
                "°C",
                3,
                True,
                "mdi:thermometer",
            ),
            AlsavoProSensor(
                coordinator, None, "Fan speed", "RPM", 22, False, "mdi:fan"
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.CURRENT,
                "Compressor",
                "A",
                26,
                False,
                "mdi:current-ac",
            ),
            AlsavoProSensor(
                coordinator,
                SensorDeviceClass.FREQUENCY,
                "Compressor running frequency",
                "Hz",
                27,
                False,
                "mdi:air-conditioner",
            ),
            AlsavoProSensor(
                coordinator,
                None,
                "Frequency limit code",
                "",
                34,
                False,
                "mdi:bell-alert",
            ),
            AlsavoProSensor(
                coordinator, None, "Alarm code 1", "", 48, False, "mdi:bell-alert"
            ),
            AlsavoProSensor(
                coordinator, None, "Alarm code 2", "", 49, False, "mdi:bell-alert"
            ),
            AlsavoProSensor(
                coordinator, None, "Alarm code 3", "", 50, False, "mdi:bell-alert"
            ),
            AlsavoProSensor(
                coordinator, None, "Alarm code 4", "", 51, False, "mdi:bell-alert"
            ),
            AlsavoProSensor(
                coordinator,
                None,
                "System status code",
                "",
                52,
                False,
                "mdi:state-machine",
            ),
            AlsavoProSensor(
                coordinator,
                None,
                "System running code",
                "",
                53,
                False,
                "mdi:state-machine",
            ),
            AlsavoProSensor(
                coordinator, None, "Device type", "", 64, False, "mdi:heat-pump"
            ),
            AlsavoProSensor(
                coordinator,
                None,
                "Main board HW revision",
                "",
                65,
                False,
                "mdi:heat-pump",
            ),
            AlsavoProSensor(
                coordinator,
                None,
                "Main board SW revision",
                "",
                66,
                False,
                "mdi:heat-pump",
            ),
            AlsavoProSensor(
                coordinator, None, "Manual HW code", "", 67, False, "mdi:heat-pump"
            ),
            AlsavoProSensor(
                coordinator, None, "Manual SW code", "", 68, False, "mdi:heat-pump"
            ),
            AlsavoProSensorPowerMode(
                coordinator,
                SensorDeviceClass.ENUM,
                "Power mode",
                "",
                16,
                True,
                "mdi:heat-pump",
            ),
            AlsavoProSensorPowerMode(
                coordinator,
                SensorDeviceClass.ENUM,
                "Running mode",
                "",
                4,
                True,
                "mdi:heat-pump",
            ),
            AlsavoProSensorOperatingMode(
                coordinator,
                SensorDeviceClass.ENUM,
                "Operating mode",
                "",
                4,
                True,
                "mdi:heat-pump",
            ),
            AlsavoProErrorSensor(coordinator, "Error messages"),
        ]
    )


class AlsavoProSensorOperatingMode(AlsavoProEntity, SensorEntity):
    """Alsavo op sensor."""

    def __init__(
        self,
        coordinator: AlsavoProDataCoordinator,
        device_class: SensorDeviceClass,
        name: str,
        unit: str,
        idx: int,
        from_config: bool,
        icon: str,
    ) -> None:
        """Init."""
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._data_handler = self.data_coordinator.data_handler
        self._name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._dataIdx = idx
        self._config = from_config
        self._icon = icon

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
        # return f"{DOMAIN}_{self._data_handler.name}_{self._name}"

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will reflect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._data_handler.is_online

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._data_handler.unique_id}_{self._name}"

    @property
    def native_value(self):
        """Returning native."""
        # Hent data fra data_handler her
        if self._config:
            val = self._data_handler.get_config_value(self._dataIdx) & 3
            if self._dataIdx == 4:
                if val & 2 == 2:
                    return "Auto"
                if val & 1 == 1:
                    return "Opvarmning"
                if val & 0 == 0:
                    return "Køling"
            return val  # self._data_handler.get_config_value(self._dataIdx)
        return self._data_handler.get_status_value(self._dataIdx)

    @property
    def icon(self):
        """Icon."""
        return self._icon

    @property
    def options(self):
        """Options."""
        return ["Auto", "Køling", "Opvarmning"]


class AlsavoProSensorPowerMode(AlsavoProEntity, SensorEntity):
    """Sensor PM."""

    def __init__(
        self,
        coordinator: AlsavoProDataCoordinator,
        device_class: SensorDeviceClass,
        name: str,
        unit: str,
        idx: int,
        from_config: bool,
        icon: str,
    ) -> None:
        """Init."""
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._data_handler = self.data_coordinator.data_handler
        self._name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._dataIdx = idx
        self._config = from_config
        self._icon = icon

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
        # return f"{DOMAIN}_{self._data_handler.name}_{self._name}"

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will reflect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._data_handler.is_online

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._data_handler.unique_id}_{self._name}"

    @property
    def native_value(self):
        """Hent data fra data_handler her."""
        if self._config:
            val = self._data_handler.get_config_value(self._dataIdx)
            if self._dataIdx == 16:
                if val == 0:
                    return "Stille"
                if val == 1:
                    return "Smart"
                if val == 2:
                    return "Max"
            if self._dataIdx == 4:
                if val & 32 == 32:
                    return "Tændt"
                if val & 32 == 0:
                    return "Slukket"
            return val  # self._data_handler.get_config_value(self._dataIdx)
        return self._data_handler.get_status_value(self._dataIdx)

    @property
    def icon(self):
        """Icon."""
        return self._icon

    @property
    def options(self):
        """Options."""
        return ["Stille", "Smart", "Max", "Opvarmning", "Tændt", "Slukket"]


class AlsavoProSensor(AlsavoProEntity, SensorEntity):
    """AlsavoPro sensor."""

    def __init__(
        self,
        coordinator: AlsavoProDataCoordinator,
        device_class: SensorDeviceClass,
        name: str,
        unit: str,
        idx: int,
        from_config: bool,
        icon: str,
    ) -> None:
        """Init."""
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._data_handler = self.data_coordinator.data_handler
        self._name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._dataIdx = idx
        self._config = from_config
        self._icon = icon

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
        # return f"{DOMAIN}_{self._data_handler.name}_{self._name}"

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will reflect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._data_handler.is_online

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._data_handler.unique_id}_{self._name}"

    @property
    def native_value(self):
        """Hent data fra data_handler her."""
        if self._attr_device_class == SensorDeviceClass.TEMPERATURE:
            if self._config:
                return self._data_handler.get_temperature_from_config(self._dataIdx)
            return self._data_handler.get_temperature_from_status(self._dataIdx)
        if self._config:
            return self._data_handler.get_config_value(self._dataIdx)

        return self._data_handler.get_status_value(self._dataIdx)

    @property
    def icon(self):
        """Icon."""
        return self._icon


class AlsavoProErrorSensor(AlsavoProEntity, SensorEntity):
    """Alsavo error sensor."""

    def __init__(self, coordinator: AlsavoProDataCoordinator, name: str) -> None:
        """Init."""
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._data_handler = self.data_coordinator.data_handler
        self._name = name
        self._icon = "mdi:alert"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
        # return f"{DOMAIN}_{self._data_handler.name}_{self._name}"

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._data_handler.unique_id}_{self._name}"

    @property
    def native_value(self):
        """Native value."""
        return self._data_handler.errors

    @property
    def icon(self):
        """Icon."""
        return self._icon

    async def async_update(self):
        """Get the latest data."""
        self._data_handler = self.data_coordinator.data_handler
