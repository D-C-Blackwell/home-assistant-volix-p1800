"""Sensors for VOLIX P1800."""

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfTime

from . import VolixConfigEntry
from .entity import VolixEntity
from .protocol import StatusData


@dataclass(frozen=True, kw_only=True)
class VolixSensorDescription(SensorEntityDescription):
    value_fn: Callable[[StatusData], int]


SENSORS = (
    VolixSensorDescription(key="battery_level", translation_key="battery_level", native_unit_of_measurement=PERCENTAGE, device_class=SensorDeviceClass.BATTERY, state_class=SensorStateClass.MEASUREMENT, value_fn=lambda s: s.battery_level),
    VolixSensorDescription(key="input_power", translation_key="input_power", native_unit_of_measurement=UnitOfPower.WATT, device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, value_fn=lambda s: s.input_power),
    VolixSensorDescription(key="output_power", translation_key="output_power", native_unit_of_measurement=UnitOfPower.WATT, device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, value_fn=lambda s: s.output_power),
    VolixSensorDescription(key="remaining_time", translation_key="remaining_time", native_unit_of_measurement=UnitOfTime.MINUTES, device_class=SensorDeviceClass.DURATION, value_fn=lambda s: s.remaining_minutes),
)


async def async_setup_entry(hass, entry: VolixConfigEntry, async_add_entities) -> None:
    async_add_entities(VolixSensor(entry, description) for description in SENSORS)


class VolixSensor(VolixEntity, SensorEntity):
    entity_description: VolixSensorDescription

    def __init__(self, entry, description):
        super().__init__(entry)
        self.entity_description = description
        self.unique(description.key)

    @property
    def native_value(self):
        status = self.coordinator.client.status if self.coordinator.client else None
        return self.entity_description.value_fn(status) if status else None
