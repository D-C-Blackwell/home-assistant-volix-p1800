"""Binary sensors for VOLIX P1800."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from . import VolixConfigEntry
from .entity import VolixEntity


async def async_setup_entry(hass, entry: VolixConfigEntry, async_add_entities) -> None:
    async_add_entities((PowerFlowSensor(entry, "charging", True), PowerFlowSensor(entry, "discharging", False)))


class PowerFlowSensor(VolixEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER

    def __init__(self, entry, key: str, input_flow: bool):
        super().__init__(entry)
        self._attr_translation_key = key
        self.input_flow = input_flow
        self.unique(key)

    @property
    def is_on(self):
        status = self.coordinator.client.status if self.coordinator.client else None
        if not status:
            return None
        return (status.input_power if self.input_flow else status.output_power) > 0
