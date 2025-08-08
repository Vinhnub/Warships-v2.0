import socket
import pickle
from mySignal import *
import time
import threading

HOST = '26.253.176.29'  
PORT = 5555    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

serverData = {}
print(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

def handleData(obj, addr):
    print(obj, addr)
    if obj.type == "CREATEROOM":
        if obj.roomID not in serverData:
            serverData[obj.roomID] = {"PHASE" : "CREATEROOM", 
                                      "TIME" : None,
                                      "TURNINDEX" : 0,
                                      "LISTPLAYER" : [addr[0]],
                                      "PLAYER" : {
                                          addr[0] : {
                                              "ready" : False,
                                              "posShip" : None,
                                              "listTorpedo" : []
                                          }
                                        }
                                      }
        return SignalRecieved(serverData[obj.roomID]["PHASE"])

    if obj.type == "JOINROOM":
        if obj.roomID not in serverData:
            print(1)
            return SignalRecieved("INVALID")
        else:
            if len(serverData[obj.roomID]["LISTPLAYER"]) >= 2:
                print(2)
                return SignalRecieved("INVALID")
            else:
                print(3)
                serverData[obj.roomID]["PHASE"] = "PREPARE"
                serverData[obj.roomID]["PLAYER"][addr[0]] = {"ready" : False, "posShip" : None, "listTorpedo" : []}
                serverData[obj.roomID]["LISTPLAYER"].append(addr[0])
                return SignalRecieved(serverData[obj.roomID]["PHASE"])
    

    

def handleRequest(data, addr):
    try:
        obj = pickle.loads(data)
        result = handleData(obj, addr)
        response = pickle.dumps(result)
        server_socket.sendto(response, addr)
        print(serverData)
    except Exception as e:
        print(f"[SERVER ERROR] Gói tin từ {addr} bị lỗi: {e}")


while True:
    data, addr = server_socket.recvfrom(4096)
    threading.Thread(target=handleRequest, args=(data, addr)).start()
