"""Sensor platform for Cuby Gas integration."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Cuby Gas sensor based on a config entry."""
    _LOGGER.debug("Setting up sensor platform")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([CubyGasSensor(coordinator, entry)])
    _LOGGER.debug("Sensor entity added")

class CubyGasSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Cuby Gas sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._device_id = entry.data.get("device_id")
        
        # Set unique ID
        self._attr_unique_id = f"cuby_gas_{self._device_id}"
        
        # Set name
        self._attr_name = f"LP Gas Level"
        
        # Set unit of measurement
        self._attr_unit_of_measurement = "%"
        
        # Set device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "Cuby Gas Tank",
            "manufacturer": "Cuby",
            "model": "Gas Tank Monitor",
        }

        _LOGGER.debug(f"Initialized sensor with device_id: {self._device_id}")

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            level = self.coordinator.data.get("level")
            _LOGGER.debug(f"Returning sensor value: {level}")
            return level
        return None


