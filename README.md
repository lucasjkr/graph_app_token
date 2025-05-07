# lucasjkr/MsGraphAuthenticator

A simple function for generation application bearer tokens for Graph API, using just the Requests package, rather than the more bloated msal package.

## Installation

Installation from git:

    pip install git+https://github.com/lucasjkr/graph_app_token


## Usage:
    from graph_app_token import bearer_token
    token = bearer_token(
                client_secret=secret, 
                client_id=client_id,
                tenant_id=tenant_id, 
                scope=scope)
