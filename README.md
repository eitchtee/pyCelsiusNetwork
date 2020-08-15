<div align="center">
	<a href="https://pypi.org/project/pycelsiusnetwork/" target="_blank">
    	<img alt="pyCelsiusNetwork Example" title="pyCelsiusNetwork" src="./.github/images/header.png" />
    </a>
    </div>

<h3 align="center">pyCelsiusNetwork</h3>
<p align="center">Unofficial Python Wrapper for the Celcius Network API</p>

<div align="center">
  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/pycelsiusnetwork?style=for-the-badge">
  <a href="https://pypi.org/project/pycelsiusnetwork/" target="_blank"><img alt="PyPI" src="https://img.shields.io/pypi/v/pycelsiusnetwork?style=for-the-badge"></a>
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pycelsiusnetwork?style=for-the-badge">
  <img alt="PyPI - Downloads" src="https://img.shields.io/badge/dynamic/json?style=for-the-badge&color=303f9f&maxAge=86400&label=downloads&query=$.total_downloads&url=https://api.pepy.tech/api/projects/pycelsiusnetwork">
</div>

<br/>

<h5 align="center"> 
🚧 Under development: Things will break and change abruptly. 🚧
</h5>

---

<p align="center">
    <a href="#what-is-this">What is this?</a> |
    <a href="#requirements">Requirements</a> |
    <a href="#installation">Installation</a> |
    <a href="#usage-and-examples">Usage and Examples</a> |
    <a href="#roadmap">Roadmap</a> |
    <a href="#contributing">Contributing</a> |
    <a href="#license">License</a>
</p>

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
#### With ``pip``

```
$ pip install pycelsiusnetwork
```

#### Manual

1. Clone this repository
2. Run ```python setup.py install```

## Usage and Examples

### Docs
Additional documentation is provided through the ``__doc__`` attribute.

```
>> from pycelsiusnetwork import CelsiusNetwork

>> print(CelsiusNetwork.get_deposit_adress_for_coin.__doc__)
```

### Initialization
```python
from pycelsiusnetwork import CelsiusNetwork

api = CelsiusNetwork("PARTNER_TOKEN",
                     "USER_API_KEY")
```

### Filtering transactions
You don't neet to set all filtering options, only the ones you want.
> dt_from and dt_to also accepts datetime objects.
>
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

<p align="center">or</p>

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

## Roadmap

#### [Native API calls](https://documenter.getpostman.com/view/4207695/Rzn6v2mZ?version=latest#83677182-2cc9-4198-b574-77ad0862237b)
- [x] <small>``GET``</small> Balance summary
- [x] <small>``GET``</small> Balance for coin
- [x] <small>``GET``</small> Transactions summary
- [x] <small>``GET``</small> Transactions for coin
- [x] <small>``GET``</small> Get deposit address
- [x] <small>``GET``</small> Interest Rates
- [x] <small>``GET``</small> KYC

#### Abstraction Layer
- [x] Option for returning raw JSON
- [x] Depagination for ``Transactions summary`` and ``Transactions for coin``
- [x] Filtering for ``Transactions summary`` and ``Transactions for coin``

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

<!-- Please make sure to update tests as appropriate. -->

## License
[MIT](https://choosealicense.com/licenses/mit/)