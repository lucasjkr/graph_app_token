import requests, logging

def get_bearer_token(
    tenant_id: str,
    client_id: str,
    client_secret: str,
    scope: str = "https://graph.microsoft.com/.default", # default scope
    mode: str = "bearer"  # 'bearer', 'token', or 'raw'
) -> str | dict:
    """
    Retrieves a bearer token from Microsoft identity platform using client credentials.

    Args:
        tenant_id (str): Azure AD tenant ID.
        client_id (str): Application (client) ID.
        client_secret (str): Client secret.
        scope (str): Scope for the token request.
        mode (str): Output mode - 'bearer' for "Bearer {token}", 'token' for just token, 'raw' for full response.

    Returns:
        str | dict: Token string or raw JSON response depending on mode.

    Raises:
        RuntimeError: If the token request fails, times out, or is malformed.
    """
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'grant_type': 'client_credentials'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

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

            if mode == "bearer":
                return f"Bearer {token}"
            elif mode == "token":
                return token
            elif mode == "raw":
                return response_json
            else:
                raise ValueError(f"Invalid mode '{mode}'. Use 'bearer', 'token', or 'raw'.")
        else:
            logging.critical(f"Token request failed: {response.status_code} - {response_json}")
            raise RuntimeError(f"Token request failed: {response.status_code} - {response_json}")

    except requests.exceptions.Timeout:
        logging.critical("Token request timed out.")
        raise RuntimeError("Token request timed out.")