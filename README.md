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

The application needs to be configured so that it knows what sensors it reads data from.
A example configuration file is provided and can be found at `sensors.json`, it contains a example and test configuration. The configuration consists of a id and a descriptive name, the name can be chosen freely and be what ever seems appropriate e.g. a room name.

See [my blog post](http://blog.polarcoder.net/2016/02/diy-home-automation-v2.html) for details on how to find out what the correct id's are for your sensors if you have any.

### Example configuration

```Javascript
[
    {
        "id": 135,
        "name": "Parveke"
    },
    {
        "id": 136,
        "name": "Olohuone"
    }
]
```

## Run application

Once prequisites are met and dependencies installed the application can run as `python http_api.py sensors.json`. If you have
python 2 and 3 installed the command `python` probably needs to be replaced with command `python3`.

### Run application with pm2

`pm2 start --interpreter=/usr/bin/python3 --name=tellstick-py-api http_api.py -- sensors.json`

## Endpoints

### List sensors

http://0.0.0.0:5001/tellstick/sensors

#### Response example

```Javascript
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

http://0.0.0.0:5001/tellstick/devices

## Response example

```Javascript
{
    devices: [
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
    ],
    groups: []
}
```

### Turn on switches

* Method: POST
* Content-Type: application/json
* URL: http://0.0.0.0:5001/tellstick/devices/on

## Request body example

[115,116]

## Response example

```Javascript
{
    devices: [
    {
        "name": "Makuuhuone",
        "switchedOn": true,
        "id": 115
    },
    {
        "name": "OH TV",
        "switchedOn": true,
        "id": 116
    }
    ],
    groups: []
}
```

### Turn off switches

* Method: POST
* Content-Type: application/json
* URL: http://0.0.0.0:5001/tellstick/devices/off

## Request body example

[115,116]

## Response example

```Javascript
{
    devices: [
    {
        "name": "Makuuhuone",
        "switchedOn": false,
        "id": 115
    },
    {
        "name": "OH TV",
        "switchedOn": false,
        "id": 116
    }
    ],
    groups: []
}
```

## Tests

No tests at this time as I'm still trying to figure out how to unit test this properly.
