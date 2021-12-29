import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.0.3'
        self.port = 5558
        self.addr = (self.server, self.port)
    #     self.first_connect = self.connect()
    #
    # def first_connect(self):
    #     return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(data.encode())
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def load(self):
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
