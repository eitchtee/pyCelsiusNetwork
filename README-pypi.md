# pyCelsiusNetwork
Unofficial Python Wrapper for the Celcius Network API

**See more on [Github](https://github.com/eitchtee/pyCelsiusNetwork)**

---

## What is this?
**pyCelsiusNetwork** is a Python API Wrapper for [Celsius Network](https://celsius.network/) public API.
This package also offers a short-and-sweet abstraction layer, with functions like depagination of API Results, reversing, and filtering, but the raw JSON response is always one paramether away.

## Requirements
You will need:
 - a Omnibus Treasury Partner Token, you can read on how to get one [here](https://developers.celsius.network/omnibus-treasury.html).
 - a Celsius Account API Key, you can read on how to generate one [here](https://developers.celsius.network/createAPIKey.html)
 - a computer with ``Python 3.5+`` and ``pip`` installed

## Installation

```
$ pip install pycelsiusnetwork
```

## Usage and Examples

### Docs
Additional documentation is provided through the ``__doc__`` attribute.

```
>> from pycelsiusnetwork import CelsiusNetwork

>> print(CelsiusNetwork.get_deposit_adress_for_coin.__doc__)
```

### Initialization
```python
from pycelsiusnetwork import CelsiusNetwork, Env

api = CelsiusNetwork(partner_token="PARTNER_TOKEN",
                     api_key="USER_API_KEY",
                     enviroment=Env.PRODUCTION)
```

### Filtering transactions
You don't neet to set all filtering options, only the ones you want.
> dt_from and dt_to also accepts datetime objects and other ISO compliant strings.

```python
filtered_transactions = api.get_transactions(dt_from="2020-01-01",
                                             dt_to="2020-05-01",
                                             state="confirmed",
                                             nature="interest",
                                             amount_lower_than=2,
                                             amount_bigger_than=0.1)
```

### Silence errors
By passing `silent=True` to any function or the API object itself, you can mute package exceptions, A.K.A. `AbstractionFailure` and `CelsiusNetworkHTTPError`, by doing so, `None` will be returned in the presence of an error instead of raising an Exception.

```python
api = CelsiusNetwork("PARTNER_TOKEN",
                     "USER_API_KEY",
                     silent=True)
```

or

```python
api.get_deposit_adress_for_coin('BTC', silent=True)
```

Also, if you pass ``silent=True`` to the API initialization, you can override it for any function by passing ``silent=False`` to it.

```python
api = CelsiusNetwork("PARTNER_TOKEN",
                     "USER_API_KEY",
                     silent=True)

api.get_deposit_adress_for_coin('BTC', silent=False)
```

### Getting the raw response
If you want to ignore the abstraction layer and get access to that juicy JSON directly, you can pass ``raw=True`` to any function, doing so, will make the function return the full response JSON.

```python
api.get_supported_coins(raw=True)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)