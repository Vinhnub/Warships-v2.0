import random
from constants import *
from ship import Ship
from botLogic import *
from listPath import *
from torpedo import *
from listPath import *
def extract_ships_from_boolean_map(boolean_map):
    rows = len(boolean_map)
    cols = len(boolean_map[0]) if rows > 0 else 0

    visited = [[False]*cols for _ in range(rows)]
    ships = []

    def neighbors(x, y):
        # 4 hướng lên, xuống, trái, phải
        for nx, ny in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if 0 <= nx < cols and 0 <= ny < rows:
                yield nx, ny

    for y in range(rows):
        for x in range(cols):
            if boolean_map[y][x] and not visited[y][x]:
                # BFS hoặc DFS để tìm tàu
                stack = [(x,y)]
                ship_cells = []
                while stack:
                    cx, cy = stack.pop()
                    if not visited[cy][cx]:
                        visited[cy][cx] = True
                        ship_cells.append((cx, cy))
                        for nx, ny in neighbors(cx, cy):
                            if boolean_map[ny][nx] and not visited[ny][nx]:
                                stack.append((nx, ny))
                ships.append(ship_cells)
    return ships
class PlayerAI():
    def __init__(self, window, enemy):
        self.window = window
        self.__listShips = []
        self.isReady = False
        self.listMyTorpedo = []
        self.listEnemyTorpedo = []
        self.canFire = None
        self.lastPosFire = None
        self.__listPosShip = [[False for _ in range(10)] for __ in range(10)]
        self._enemy = enemy
        self.__boardWidth = FIELD_WIDTH // CELL_SIZE[0]
        self.__boardHeight = FIELD_HEIGHT // CELL_SIZE[1]
        self.botLogic = BotLogic()
        self.botLogic.set_enemy_player(enemy)
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

    def isCorrect(self, pos):
        if pos is None:
            return False
        return self.__listPosShip[pos[0]][pos[1]]

    def grid_to_pixel(self, cell_x, cell_y):
        pixel_x = FIELD_COORD[0] + cell_x * CELL_SIZE[0]
        pixel_y = FIELD_COORD[1] + cell_y * CELL_SIZE[1]
        return pixel_x, pixel_y

    def auto_place_ships(self):
        ship_sizes = [5, 4, 3, 3, 2]
        self.__listShips = []

        for idx, size in enumerate(ship_sizes):
            placed = False
            while not placed:
                horizontal = random.choice([True, False])

                if horizontal:
                    cell_x = random.randint(0, self.__boardWidth - size)
                    cell_y = random.randint(0, self.__boardHeight - 1)
                else:
                    cell_x = random.randint(0, self.__boardWidth - 1)
                    cell_y = random.randint(0, self.__boardHeight - size)

                can_place = True
                for i in range(size):
                    x = cell_x + (i if horizontal else 0)
                    y = cell_y + (0 if horizontal else i)
                    if self.__listPosShip[x][y]:
                        can_place = False
                        break

                if can_place:
                    for i in range(size):
                        x = cell_x + (i if horizontal else 0)
                        y = cell_y + (0 if horizontal else i)
                        self.__listPosShip[x][y] = True

                    start_pixel = self.grid_to_pixel(cell_x, cell_y)
                    path = None
                    for p in listPathShip:
                        if p[2] == size:  
                            path = p[0]
                            break

                    if path is None:
                        path = listPathShip[0][0]

                    ship = Ship(self.window, start_pixel, path, idx)
                    self.__listShips.append(ship)
                    placed = True
        self.isReady = True

    def ready(self):
        return self.isReady
    def makeHit(self):
        pixel_loc = (FIELD_COORD[0] + pos[0] * CELL_SIZE[0] + 3, FIELD_COORD[1] + pos[1] * CELL_SIZE[1] + 3)
        torpedo = Torpedo(self.window, pixel_loc, listPathTorpedoAnimation, [pathImageHit, pathImageMiss], hit, spf=50)
        self.listMyTorpedo.append(torpedo)
        self.lastPosFire = pos
        hit, pos = self.botLogic.takeTurn()
        if hit is False and pos is None:
            return None
        elif:
    
    def get_ships_for_botlogic(self):
        return extract_ships_from_boolean_map(self._enemy.__listPosShip)