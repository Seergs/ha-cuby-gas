DOMAIN = "cuby_gas"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_DEVICE_ID = "device_id"
DEFAULT_SCAN_INTERVAL = 300
API_BASE_URL = "https://cuby.cloud/api/v2"

def get_token_endpoint(email: str) -> str:
    """Get the token endpoint URL for a specific email."""
    return f"{API_BASE_URL}/token/{email}"

def get_gas_level_endpoint() -> str:
    """Get the gas level endpoint URL."""
    return f"{API_BASE_URL}/history/gas/level"
