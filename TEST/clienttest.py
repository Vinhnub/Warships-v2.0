import socket
import pickle
from mySignal import Signal  # Đảm bảo tên class đúng với bên server

HOST = '192.168.1.28'  # Địa chỉ IP của server
PORT = 5555            # Cổng server đang lắng nghe

# Tạo socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Tạo đối tượng để gửi
count = 0
while True:
    count += 1
    signal = Signal(count)  # Giả sử bạn muốn gửi giá trị 10, có thể thay đổi

    # Gửi dữ liệu đi
    data = pickle.dumps(signal)
    client_socket.sendto(data, (HOST, PORT))

    # Nhận phản hồi từ server
    response, server_addr = client_socket.recvfrom(4096)
    received_obj = pickle.loads(response)

    print(f"[CLIENT] Phản hồi từ server: {received_obj}")

client_socket.close()
