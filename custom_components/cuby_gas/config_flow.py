"""Config flow for Cuby Gas integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CubyApiClient
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_DEVICE_ID

_LOGGER = logging.getLogger(__name__)

class CubyGasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Cuby Gas."""

    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            device_id = user_input[CONF_DEVICE_ID]
            
            # Validate credentials by attempting to get a token
            session = async_get_clientsession(self.hass)
            client = CubyApiClient(username, password, session)
            
            try:
                _LOGGER.debug("Attempting to refresh token in config flow")
                await client._refresh_token()
                
                if client._token:
                    _LOGGER.debug("Token obtained successfully, testing device_id")
                    try:
                        gas_level = await client.get_gas_level(device_id)
                        _LOGGER.debug(f"Gas level API response: {gas_level}")
                    
                        if gas_level is not None:
                            _LOGGER.debug("Creating config entry")
                            return self.async_create_entry(
                                title=f"Cuby Gas ({device_id})",
                                data={
                                    CONF_USERNAME: username,
                                    CONF_PASSWORD: password,
                                    CONF_DEVICE_ID: device_id,
                                },
                            )
                        else:
                            _LOGGER.error(f"Invalid device ID: {device_id}")
                            errors["device_id"] = "invalid_device_id"
                    except Exception as ex:
                        _LOGGER.exception(f"Error getting gas level: {ex}")
                        errors["device_id"] = "cannot_connect"
                else:
                    _LOGGER.error("Authentication failed - no token received")
                    errors["base"] = "auth_failed"
            except Exception:
                _LOGGER.exception(f"Connection error during setup: {ex}")
                errors["base"] = "connection_error"
        
        # Show form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_DEVICE_ID): str,
                }
            ),
            errors=errors,
        )


