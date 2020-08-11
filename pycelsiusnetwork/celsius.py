import requests
from .exceptions import AbstractionFailure, CelsiusNetworkHTTPError


class CelsiusNetwork:
    def __init__(self,
                 partner_token: str,
                 api_key: str,
                 enviroment: str = 'PRODUCTION',
                 silent: bool = False):

        self._token = partner_token
        self._key = api_key

        if enviroment.upper() == 'PRODUCTION':
            self._base_url = "https://wallet-api.celsius.network"
        elif enviroment.upper() == 'STAGING':
            self._base_url = "https://wallet-api.staging.celsius.network"
        else:
            self._base_url = "https://wallet-api.celsius.network"

        self.headers = {
            'X-Cel-Partner-Token': self._token,
            'X-Cel-Api-Key': self._key
        }

        self.silent = silent

    def get_wallet_balance(self,
                           raw: bool = False,
                           silent: bool = None):

        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              "/wallet" \
              "/balance"

        response = requests.request("GET", url, headers=self.headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        json = response.json()
        if raw:
            return json
        else:
            try:
                fetch_balance = json['balance']
            except KeyError:
                if (self.silent and silent) or silent:
                    return None
                else:
                    raise AbstractionFailure(json=json)
            else:
                return fetch_balance

    def get_coin_balance(self,
                         coin: str,
                         return_type: str = 'in_coin',
                         raw: bool = False,
                         silent: bool = None):

        coin = coin.upper()
        silent = silent if silent is not None else self.silent
        return_type = return_type.lower()

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/{coin}" \
              f"/balance"

        response = requests.request("GET", url, headers=self.headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        json = response.json()
        if raw:
            return json
        else:
            try:
                fetch_in_coin = json['amount']
                fetch_in_usd = json['amount_in_usd']
            except KeyError:
                if (self.silent and silent) or silent:
                    return None
                else:
                    raise AbstractionFailure(json=json)
            else:
                if return_type == 'in_coin':
                    return fetch_in_coin
                elif return_type == 'in_usd':
                    return fetch_in_usd
                elif return_type == 'both':
                    return {'in_coin': fetch_in_coin,
                            'in_usd': fetch_in_usd}

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

        response = requests.request("GET", url, headers=self.headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        json = response.json()
        if raw:
            return json
        elif depaginate:
            # Depaginate results and return then as one list
            result = []
            try:
                result += json['record']

                pagination = json['pagination']
                if pagination['pages'] > page:
                    for next_page in range(
                            pagination['current'] + 1, pagination['pages'] + 1):
                        url = f"{self._base_url}" \
                              f"/wallet" \
                              f"/transactions?page={next_page}&per_page={per_page}"
                        response = requests.request("GET", url,
                                                    headers=self.headers)

                        json = response.json()
                        result += json['record']
            except KeyError:
                if (self.silent and silent) or silent:
                    return None
                else:
                    raise AbstractionFailure(json=json)

            if reverse:
                result.reverse()

            return result

        else:
            try:
                fetch_record = json['record']
            except KeyError:
                if (self.silent and silent) or silent:
                    return None
                else:
                    raise AbstractionFailure(json=json)
            else:
                return fetch_record

    def get_transactions_for_coin(self,
                                  coin: str,
                                  depaginate: bool = True,
                                  reverse: bool = False,
                                  raw: bool = False,
                                  silent: bool = None,
                                  **kwargs):

        coin = coin.upper()
        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 100
        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/{coin}" \
              f"/transactions?page={page}&per_page={per_page}"

        response = requests.request("GET", url, headers=self.headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        json = response.json()
        if raw:
            return json
        elif depaginate:
            # Depaginate results and return then as one list
            result = []
            try:
                result += json['record']

                pagination = json['pagination']
                if pagination['pages'] > page:
                    for next_page in range(
                            pagination['current'] + 1, pagination['pages'] + 1):
                        url = f"{self._base_url}" \
                              f"/wallet" \
                              f"/transactions?page={next_page}&per_page=" \
                              f"{per_page}"
                        response = requests.request("GET", url,
                                                    headers=self.headers)

                        json = response.json()
                        result += json['record']
            except KeyError:
                if (self.silent and silent) or silent:
                    return None
                else:
                    raise AbstractionFailure(json=json)

            if reverse:
                result.reverse()

            return result

        else:
            try:
                fetch_record = json['record']
            except KeyError:
                if (self.silent and silent) or silent:
                    return None
                else:
                    raise AbstractionFailure(json=json)
            else:
                return fetch_record

    def get_deposit_adress_for_coin(self,
                                    coin: str,
                                    raw: bool = False,
                                    silent: bool = None):

        coin = coin.upper()
        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              "/wallet" \
              f"/{coin}" \
              "/deposit"

        response = requests.request("GET", url, headers=self.headers)

        if not response.ok:
            if (self.silent and silent) or silent:
                return None
            else:
                raise CelsiusNetworkHTTPError(response)

        json = response.json()
        if raw:
            return json
        else:
            try:
                fetch_address = json['address']
            except KeyError:
                if (self.silent and silent) or silent:
                    return None
                else:
                    raise AbstractionFailure(json=json)
            else:
                return fetch_address
