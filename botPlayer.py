import pygame
from pygame.locals import *
from constants import *     
from listPath import *        
from ship import Ship
from torpedo import Torpedo   

class PlayerAI():
    def __init__(self):
        self.__listShips = [Ship(path[1], path[0], path[2]) for path in listPathShip]
        self.isReady = False
        self.__listMyTorpedo = []
        self.__listEnemyTorpedo = []
        self.canFire = None
        self.numberCorrect = 0
        self.numberCorrectE = 0  
        self.startTime = None    
        self.finishGame = None

        self.__boardWidth = FIELD_WIDTH // CELL_SIZE[0]
        self.__boardHeight = FIELD_HEIGHT // CELL_SIZE[1]
        self.__listPosShip = [[False for _ in range(self.__boardHeight)] for _ in range(self.__boardWidth)]

    def calListPosShip(self):
        self.__listPosShip = [[False for _ in range(self.__boardHeight)] for _ in range(self.__boardWidth)]
        for ship in self.__listShips:
            for x in range(ship.loc[0], ship.loc[0] + ship.width, CELL_SIZE[0]):
                for y in range(ship.loc[1], ship.loc[1] + ship.height, CELL_SIZE[1]):
                    grid_x = int((x - FIELD_COORD[0]) / CELL_SIZE[0])
                    grid_y = int((y - FIELD_COORD[1]) / CELL_SIZE[1])
                    if 0 <= grid_x < self.__boardWidth and 0 <= grid_y < self.__boardHeight:
                        self.__listPosShip[grid_x][grid_y] = True
        return self.__listPosShip
    
    def handleEvent(self, event):
        pass

    # Vẽ tất cả đối tượng (tàu và đạn) lên cửa sổ
    def draw(self, window, isMyTurn=None):
        if isMyTurn is None:
            # Vẽ tàu của AI
            for ship in self.__listShips:
                ship.draw(window)
        elif isMyTurn:
            # Nếu đến lượt mình bắn, vẽ đạn của mình
            for oTorpedo in self.__listMyTorpedo:
                oTorpedo.draw(window)
        else:
            # Nếu không phải lượt mình bắn, vẽ tàu AI và đạn của đối thủ
            for ship in self.__listShips:
                ship.draw(window)
            for oTorpedo in self.__listEnemyTorpedo:
                oTorpedo.draw(window)

    # Hàm tự động đặt tàu (bạn cần bổ sung logic đặt tàu hợp lệ)
    def auto_place_ships(self):
        # Ví dụ: đặt ngẫu nhiên các tàu trong danh sách
        import random
        for ship in self.__listShips:
            placed = False
            while not placed:
                # random vị trí x, y trên bảng
                x = random.randint(FIELD_COORD[0], FIELD_COORD[0] + FIELD_WIDTH - ship.width)
                y = random.randint(FIELD_COORD[1], FIELD_COORD[1] + FIELD_HEIGHT - ship.height)
                # chuyển về vị trí chuẩn theo ô lưới
                x = FIELD_COORD[0] + ((x - FIELD_COORD[0]) // CELL_SIZE[0]) * CELL_SIZE[0]
                y = FIELD_COORD[1] + ((y - FIELD_COORD[1]) // CELL_SIZE[1]) * CELL_SIZE[1]

                # kiểm tra không đè lên tàu khác
                collision = False
                for other in self.__listShips:
                    if other == ship:
                        continue
                    rect1 = pygame.Rect(x, y, ship.width, ship.height)
                    rect2 = pygame.Rect(other.loc[0], other.loc[1], other.width, other.height)
                    if rect1.colliderect(rect2):
                        collision = True
                        break
                if not collision:
                    ship.loc = (x, y)
                    placed = True

        self.calListPosShip()
        self.isReady = True
 

            