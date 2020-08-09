import requests
from .exceptions import CelsiusNetworkHTTPError


class CelsiusNetwork:
    def __init__(self, partner_token: str, api_key: str):
        self.token = str(partner_token)
        self.key = str(api_key)

    def get_wallet_balance(self, raw: bool = False):
        url = "https://wallet-api.celsius.network/wallet/balance"

        headers = {
            'X-Cel-Partner-Token': self.token,
            'X-Cel-Api-Key': self.key
        }

        response = requests.request("GET", url, headers=headers)

        print(response.status_code)

        if not response.ok:
            raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        else:
            return response.json().get('balance')

    def get_coin_balance(self, coin: str, raw: bool = False):
        coin = str(coin).upper()

        url = f"https://wallet-api.celsius.network/wallet/{coin}/balance"

        headers = {
            'X-Cel-Partner-Token': self.token,
            'X-Cel-Api-Key': self.key
        }

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        else:
            return response.json().get('amount'),\
                   response.json().get('amount_in_usd'),
