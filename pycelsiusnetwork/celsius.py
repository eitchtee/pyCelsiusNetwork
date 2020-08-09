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

    def get_transactions(self, raw: bool = False, **kwargs):
        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 100
        url = f"https://wallet-api.celsius.network/" \
              f"wallet/transactions?page={page}&per_page={per_page}"

        headers = {
            'X-Cel-Partner-Token': self.token,
            'X-Cel-Api-Key': self.key}

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        else:
            pagination = response.json().get('pagination')

            result = []
            result += response.json().get('record')

            if pagination['pages'] > page:
                for next_page in range(
                        pagination['current'] + 1, pagination['pages'] + 1):

                    url = f"https://wallet-api.celsius.network" \
                          f"/wallet" \
                          f"/transactions?page={next_page}&per_page={per_page}"

                    response = requests.request("GET", url, headers=headers)

                    result += response.json().get('record')

            return result
