from socket import *
import json
import marshal
import charun_tac

class Sender():
    def __init__(self):
        host = charun_tac.host
        port = charun_tac.port
        #buf = 1024
        self.addr = (host,port)
        self.UDPSock = socket(AF_INET,SOCK_DGRAM)
    def send(self, msg):    
        print self.UDPSock, self.addr
        self.UDPSock.sendto(json.dumps(msg), self.addr)
    def send_func(self, i_function = None):
        """serialize the code of a function and send it the socket"""
        serialized_object = marshal.dumps(test_function.func_code)
        self.UDPSock.sendto(serialized_object, self.addr)


if __name__ == "__main__":
        msg = "Whatever message goes here..."

