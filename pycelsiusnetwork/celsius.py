import requests
from .exceptions import AbstractionFailure, CelsiusNetworkHTTPError
from .utils import get_key, filter_json


class CelsiusNetwork:
    def __init__(self,
                 partner_token: str,
                 api_key: str,
                 enviroment: str = 'production',
                 silent: bool = False):

        self._token = partner_token
        self._key = api_key

        if enviroment.lower() == 'production':
            self._base_url = "https://wallet-api.celsius.network"
        elif enviroment.upper() == 'staging':
            self._base_url = "https://wallet-api.staging.celsius.network"
        else:
            self._base_url = "https://wallet-api.celsius.network"

        self.headers = {
            'X-Cel-Partner-Token': self._token,
            'X-Cel-Api-Key': self._key
        }

        self.silent = silent

    def get_interest_rate(self,
                          coin: str = None,
                          raw: bool = False,
                          silent: bool = None):

        silent = silent if silent is not None else self.silent
        coin = coin.upper() if coin else None

        url = f"{self._base_url}" \
              "/util" \
              "/interest" \
              "/rates"

        response = requests.request("GET", url)

        if silent and not response.ok:
            return None
        elif not silent and not response.ok:
            raise CelsiusNetworkHTTPError(response)

        json = response.json()

        if raw:
            return json
        else:
            rates = get_key(key='interestRates', json=json, silent=silent)
            rates_list = [{'coin': x['coin'], 'rate': x['rate']} for x in rates]
            rates_dict = {item.pop("coin"): item['rate'] for item in rates_list}
            if coin:
                return rates_dict[coin]
            else:
                return rates_dict

    def get_wallet_balance(self,
                           raw: bool = False,
                           silent: bool = None):

        silent = silent if silent is not None else self.silent

        url = f"{self._base_url}" \
              "/wallet" \
              "/balance"

        response = requests.request("GET", url, headers=self.headers)

        if silent and not response.ok:
            return None
        elif not silent and not response.ok:
            raise CelsiusNetworkHTTPError(response)

        json = response.json()
        if raw:
            return json
        else:
            return get_key(key='balance', json=json, silent=silent)

    def get_coin_balance(self,
                         coin: str,
                         raw: bool = False,
                         return_type: str = 'in_coin',
                         silent: bool = None):

        coin = coin.upper()
        silent = silent if silent is not None else self.silent
        return_type = return_type.lower()

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/{coin}" \
              f"/balance"

        response = requests.request("GET", url, headers=self.headers)

        if silent and not response.ok:
            return None
        elif not silent and not response.ok:
            raise CelsiusNetworkHTTPError(response)

        json = response.json()

        if raw:
            return json
        else:
            if return_type == 'in_coin':
                in_coin = get_key(key='amount', json=json, silent=silent)
                return in_coin
            elif return_type == 'in_usd':
                in_usd = get_key(key='amount_in_usd', json=json, silent=silent)
                return in_usd
            elif return_type == 'both':
                in_coin = get_key(key='amount', json=json, silent=silent)
                in_usd = get_key(key='amount_in_usd', json=json, silent=silent)
                return {'in_coin': in_coin,
                        'in_usd': in_usd}

    def get_transactions(self,
                         raw: bool = False,
                         depaginate: bool = True,
                         reverse: bool = False,
                         silent: bool = None,
                         **kwargs):

        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 100
        silent = silent if silent is not None else self.silent

        # Filter options
        dt_from = kwargs.get('dt_from')
        dt_to = kwargs.get('dt_to')
        amount_bigger_than = kwargs.get('amount_bigger_than')
        amount_lower_than = kwargs.get('amount_lower_than')
        state = kwargs.get('state')
        nature = kwargs.get('nature')

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/transactions?page={page}&per_page={per_page}"

        response = requests.request("GET", url, headers=self.headers)

        if silent and not response.ok:
            return None
        elif not silent and not response.ok:
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

            return filter_json(dt_from,
                               dt_to,
                               amount_bigger_than,
                               amount_lower_than,
                               state,
                               nature)

        else:
            return get_key(key='record', json=json, silent=silent)

    def get_transactions_for_coin(self,
                                  coin: str,
                                  raw: bool = False,
                                  depaginate: bool = True,
                                  reverse: bool = False,
                                  silent: bool = None,
                                  **kwargs):

        coin = coin.upper()
        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 100
        silent = silent if silent is not None else self.silent

        # Filter options
        dt_from = kwargs.get('dt_from')
        dt_to = kwargs.get('dt_to')
        amount_bigger_than = kwargs.get('amount_bigger_than')
        amount_lower_than = kwargs.get('amount_lower_than')
        state = kwargs.get('state')
        nature = kwargs.get('nature')

        url = f"{self._base_url}" \
              f"/wallet" \
              f"/{coin}" \
              f"/transactions?page={page}&per_page={per_page}"

        response = requests.request("GET", url, headers=self.headers)

        if silent and not response.ok:
            return None
        elif not silent and not response.ok:
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

            return filter_json(dt_from,
                               dt_to,
                               amount_bigger_than,
                               amount_lower_than,
                               state,
                               nature)

        else:
            return get_key(key='record', json=json, silent=silent)

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

        if silent and not response.ok:
            return None
        elif not silent and not response.ok:
            raise CelsiusNetworkHTTPError(response)

        json = response.json()

        if raw:
            return json
        else:
            return get_key(key='address', json=json, silent=silent)
