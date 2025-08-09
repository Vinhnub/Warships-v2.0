import socket
import pickle
from mySignal import *
import time
import threading
import random
import logging
from constants import *

# Cấu hình logging
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG để log chi tiết nhất
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler("server.log", encoding="utf-8"),  # Ghi vào file
        logging.StreamHandler()  # In ra màn hình
    ]
)

# # Ví dụ log
# logging.debug("Server đang khởi động...")
# logging.info("Đã kết nối với client 192.168.1.5")
# logging.warning("Gói tin không hợp lệ")
# logging.error("Lỗi xử lý dữ liệu")


HOST = '26.253.176.29'  
PORT = 5555    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

serverData = {}
logging.info(f"[SERVER] Đang lắng nghe tại {HOST}:{PORT}...")

def printdata(serverData):
    for roomID in serverData.keys():
        logging.info(f"""
===========================
|   Room Information      |
===========================
| Room ID   : {roomID}
| Phase     : {serverData[roomID]["PHASE"]}
| TIME      : {time.time() - serverData[roomID]["TIME"] if serverData[roomID]["TIME"] is not None else None}
| TURN      : {serverData[roomID]["TURNINDEX"]}
| LISTPLAYER: {serverData[roomID]["LISTPLAYER"]}
| PLAYER {serverData[roomID]["LISTPLAYER"][0]} : ready : {serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][0]]["ready"]}, lastPosFire : {serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][0]]["lastPosFire"]}
| PLAYER {serverData[roomID]["LISTPLAYER"][1] if len(serverData[roomID]["LISTPLAYER"] ) > 1 else None} : ready :{serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][1]]["ready"] if len(serverData[roomID]["LISTPLAYER"]) > 1 else None}, lastPosFire : {serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][1]]["lastPosFire"] if len(serverData[roomID]["LISTPLAYER"]) > 1 else None}
===========================
""")

def handleData(obj, addr):
    # ======== CREATE AND JOIN ROOM LOGIC ========

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
                                              "listTorpedo" : [],
                                              "lastPosFire" : None
                                          }
                                        }
                                      }
        return SignalRecieved(serverData[obj.roomID]["PHASE"])

    if obj.type == "JOINROOM":
        if obj.roomID not in serverData:
            return SignalRecieved("INVALID")
        else:
            if len(serverData[obj.roomID]["LISTPLAYER"]) >= 2:
                return SignalRecieved("INVALID")
            else:
                serverData[obj.roomID]["PHASE"] = "PREPARE"
                serverData[obj.roomID]["PLAYER"][addr[0]] = {"ready" : False, "posShip" : None, "listTorpedo" : [], "lastPosFire" : None}
                serverData[obj.roomID]["LISTPLAYER"].append(addr[0])
                return SignalRecieved(serverData[obj.roomID]["PHASE"])

    # ======== PREPARE PHASE LOGIC ========        
    
    if serverData[obj.roomID]["PHASE"] == "PREPARE":
        if obj.type == "READY":
            serverData[obj.roomID]["PLAYER"][addr[0]]["ready"] = True
            serverData[obj.roomID]["PLAYER"][addr[0]]["posShip"] = obj.data
            enemyIndex = 1 - serverData[obj.roomID]["LISTPLAYER"].index(addr[0])
            enemy = serverData[obj.roomID]["LISTPLAYER"][enemyIndex]
            if serverData[obj.roomID]["PLAYER"][enemy]["ready"]:
                serverData[obj.roomID]["PHASE"] = "PLAYING"
                serverData[obj.roomID]["TIME"] = time.time()
                serverData[obj.roomID]["TURNINDEX"] = random.randint(0, 1)
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0])

        return SignalRecieved(serverData[obj.roomID]["PHASE"])
        
    # ======== PLAYING PHASE LOGIC ========

    if serverData[obj.roomID]["PHASE"] == "PLAYING":

        if TIME_EACH_TURN - (time.time() - serverData[obj.roomID]["TIME"]) <= 0:
            serverData[obj.roomID]["TURNINDEX"] = 1 - serverData[obj.roomID]["TURNINDEX"]
            serverData[obj.roomID]["TIME"] = time.time() - (TIME_EACH_TURN - 3000)

        enemyIndex = 1 - serverData[obj.roomID]["LISTPLAYER"].index(addr[0])
        enemy = serverData[obj.roomID]["LISTPLAYER"][enemyIndex]

        if obj.type == "WAITING":
            if obj.data == len(serverData[obj.roomID]["PLAYER"][enemy]["listTorpedo"]):
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0])
            else:
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      type="ENEMYFIRE", 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0], 
                                      data=serverData[obj.roomID]["PLAYER"][enemy]["lastPosFire"])
            
        if obj.type == "FIRE":
            pos = obj.data
            serverData[obj.roomID]["TIME"] = 
            if pos != serverData[obj.roomID]["PLAYER"][addr[0]]["lastPosFire"]: 
                serverData[obj.roomID]["PLAYER"][addr[0]]["listTorpedo"].append(pos)
                serverData[obj.roomID]["PLAYER"][addr[0]]["lastPosFire"] = pos
                
            if serverData[obj.roomID]["PLAYER"][enemy]["posShip"][pos[0]][pos[1]]:
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      type="FIRERESULT", 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0], 
                                      data=True)
            else:
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      type="FIRERESULT", 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0], 
                                      data=False)
            

        
        return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                              turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                              playerIP=addr[0])
    

def handleRequest(data, addr):
    try:
        obj = pickle.loads(data)
        result = handleData(obj, addr)
        response = pickle.dumps(result)
        server_socket.sendto(response, addr)
        printdata(serverData)
    except Exception as e:
        logging.error(f"[SERVER ERROR] Gói tin từ {addr} bị lỗi: {e}")


while True:
    data, addr = server_socket.recvfrom(4096)
    threading.Thread(target=handleRequest, args=(data, addr)).start()
