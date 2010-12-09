"""this module creates a Client class to send data

manually to the server defined in the module charun"""
from socket import *

import json
import marshal

import charun_tac


def test_function(_dict):
    """top-level used for the purpose of demonstration.

    how to send a function over the UDP socket to the reactor.
    """
    _dict["add__test"] = "added field"
    return _dict


class Client():
    """a class to send data over a UDP socket is creates

    Public Functions:
    send - sends data to the socket
    send_func - sends a serialized function to the socket"""
    def __init__(self):
        """creates the client and sets address and UDPSock instance variable"""
        host = charun_tac.host
        port = charun_tac.port
        #buf = 1024
        self.addr = (host, port)
        self.UDPSock = socket(AF_INET, SOCK_DGRAM)

    def send(self, msg):
        """send a msg to the socket"""
        self.UDPSock.sendto(json.dumps(msg), self.addr)

    def send_func(self, i_function=None):
        """serialize the code of a function and send it the socket"""
        serialized_object = marshal.dumps(test_function.func_code)
        self.UDPSock.sendto(serialized_object, self.addr)


if __name__ == "__main__":
        msg = "Whatever message goes here..."
