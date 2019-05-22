#!/usr/bin/env python3
#
# This is adapted from https://github.com/softScheck/tplink-smartplug,
# created by Lubomir Stroetmann, Copyright 2016 softScheck GmbH and
# licensed under the Apache License, Version 2.0.
#
# It was converted from Python 2 to Python 3, made into a class for
# easy import and only the 'on' and 'off' commands were kept
#
# Clem Lorteau - 2019-05-21

import socket
from struct import pack

class Core:

    # Encryption and Decryption of TP-Link Smart Home Protocol
    # XOR Autokey Cipher with starting key = 171
    def encrypt(self, string):
        key = 171
        result = pack('>I', len(string))
        for i in string:
            a = key ^ ord(i)
            key = a
            result += bytes([a])
        return result

    def decrypt(self, string):
        key = 171
        result = ""
        for i in string:
            a = key ^ i
            key = i
            result += chr(a)
        return result

    # Send command and receive reply
    def sendCommand(self, ip, cmd):
        commands = {'on':  '{"system":{"set_relay_state":{"state":1}}}',
                    'off': '{"system":{"set_relay_state":{"state":0}}}'}
        port = 9999
        try:
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_tcp.connect((ip, port))
            sock_tcp.send(self.encrypt(commands[cmd]))
            data = sock_tcp.recv(2048)
            sock_tcp.close()
            print("Sent:     ", commands[cmd])
            print("Received: ", self.decrypt(data[4:]))
        except socket.error:
            raise Exception("Cound not connect to host " + ip + ":" + str(port))
