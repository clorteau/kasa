# kasa

This is a small desktop application that allows turning TP-Link Kasa smart plugs and switches on and off. It's written Python using the Qt framework and runs on Linux, Windows and Mac OS X.

It uses Lubomir Stroetmann's script available at https://github.com/softScheck/tplink-smartplug at its core.

## Pre-requisites

* Python 3.x
* PySide2
* Reserve your TP-Link Kasa devices' IP address in your DHCP server so they don't change

## Configuration

Edit config.py to give names and IP addresses to your Kasa devices. A "all lights" entry will be added automatically.

## Usage
### GUI

Run kasa.py via python. Click the On/Off buttons to control the switches.

(http://www.lorteau.fr/images/kasa.png)

### CLI

Syntax:
```bash
$ python kasa-cli.py -h
usage: kasa-cli.py [-h] target on/off

Turn lights on/off

positional arguments:
  target      the name of the light to switch on/off, or 'all'
  on/off      on or off

optional arguments:
  -h, --help  show this help message and exit
```

For instance:
```
$ python kasa-cli.py lamp on
```

Or:
```
$ python kasa-cli.py all off
```
