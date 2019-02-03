# ruuvitag-api

HTTP REST JSON API for reading tellstick sensor and switch data and to control tellstick switches, implemented in Python.

## Prequisites

* Python 3.5 or later
* pip

Python 3.5+ is required because the application uses reactive extensions (rx) implementation of ruuvitag reader.

### Install dependencies

`pip install -r requirements.txt` or if you have pip for python 2 and 3 then `pip3 install -r requirements.txt`.

The `tellcore-py` module has it's own requirements that need to be attended, see details from [tellcore-py's README](https://github.com/erijo/tellcore-py).

## Configuring application

TODO

### Example configuration

TODO

## Run application

Once prequisites are met and dependencies installed the application can run as `python http_api.py`. If you have
python 2 and 3 installed the command `python` probably needs to be replaced with command `python3`.

## Endpoints

### List sensors

http://0.0.0.0:5001/tellstick/sensors

#### Response example

```
[
  {
    "id": 136,
    "temperature": 23.3,
    "humidity": 36
    "name": "Makuuhuone"
  },
  {
    "id": 135,
    "temperature": -2.4,
    "name": "Parveke"
  }
]
```

### List switches

http://0.0.0.0:5001/tellstick/switches

## Response example

```
[
  {
    "name": "Makuuhuone",
    "switchedOn": false,
    "id": 115
  },
  {
    "name": "OH TV",
    "switchedOn": true,
    "id": 116
  }
]
```

## Tests

TODO
