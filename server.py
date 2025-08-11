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
| TIME      : {TIME_EACH_TURN - time.time() + serverData[roomID]["TIME"] if serverData[roomID]["TIME"] is not None else None}
| TURN      : {serverData[roomID]["TURNINDEX"]}
| LISTPLAYER: {serverData[roomID]["LISTPLAYER"]}
| PLAYER {serverData[roomID]["LISTPLAYER"][0]} : numCorrect : {serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][0]]["numCorrect"]}, lastPosFire : {serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][0]]["lastPosFire"]}, coolDown : {time.time() - serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][0]]["coolDown"]}                    
| PLAYER {serverData[roomID]["LISTPLAYER"][1] if len(serverData[roomID]["LISTPLAYER"] ) > 1 else None} : numCorrect :{serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][1]]["numCorrect"] if len(serverData[roomID]["LISTPLAYER"]) > 1 else None}, lastPosFire : {serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][1]]["lastPosFire"] if len(serverData[roomID]["LISTPLAYER"]) > 1 else None}, coolDown : {time.time() - serverData[roomID]["PLAYER"][serverData[roomID]["LISTPLAYER"][0]]["coolDown"] if len(serverData[roomID]["LISTPLAYER"]) > 1 else None}
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
                                              "listShip" : None,
                                              "listTorpedo" : [],
                                              "lastPosFire" : None,
                                              "numCorrect" : 0,
                                              "coolDown" : 0
                                          }
                                        }
                                      }
        return SignalRecieved(serverData[obj.roomID]["PHASE"])

    if obj.type == "JOINROOM":
        if obj.roomID not in serverData:
            return SignalRecieved("INVALID")
        elif serverData[obj.roomID]["PHASE"] == "CREATEROOM":
            if len(serverData[obj.roomID]["LISTPLAYER"]) >= 2:
                return SignalRecieved("INVALID")
            else:
                serverData[obj.roomID]["PHASE"] = "PREPARE"
                serverData[obj.roomID]["PLAYER"][addr[0]] = {"ready" : False, 
                                                             "posShip" : None, 
                                                             "listShip" : None,
                                                             "listTorpedo" : [], 
                                                             "lastPosFire" : None, 
                                                             "numCorrect" : 0, 
                                                             "coolDown" : 0
                                                             }
                serverData[obj.roomID]["LISTPLAYER"].append(addr[0])
                return SignalRecieved(serverData[obj.roomID]["PHASE"])

    # ======== PREPARE PHASE LOGIC ========        
    
    if serverData[obj.roomID]["PHASE"] == "PREPARE":
        if obj.type == "READY":
            serverData[obj.roomID]["PLAYER"][addr[0]]["ready"] = True
            serverData[obj.roomID]["PLAYER"][addr[0]]["posShip"] = obj.data
            serverData[obj.roomID]["PLAYER"][addr[0]]["coolDown"] = time.time() - COOL_DOWN
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
            serverData[obj.roomID]["TIME"] = time.time()

        enemyIndex = 1 - serverData[obj.roomID]["LISTPLAYER"].index(addr[0])
        enemy = serverData[obj.roomID]["LISTPLAYER"][enemyIndex]

        if obj.type == "WAITING_PL":
            if obj.data == len(serverData[obj.roomID]["PLAYER"][enemy]["listTorpedo"]):

                player1 = serverData[obj.roomID]["LISTPLAYER"][0]
                player2 = serverData[obj.roomID]["LISTPLAYER"][1]
                if serverData[obj.roomID]["PLAYER"][player1]["numCorrect"] >= NUM_CELL_SHIP or serverData[obj.roomID]["PLAYER"][player2]["numCorrect"] >= NUM_CELL_SHIP:
                    serverData[obj.roomID]["PHASE"] = "END"
                    return SignalRecieved(serverData[obj.roomID]["PHASE"],
                              data=(serverData[obj.roomID]["PLAYER"][addr[0]]["numCorrect"] >= NUM_CELL_SHIP))

                return SignalRecieved(serverData[obj.roomID]["PHASE"],  
                                      type="WAITING_PL",
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0],
                                      data=TIME_EACH_TURN - (time.time() - serverData[obj.roomID]["TIME"]), 
                                      coolDown=(time.time() - serverData[obj.roomID]["PLAYER"][addr[0]]["coolDown"]))
            else:
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      type="ENEMYFIRE", 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0], 
                                      data=serverData[obj.roomID]["PLAYER"][enemy]["lastPosFire"])
            
        if obj.type == "FIRETORPEDO":
            pos = obj.data
            if pos != serverData[obj.roomID]["PLAYER"][addr[0]]["lastPosFire"]: 
                serverData[obj.roomID]["PLAYER"][addr[0]]["listTorpedo"].append(pos)
                serverData[obj.roomID]["PLAYER"][addr[0]]["coolDown"] = time.time()
                
            if serverData[obj.roomID]["PLAYER"][enemy]["posShip"][pos[0]][pos[1]] > 0:
                if pos != serverData[obj.roomID]["PLAYER"][addr[0]]["lastPosFire"]:
                    if serverData[obj.roomID]["PLAYER"][enemy]["posShip"][pos[0]][pos[1]] == 1: serverData[obj.roomID]["PLAYER"][addr[0]]["numCorrect"] += 1
                    serverData[obj.roomID]["PLAYER"][addr[0]]["lastPosFire"] = pos
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      type="FIRETORPEDORESULT", 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0], 
                                      data=serverData[obj.roomID]["PLAYER"][enemy]["posShip"][pos[0]][pos[1]])
            else:
                serverData[obj.roomID]["PLAYER"][addr[0]]["lastPosFire"] = pos
                serverData[obj.roomID]["TIME"] = time.time() - (TIME_EACH_TURN - 4)
                return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                                      type="FIRETORPEDORESULT", 
                                      turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                                      playerIP=addr[0], 
                                      data=serverData[obj.roomID]["PLAYER"][enemy]["posShip"][pos[0]][pos[1]])
        
        return SignalRecieved(serverData[obj.roomID]["PHASE"], 
                              type="WAITING_PL",
                              turnIP=serverData[obj.roomID]["LISTPLAYER"][serverData[obj.roomID]["TURNINDEX"]], 
                              playerIP=addr[0],
                              data=TIME_EACH_TURN - (time.time() - serverData[obj.roomID]["TIME"]),
                              coolDown=(time.time() - serverData[obj.roomID]["PLAYER"][addr[0]]["coolDown"]))
    
    if serverData[obj.roomID]["PHASE"] == "END":
        if obj.type == "MYSHIP":
            serverData[obj.roomID]["PLAYER"][addr[0]]["listShip"] = obj.data
            enemyIndex = 1 - serverData[obj.roomID]["LISTPLAYER"].index(addr[0])
            enemy = serverData[obj.roomID]["LISTPLAYER"][enemyIndex]
            return SignalRecieved(serverData[obj.roomID]["PHASE"],
                                  type="ENEMYSHIP",
                                  data=serverData[obj.roomID]["PLAYER"][enemy]["listShip"])

        return SignalRecieved(serverData[obj.roomID]["PHASE"],
                              data=(serverData[obj.roomID]["PLAYER"][addr[0]]["numCorrect"] >= NUM_CELL_SHIP))


def handleRequest(data, addr):
    try:
        obj = pickle.loads(data)
        result = handleData(obj, addr)
        logging.info(f"{obj} {addr} {result}")
        response = pickle.dumps(result)
        server_socket.sendto(response, addr)
        #printdata(serverData)
    except Exception as e:
        logging.error(f"[SERVER ERROR] Gói tin từ {addr} bị lỗi: {e}")


while True:
    data, addr = server_socket.recvfrom(4096)
    threading.Thread(target=handleRequest, args=(data, addr)).start()
