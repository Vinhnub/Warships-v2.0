import random

class Bot:
    def __init__(self, BOARD_SIZE=10):
        self._BOARD_SIZE = BOARD_SIZE
        self._board = [[0 for _ in range(self._BOARD_SIZE)] for _ in range(self._BOARD_SIZE)]
        self._cells = [(x, y) for x in range(self._BOARD_SIZE) for y in range(self._BOARD_SIZE)]  # ô chưa bắn
        self._ships = ships = [
                                [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
                                [(2, 2), (3, 2), (4, 2), (5, 2)],
                                [(7, 0), (7, 1), (7, 2)],
                                [(5, 5), (6, 5)],
                                [(9, 9)]]
        self._turnCount = 0
        self._preSuspiciousCells = []
        self._suspiciousCells = []  # lưu các ô nghi ngờ quanh ô vừa trúng nếu k có thì random
        self._remainShips = [1, 2, 3, 4, 5]
        self._streak = []
        self._direction = None


    def secondBoard(self):
        # Tạo bảng đánh giá khả năng có tàu
        secondBoard = [[0 for _ in range(self._BOARD_SIZE)] for _ in range(self._BOARD_SIZE)]
        # Ngang
        for shipSize in self._remainShips:
            for x in range(self._BOARD_SIZE):
                for y in range(self._BOARD_SIZE - shipSize + 1):
                    positions = [(x, y+i) for i in range(shipSize)]
                    if all(self._board[posx][posy] == 0 for posx, posy in positions):
                        for posx, posy in positions:
                            secondBoard[posx][posy] += 1
        # Dọc
        for shipSize in self._remainShips:
            for y in range(self._BOARD_SIZE):
                for x in range(self._BOARD_SIZE - shipSize + 1):
                    positionsAlign = [(x+i, y) for i in range(shipSize)]
                    if all(self._board[posx][posy] == 0 for posx, posy in positionsAlign):
                        for posx, posy in positionsAlign:
                            secondBoard[posx][posy] += 1
        return secondBoard

    def randomMode(self):
        target = random.choice(self._cells)
        self._turnCount += 1
        return self.checkTarget(target)

    def checkTarget(self, target):
        if target in self._cells:
            self._cells.remove(target)  # xóa ô vừa bắn
        x, y = target
        for ship in self._ships:
            for pos in ship:
                if x == pos[0] and y == pos[1]:
                    self._board[x][y] = 1
                    if len(self._streak) == 0: 
                        self._preSuspiciousCells.extend(self.getNeighbors(x, y))
                    elif len(self._streak) == 1:
                        if self._streak[0][0] == x:
                            self._suspiciousCells = [cell for cell in self._preSuspiciousCells if cell[0] == x]
                            self._direction = (0, 1)
                        elif self._streak[0][1] == y:
                            self._suspiciousCells = [cell for cell in self._preSuspiciousCells if cell[1] == y]
                            self._direction = (1, 0)
                    if self.isShipSunk(ship):
                       print(f"  → Tàu kích thước {len(ship)} đã chìm!")
                       self._ships.remove(ship)
                       self._remainShips.remove(len(ship))
                    self._streak.append(target)
                    return True
        self._board[x][y] = -1
        return False

    def getNeighbors(self, x, y):
        targetRange = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
        validTargets = [i for i in targetRange if i in self._cells] 
        return validTargets

    def chooseTargetMode(self):
        self._turnCount += 1
        EstimazeBoard = self.secondBoard()
        self._preSuspiciousCells = [pos for pos in self._preSuspiciousCells if pos in self._cells]

        if self._preSuspiciousCells:  # truy tìm tàu vẫn dựa trên trọng số chứ chưa tự đoán được tàu nằm hướng nào để bắn
            maxValue = max(EstimazeBoard[x][y] for (x, y) in self._preSuspiciousCells)
            bestCells = [(x, y) for (x, y) in self._preSuspiciousCells if EstimazeBoard[x][y] == maxValue]
            if bestCells:
                target = random.choice(bestCells)
                return self.checkTarget(target)
            else:
                return self.randomMode()
        else:  # tìm tàu mới
            maxValue = max(max(row) for row in EstimazeBoard)
            bestCells = [(x, y) for x in range(self._BOARD_SIZE)
                         for y in range(self._BOARD_SIZE)
                         if EstimazeBoard[x][y] == maxValue and (x, y) in self._cells]
            if bestCells:
                target = random.choice(bestCells)
                return self.checkTarget(target)
            else:
                return self.randomMode()

    def takeTurn(self):
        if self._suspiciousCells:
            return self.HuntMode(self._suspiciousCells)
        elif self._preSuspiciousCells :
            return self.chooseTargetMode()
        else:
            return self.randomMode()
        
    def isHit(self, coord):
        """Trả về True nếu bắn trúng tàu, False nếu trượt."""
        x, y = coord
        for ship in self._ships:
            if coord in ship:
               return True
        return False
      
    def HuntMode(self, targets):
        left = targets[0]
        right = targets[1]
        if self.isHit(left):
            x, y = self._streak[-1]  # ô trúng gần nhất
            if self._direction == (0,1):
               dx, dy = self._direction  # hướng hiện tại
               nx, ny = x - dx, y - dy 
            if (nx, ny) not in self._cells:
                dx, dy = -dx, -dy
                nx, ny = x + dx, y + dy
                if (nx, ny) not in self._cells:
                    if dx == 0:  # đang bắn ngang đổi sang dọc
                        self._direction = (1, 0)
                    else: 
                        self._direction = (0, 1)
                    nx, ny = self._streak[0][0] + self._direction[0], self._streak[0][1] + self._direction[1]
        self._suspiciousCells.append((nx, ny))
        return self.checkTarget(self._suspiciousCells[0])
    
    def isShipSunk(self, ship):
        return all(self._board[x][y] == 1 for x, y in ship)

# Tạo bot
bot = Bot(BOARD_SIZE=10)

# Chạy game cho đến khi bắn hết tất cả các tàu
while bot._ships:  # còn tàu
    hit = bot.takeTurn()  # bot bắn 1 lượt
    if hit:
        print(f"Lượt {bot._turnCount}: Trúng!")
        # Kiểm tra xem có tàu nào bị bắn hết chưa
        bot._ships = [ship for ship in bot._ships if not all(pos not in bot._cells and bot._board[pos[0]][pos[1]] == 1 for pos in ship)]
    else:
        print(f"Lượt {bot._turnCount}: Trượt!")
# Kết thúc
print("Tất cả tàu đã bị bắn hạ!")
print("Tổng số lượt:", bot._turnCount)
