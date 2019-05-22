#!/usr/bin/env python3
#
#Turn TP-Link Kasaa lights and plugs on and off
#Clem Lorteau - 2019-05-21

import argparse
import sys
from tplink import Core
from config import devices

ap = argparse.ArgumentParser(description='Turn lights on/off')
ap.add_argument('target', metavar='target', type=str, help='the name of the light to switch on/off, or \'all\'')
ap.add_argument('command', metavar='on/off', type=str, help='on or off')
args = ap.parse_args()

if (args.target == 'all'):
    for name, ip in devices.items():
        Core().sendCommand(ip, args.command)
else:
    Core().sendCommand(devices[args.target], args.command)

if (args.command != 'on' and args.command != 'off'):
    print('Invalid command')
    sys.exit(-1)


