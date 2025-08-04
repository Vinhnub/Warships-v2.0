import socket
import pickle

HOST = '127.0.0.1'  
PORT = 5555    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

while True:
    data, addr = server_socket.recvfrom(4096)
    obj = pickle.loads(data)

    print(f"[SERVER] Nhận từ {addr}: {obj}")

    # Ví dụ phản hồi: gửi lại đối tượng đã sửa
    if isinstance(obj, dict):
        obj['server_response'] = "Dữ liệu đã nhận!"
    elif isinstance(obj, str):
        obj = f"[SERVER] Đã nhận: {obj}"

    response = pickle.dumps(obj)
    server_socket.sendto(response, addr)
