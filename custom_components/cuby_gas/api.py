import logging
from datetime import datetime, timedelta
import aiohttp
import async_timeout

from .const import API_TOKEN_ENDPOINT, API_GAS_LEVEL_ENDPOINT

_LOGGER = logging.getLogger(__name__)

class CubyApiClient:
    def __init__(self, username, password, session):
        self._username = username
        self._password = password
        self._session = session
        self._token = None
        self._token_expires_at = None

    async def ensure_token_valid(self):
        now = datetime.now()

        if (not self._token or not self._token_expires_at or
            self._token_expires_at <= now + timedelta(minutes=10)):
            await self._refresh_token()

    async def _refresh_token(self):
        _LOGGER.debug("Refreshing Cuby API token")

        try:
            async with async_timeout.timeout(10):
                response = await self._session.post(
                        API_TOKEN_ENDPOINT,
                        json={"password": self._password})
                
                if response.status != 200:
                    _LOGGER.error("Failed to refresh token, status: %s, response: %s", response.status, await response.text())
                    return False
                
                data = await response.json()

                self._token = data.get("token")
                expiration = data.get("expiration")
                self._token_expires_at = datetime.now() + timedelta(seconds=expiration)

                _LOGGER.debug("Token refreshed successfully")
                return True
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Error refreshing token: %s", err)
            return False

    async def get_gas_level(self, device_id):
        await self.ensure_token_valid()

        if not self._token:
            _LOGGER.error("No valid token available")
            return None

        try:
            headers = {"Authorization": f"Bearer {self._token}"}

            async with async_timeout.timeout(10):
                response = await self._session.get(
                        f"{API_GAS_LEVEL_ENDPOINT}/{device_id}", headers=headers)

                if response.status != 200:
                    _LOGGER.error("Failed to get gas level, status: %s, response: %s", response.status, await response.text())
                    return None

                data = await response.json()

                return data.get("level")

        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Error getting gas level: %s", err)
            return None

