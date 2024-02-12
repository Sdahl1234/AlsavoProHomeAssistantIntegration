"""Base alsavopro entity."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AlsavoProDataCoordinator


class AlsavoProEntity(CoordinatorEntity[AlsavoProDataCoordinator]):
    """Base AlsavoPro entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: AlsavoProDataCoordinator,
    ) -> None:
        """Initialize light."""
        super().__init__(coordinator)
        self._attr_device_info = coordinator.device_info
