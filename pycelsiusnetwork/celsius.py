import requests
from .exceptions import CelsiusNetworkHTTPError


class CelsiusNetwork:
    def __init__(self,
                 partner_token: str,
                 api_key: str,
                 enviroment: str = 'PRODUCTION',
                 silent: bool = False):

        self._token = str(partner_token)
        self._key = str(api_key)

        if str(enviroment).upper() == 'PRODUCTION':
            self._base_url = "https://wallet-api.celsius.network"
        elif str(enviroment).upper() == 'STAGING':
            self._base_url = "https://wallet-api.staging.celsius.network"
        else:
            self._base_url = "https://wallet-api.celsius.network"

        self.silent = silent

    def get_wallet_balance(self,
                           raw: bool = False,
                           silent: bool = None):

        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              "/wallet" \
              "/balance"

        headers = {
            'X-Cel-Partner-Token': self._token,
            'X-Cel-Api-Key': self._key
        }

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        else:
            return response.json().get('balance')

    def get_coin_balance(self,
                         coin: str,
                         raw: bool = False,
                         silent: bool = None):

        coin = str(coin).upper()
        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/{coin}" \
              f"/balance"

        headers = {
            'X-Cel-Partner-Token': self._token,
            'X-Cel-Api-Key': self._key
        }

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        else:
            return response.json().get('amount'), \
                   response.json().get('amount_in_usd'),

    def get_transactions(self,
                         depaginate: bool = True,
                         reverse: bool = False,
                         raw: bool = False,
                         silent: bool = None,
                         **kwargs):

        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 100
        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/transactions?page={page}&per_page={per_page}"

        headers = {
            'X-Cel-Partner-Token': self._token,
            'X-Cel-Api-Key': self._key}

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        elif depaginate:
            # Depaginate results and return then as one list
            result = []
            result += response.json().get('record') or []

            pagination = response.json().get('pagination')
            if pagination['pages'] > page:
                for next_page in range(
                        pagination['current'] + 1, pagination['pages'] + 1):
                    url = f"https://wallet-api.celsius.network" \
                          f"/wallet" \
                          f"/transactions?page={next_page}&per_page={per_page}"
                    response = requests.request("GET", url, headers=headers)

                    result += response.json().get('record') or []

            if reverse:
                result.reverse()

            return result
        else:
            return response.json().get('record')

    def get_transactions_for_coin(self,
                                  coin: str,
                                  depaginate: bool = True,
                                  reverse: bool = False,
                                  raw: bool = False,
                                  silent: bool = None,
                                  **kwargs):

        coin = str(coin).upper()
        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 100
        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/{coin}" \
              f"/transactions?page={page}&per_page={per_page}"

        headers = {
            'X-Cel-Partner-Token': self._token,
            'X-Cel-Api-Key': self._key}

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        elif depaginate:
            # Depaginate results and return then as one list
            result = []
            result += response.json().get('record') or []

            pagination = response.json().get('pagination')
            if pagination['pages'] > page:
                for next_page in range(
                        pagination['current'] + 1, pagination['pages'] + 1):
                    url = f"https://wallet-api.celsius.network" \
                          f"/wallet" \
                          f"/{coin}" \
                          f"/transactions?page={next_page}&per_page={per_page}"
                    response = requests.request("GET", url, headers=headers)

                    result += response.json().get('record') or []

            if reverse:
                result.reverse()

            return result
        else:
            return response.json().get('record')

    def get_deposit_adress_for_coin(self,
                                    coin: str,
                                    raw: bool = False,
                                    silent: bool = None):

        coin = str(coin).upper()
        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              "/wallet" \
              f"/{coin}" \
              "/deposit"

        headers = {
            'X-Cel-Partner-Token': self._token,
            'X-Cel-Api-Key': self._key
        }

        response = requests.request("GET", url, headers=headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        if raw:
            return response.json()
        else:
            return response.json().get('address')
