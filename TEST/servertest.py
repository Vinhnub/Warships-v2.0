import socket
import pickle
from mySignal import *
import time
import threading

HOST = '192.168.1.28'  
PORT = 5555    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

dataServer = {}
print(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

def handle_request(data, addr):
    obj = pickle.loads(data)
    print(f"[SERVER] Nhận từ {addr}: {obj}")
    obj.setData(obj.data + 1)
    response = pickle.dumps(obj)
    server_socket.sendto(response, addr)

while True:
    data, addr = server_socket.recvfrom(4096)
    threading.Thread(target=handle_request, args=(data, addr)).start()
