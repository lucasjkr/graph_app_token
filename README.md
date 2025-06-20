# graph_app_token

A lightweight Python package to retrieve Microsoft Graph API bearer tokens using client credentials.

## Installation

You can install this package directly from GitHub using pip:

```bash pip install git+https://github.com/lucasjkr/graph_app_token.git```

## Usage

    from graph_app_token import get_bearer_token

    token = get_bearer_token(
        tenant_id="your-tenant-id",
        client_id="your-client-id",
        secret="your-client-secret",
        scope="https://graph.microsoft.com/.default",
        mode="bearer"  # Options: 'bearer', 'token', 'raw'
    )
    
    print(token)
