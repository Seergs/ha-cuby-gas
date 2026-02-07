import asyncio
import logging
from datetime import timedelta

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import CubyApiClient
from .const import (
        DOMAIN,
        DEFAULT_SCAN_INTERVAL
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug(f"Setting up Cuby Gas integration for entry: {entry.entry_id}")
    hass.data.setdefault(DOMAIN, {})

    username = entry.data.get("username")
    password = entry.data.get("password")

    session = async_get_clientsession(hass)
    client = CubyApiClient(username, password, session)

    coordinator = CubyDataUpdateCoordinator(
            hass,
            client=client,
            device_id=entry.data.get("device_id")
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug(f"Cuby Gas integration setup complete for entry: {entry.entry_id}")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class CubyDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client, device_id):
        self.client = client
        self.device_id = device_id

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL)
        )

    async def _async_update_data(self):
        try:
            _LOGGER.debug(f"Updating data for device_id: {self.device_id}")
            gas_level = await self.client.get_gas_level(self.device_id)

            if gas_level is None:
                raise UpdateFailed("Failed to get gas level data")

            data = {"level": gas_level}
            _LOGGER.debug(f"Updated data: {data}")

            return data

        except Exception as err:
            _LOGGER.exception(f"Error communicating with API: {err}")
            raise UpdateFailed(f"Error communicating with API: {err}")

