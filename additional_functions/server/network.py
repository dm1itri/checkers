import socket


class Network:
    """Взаимодействие с сервером со стороны клиента"""

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '5.23.55.52'
        self.port = 6668
        self.addr = (self.server, self.port)

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

    def close(self):
        self.client.close()