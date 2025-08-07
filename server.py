import socket
import pickle
from mySignal import *
import time
import threading

HOST = '192.168.1.28'  
PORT = 5555    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

serverData = {}
print(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

def handleData(obj, addr):
    if obj.type == "CREATEROOM":
        print(obj)
        if obj.roomID not in serverData:
            serverData[obj.roomID] = {"PHASE" : "CREATEROOM", 
                                      "TIME" : None,
                                      "TURNINDEX" : 0,
                                      "LISTPLAYER" : [addr],
                                      "PLAYER" : {
                                          addr : None
                                        }
                                      }
        print(serverData)
        return SignalRecieved(serverData[obj.roomID]["PHASE"])

def handleRequest(data, addr):
    obj = pickle.loads(data)
    print(f"[SERVER] Nhận từ {addr}: {obj}")
    response = pickle.dumps(handleData(obj, addr))
    server_socket.sendto(response, addr)

while True:
    data, addr = server_socket.recvfrom(4096)
    threading.Thread(target=handleRequest, args=(data, addr)).start()
