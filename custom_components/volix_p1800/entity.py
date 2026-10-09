"""Shared VOLIX entity base."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import VolixConfigEntry
from .const import DOMAIN


class VolixEntity(CoordinatorEntity):
    """Base entity tied to a VOLIX config entry."""

    _attr_has_entity_name = True

    def __init__(self, entry: VolixConfigEntry) -> None:
        super().__init__(entry.runtime_data)
        self.entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            name=entry.title,
            manufacturer="VOLIX / ALLPOWERS",
            model="P1800",
        )

    def unique(self, suffix: str) -> None:
        self._attr_unique_id = f"{self.entry.unique_id}_{suffix}"
