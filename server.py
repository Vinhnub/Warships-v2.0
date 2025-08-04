import socket
import pickle
from mySignal import *

HOST = '192.168.1.28'  
PORT = 5555    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

while True:
    data, addr = server_socket.recvfrom(4096)
    obj = pickle.loads(data)

    print(f"[SERVER] Nhận từ {addr}: {obj}")

    # Ví dụ phản hồi: gửi lại đối tượng đã sửa
    obj.setData(obj.data + 1)
    print(obj.data)
    response = pickle.dumps(obj)
    server_socket.sendto(response, addr)
# server UDP socket