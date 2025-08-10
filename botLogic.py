import random

class Bot:
    def __init__(self, BOARD_SIZE=10):
        self._BOARD_SIZE = BOARD_SIZE
        self._board = [[0] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]
        self._cells = [(x, y) for x in range(self._BOARD_SIZE) for y in range(self._BOARD_SIZE)]
        self._ships = [
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
            [(2, 2), (3, 2), (4, 2), (5, 2)],
            [(7, 0), (7, 1), (7, 2)],
            [(5, 5), (6, 5)],
            [(9, 9)]
        ]

        self._turnCount = 0
        self._preSuspicious = []
        self._suspicious = []
        self._streak = []
        self._direction = None
        self._directionMode = None  # forward hoặc backward
        self._remainShips = [len(ship) for ship in self._ships]
        self._rootCell = None
        self._result = None
    def secondBoard(self):
        secondBoard = [[0 for _ in range(self._BOARD_SIZE)] for _ in range(self._BOARD_SIZE)]
        for shipSize in self._remainShips:
            for x in range(self._BOARD_SIZE):
                for y in range(self._BOARD_SIZE - shipSize + 1):
                    positions = [(x, y+i) for i in range(shipSize)]
                    if all(self._board[px][py] == 0 for px, py in positions):
                        for px, py in positions:
                            secondBoard[px][py] += 1
            for y in range(self._BOARD_SIZE):
                for x in range(self._BOARD_SIZE - shipSize + 1):
                    positions = [(x+i, y) for i in range(shipSize)]
                    if all(self._board[px][py] == 0 for px, py in positions):
                        for px, py in positions:
                            secondBoard[px][py] += 1
        return secondBoard

    def randomMode(self):
        EstimazeBoard = self.secondBoard()
        self._suspicious = [pos for pos in self._suspicious if pos in self._cells]
        if self._suspicious:
            maxValue = max(EstimazeBoard[x][y] for (x, y) in self._suspicious)
            bestCells = [(x, y) for (x, y) in self._suspicious if EstimazeBoard[x][y] == maxValue]
        else:
            maxValue = max(max(row) for row in EstimazeBoard)
            bestCells = [(x, y) for x in range(self._BOARD_SIZE)
                         for y in range(self._BOARD_SIZE)
                         if EstimazeBoard[x][y] == maxValue and (x, y) in self._cells]

        if bestCells:
            return self.checkTarget(random.choice(bestCells))
        elif self._cells:
            return self.checkTarget(random.choice(self._cells))
        else:
        # Hết ô để bắn rồi, game kết thúc hoặc không còn nước đi
            return False, None
    def isShipSunk(self, ship):
        return all(self._board[x][y] == 1 for (x, y) in ship)
    def checkTarget(self, target):
        if target not in self._cells:
            return False, None
        self._cells.remove(target)
        self._turnCount += 1
        x, y = target
        for ship in list(self._ships):
            if target in ship:
                self._board[x][y] = 1
                # Cập nhật self._streak đúng chiều
                if self._directionMode == "backward":
                    self._streak.insert(0, target)  # chèn đầu danh sách
                else:
                    self._streak.append(target)  # thêm cuối danh sách
                # Xác định hướng khi mới trúng
                if len(self._streak) == 1:
                    self._rootCell = target
                    self._preSuspicious.extend(self.getNeighbors(x, y))
                elif len(self._streak) == 2 and self._direction is None:
                    if self._streak[0][0] == x:
                        self._direction = (0, 1 if self._streak[1][1] > self._streak[0][1] else -1)
                        self._directionMode = "forward"
                    elif self._streak[0][1] == y:
                        self._direction = (1 if self._streak[1][0] > self._streak[0][0] else -1, 0)
                        self._directionMode = "forward"

                if self.isShipSunk(ship):
                    sunk_size = len(ship)
                    self._ships.remove(ship)
                    self._remainShips.remove(sunk_size)
                    self.resetTargeting()
                    return True, sunk_size
                return True, None

        self._board[x][y] = -1
        return False, None


    def huntMode(self):
        if self._direction:
            dx, dy = self._direction

            if self._directionMode == "forward":
                last_x, last_y = self._streak[-1]
                nx, ny = last_x + dx, last_y + dy
                if (nx, ny) in self._cells:
                    return self.checkTarget((nx, ny))
                else:
                    # chuyển sang bắn backward nếu forward hết ô
                    self._directionMode = "backward"

            if self._directionMode == "backward":
                first_x, first_y = self._streak[0]
                nx, ny = first_x - dx, first_y - dy
                if (nx, ny) in self._cells:
                    return self.checkTarget((nx, ny))
                else:
                    # không còn ô theo hướng, nhưng tàu chưa chắc đã chìm
                    # thử bắn các ô lân cận của các ô trong streak chưa bắn
                    neighbors = []
                    for (x, y) in self._streak:
                        neighbors.extend(self.getNeighbors(x, y))
                    neighbors = list(set(neighbors))  # loại trùng

                    # Loại bỏ những ô đã bắn hoặc không còn trong cells
                    neighbors = [pos for pos in neighbors if pos in self._cells]
                    if neighbors:
                        return self.checkTarget(neighbors[0])
                    else:
                        self.resetTargeting()
                        return self.randomMode()
        else:
            # Nếu chưa xác định hướng, bắn theo suspicious hoặc random
            if self._suspicious:
                return self.checkTarget(self._suspicious.pop(0))
            else:
                return self.randomMode()

    def getNeighbors(self, x, y):
        possible = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        return [p for p in possible if p in self._cells]
    def resetTargeting(self):
        self._direction = None
        self._directionMode = None
        self._streak.clear()
        self._suspicious.clear()
        self._preSuspicious.clear()
    def takeTurn(self):
        if self._direction or self._suspicious or self._streak:
            self._result =  self.huntMode()
        else:
            self._result = self.randomMode()
        if self._result is None:
            return False, None
        return self._result
if __name__ == "__main__":
    bot = Bot()
    for i in range(1, 100):
        hit, sunk = bot.takeTurn()
        print(f"Lượt {i}: {'Trúng!' if hit else 'Trượt!'}")
        if sunk:
            print(f"→ Tàu {sunk} ô đã chìm!")
