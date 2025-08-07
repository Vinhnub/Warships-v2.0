import socket
import pickle

class NetWork():
    def __init__(self, serverIp):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = serverIp
        self.port = 5555
        self.addr = (self.server, self.port)

    def send(self, data):
        try:
            self._client.sendto(pickle.dumps(data), self.addr)
            responseData, self.server = self._client.recvfrom(4096)
            result = pickle.loads(responseData)
            return result
        except socket.error as e:
            print(e)

