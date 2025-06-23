import requests, logging
import time
import json
import hashlib

# In-memory token cache
_token_cache = {}

def _generate_cache_key(tenant_id, client_id, secret, scope):
    key_string = f"{tenant_id}:{client_id}:{secret}:{scope}"
    return hashlib.sha256(key_string.encode()).hexdigest()

def get_bearer_token(
    tenant_id: str,
    client_id: str,
    client_secret: str,
    scope: str = "https://graph.microsoft.com/.default",  # default scope
    mode: str = "token"  # 'token', or 'raw'
) -> str:
    """
    Retrieves a bearer token from Microsoft identity platform using client credentials.
    Args:
        tenant_id (str): Azure AD tenant ID.
        client_id (str): Application (client) ID.
        client_secret (str): Client secret.
        scope (str): Scope for the token request.
        mode (str): Output mode - 'token' for just token, 'raw' for full response.
    Returns:
        str or dict: Token string or raw JSON response depending on mode.
    Raises:
        RuntimeError: If the token request fails, times out, or is malformed.
    """
    cache_key = _generate_cache_key(tenant_id, client_id, client_secret, scope)
    cached = _token_cache.get(cache_key)
    if cached and cached['expires_at'] > time.time():
        return cached['token']

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'grant_type': 'client_credentials'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(token_url, data=data, headers=headers, timeout=10)
        try:
            response_json = response.json()
        except ValueError:
            logging.critical("Non-JSON response received.")
            raise RuntimeError("Invalid JSON response received.")

        if response.status_code == 200:
            logging.info("Successfully obtained access token.")
            token = response_json.get('access_token')
            if not token:
                logging.critical("Token not found in the response.")
                raise RuntimeError("Token not found in the response.")
            expires_in = response_json.get('expires_in', 3599)
            _token_cache[cache_key] = {
                'token': f"{token}" if mode == "token" else response_json,
                'expires_at': time.time() + expires_in - 60
            }
            if mode == "token":
                return token
            elif mode == "raw":
                return response_json
            else:
                raise ValueError(f"Invalid mode '{mode}'. Use 'token', or 'raw'.")
        else:
            logging.critical(f"Token request failed: https status code {response.status_code} - {response_json}")
            raise RuntimeError(f"Token request failed, received https status code {response.status_code}\n{json.dumps(response_json, indent=4)}")

    except requests.exceptions.Timeout:
        logging.critical("Token request timed out.")
        raise RuntimeError("Token request timed out.")
