import os
import json
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import requests
from src.logger import logger

load_dotenv()


def load_service_routes() -> Dict[str, Any]:
    """Load service routes dynamically from the SERVICE_ROUTES_JSON environment variable."""
    routes_env = os.getenv("SERVICE_ROUTES_JSON", "{}")

    try:
        routes = json.loads(routes_env)
        if not isinstance(routes, dict):
            raise ValueError("SERVICE_ROUTES_JSON must be a valid JSON object")

        logger.debug(f"Loaded service routes: {routes}")
        return routes
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse SERVICE_ROUTES_JSON: {e}")
        return {}


def get_env_var(name: str, default="", required: bool = False) -> Optional[str]:
    """Retrieve an environment variable and optionally raise an error if missing."""
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_env_list(name: str, default: str = "") -> List[str]:
    """Retrieve an environment variable as a list, splitting by commas."""
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


def fetch_openid_configuration(issuer: str) -> Dict[str, Any]:
    url = f"{issuer}/.well-known/openid-configuration"
    logger.info(f"Fetching OpenID configuration from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        config = response.json()
        logger.info("Successfully fetched OpenID configuration.")
        return config
    except Exception as e:
        logger.error(f"Error fetching OpenID configuration: {e}")
        raise


SERVICE_ROUTES = load_service_routes()

KEYCLOAK_ISSUER = get_env_var("KEYCLOAK_ISSUER", required=True)
openid_config = fetch_openid_configuration(KEYCLOAK_ISSUER)

KEYCLOAK_JWKS_URL = openid_config.get("jwks_uri")
KEYCLOAK_LOGIN_URL = openid_config.get("authorization_endpoint")
KEYCLOAK_LOGOUT_URL = openid_config.get("end_session_endpoint")
KEYCLOAK_TOKEN_URL = openid_config.get("token_endpoint")
KEYCLOAK_INTROSPECT_URL = openid_config.get("introspection_endpoint")
KEYCLOAK_USERINFO_URL = openid_config.get("userinfo_endpoint")

KEYCLOAK_CLIENT_ID = get_env_var("KEYCLOAK_CLIENT_ID", required=True)
KEYCLOAK_CLIENT_SECRET = get_env_var("KEYCLOAK_CLIENT_SECRET", required=True)
REDIRECT_URL = get_env_var("REDIRECT_URL", required=True)
KEYCLOAK_SCOPE = get_env_var("KEYCLOAK_SCOPE", required=True)
FRONTEND_URL = get_env_var("FRONTEND_URL", required=True)

TIMEOUT = get_env_var("TIMEOUT", 300, required=False)
ALLOW_METHODS = get_env_list("ALLOW_METHODS", "GET,POST,PUT,DELETE,OPTIONS")
ALLOW_HEADERS = get_env_list("ALLOW_HEADERS", "Authorization,Content-Type")

logger.info("Keycloak configuration loaded successfully.")
logger.info(f"Authorization URL: {KEYCLOAK_LOGIN_URL}")
logger.info(f"Token URL: {KEYCLOAK_TOKEN_URL}")
logger.info(f"JWKS URL: {KEYCLOAK_JWKS_URL}")
logger.info(f"Logout URL: {KEYCLOAK_LOGOUT_URL}")
logger.info(f"Introspection URL: {KEYCLOAK_INTROSPECT_URL}")
logger.info(f"Userinfo URL: {KEYCLOAK_USERINFO_URL}")
logger.info(f"Allowed methods: {ALLOW_METHODS}")
logger.info(f"Allowed headers: {ALLOW_HEADERS}")