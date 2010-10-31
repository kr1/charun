from socket import *
import json

class Sender():
    def __init__(self):
        host = "localhost"
        port = 9999
        buf = 1024
        self.addr = (host,port)
        self.UDPSock = socket(AF_INET,SOCK_DGRAM)
    def send(self, msg):    
        print self.UDPSock, self.addr
        self.UDPSock.sendto(json.dumps(msg), self.addr)

if __name__ == "__main__":
        msg = "Whatever message goes here..."



