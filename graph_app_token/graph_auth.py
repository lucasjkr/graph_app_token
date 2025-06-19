import requests, json, logging

def get_bearer_token(tenant_id: str, client_id: str, secret: str, scope: str) -> str:
    """
    Retrieves a bearer token from Microsoft identity platform using client credentials.

    Args:
        tenant_id (str): Azure AD tenant ID.
        client_id (str): Application (client) ID.
        secret (str): Client secret.
        scope (str): Scope for the token request.

    Returns:
        str: Bearer token string.

    Raises:
        RuntimeError: If the token request fails or times out.
    """

    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'client_secret': secret,
        'scope': scope,
        'grant_type': 'client_credentials'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(token_url, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            token = response.json().get('access_token')
            return f'Bearer {token}'
        else:
            error_details = response.json()
            logging.critical(f"Failed to obtain token: {response.status_code} - {error_details}")
            raise RuntimeError(f"Token request failed with status {response.status_code}: {error_details}")
    except requests.exceptions.Timeout:
        logging.critical("Token request timed out.")
        raise RuntimeError("Token request timed out.")
