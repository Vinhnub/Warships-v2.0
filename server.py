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
        if obj.roomID not in serverData:
            serverData[obj.roomID] = {"PHASE" : "CREATEROOM", 
                                      "TIME" : None,
                                      "TURNINDEX" : 0,
                                      "LISTPLAYER" : [addr],
                                      "PLAYER" : {
                                          addr : None
                                        }
                                      }
        return SignalRecieved(serverData[obj.roomID]["PHASE"])

    if obj.type == "JOINROOM":
        if obj.roomID not in serverData:
            return SignalRecieved("ERROR")
        else:
            if len(serverData[obj.roomID]["LISTPLAYER"]) >= 2:
                return SignalRecieved("ERROR")
            else:
                serverData[obj.roomID]["PHASE"] = "PREPARE"
                serverData[obj.roomID]["PLAYER"][addr] = None
                serverData[obj.roomID]["LISTPLAYER"].append(addr)
                return SignalRecieved(serverData[obj.roomID]["PHASE"])
            

def handleRequest(data, addr):
    obj = pickle.loads(data)
    response = pickle.dumps(handleData(obj, addr))
    server_socket.sendto(response, addr)
    print(serverData)

while True:
    data, addr = server_socket.recvfrom(4096)
    threading.Thread(target=handleRequest, args=(data, addr)).start()
