import socket
import pickle
import select
from mySignal import *

HOST = '192.168.1.28'  
PORT = 5555    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
server_socket.setblocking(False)  # Không chặn khi không có dữ liệu

dataServer = {}
print(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

while True:
    # Dùng select để kiểm tra socket có dữ liệu không
    ready_sockets, _, _ = select.select([server_socket], [], [], 0.1)  # timeout = 0.1 giây

    if server_socket in ready_sockets:
        data, addr = server_socket.recvfrom(4096)
        obj = pickle.loads(data)
        print(f"[SERVER] Nhận từ {addr}: {obj}")

        obj.setData(obj.data + 1)
        response = pickle.dumps(obj)
        server_socket.sendto(response, addr)
    
    
    print("[SERVER] Đang làm việc khác...")
