import random

class Bot:
    def __init__(self, BOARD_SIZE=10):
        self._BOARD_SIZE = BOARD_SIZE
        self._board = [[0 for _ in range(self._BOARD_SIZE)] for _ in range(self._BOARD_SIZE)]
        self._cells = [(x, y) for x in range(self._BOARD_SIZE) for y in range(self._BOARD_SIZE)]  # ô chưa bắn
        self._turnCount = 0
        self._preSuspiciousCells = []
        self._suspiciousCells = []  # lưu các ô nghi ngờ quanh ô vừa trúng nếu k có thì random
        self._remainShips = [1, 2, 3, 4, 5]
        self._streak = []

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
        for ship in ships:
            for pos in ship:
                if x == pos[0] and y == pos[1]:
                    self.board[x][y] = 1
                    for i in self.getNeighbors(x, y):
                        self._suspiciousCells.append(i)
                    self._streak.append(target)
                    if len(self._streak) == 2:
                        self.checkStreak() 
                    return True
        self.board[x][y] = -1
        return False

    def getNeighbors(self, x, y):
        targetRange = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
        validTargets = [i for i in targetRange if i in self._cells] 
        return validTargets

    def chooseTargetMode(self):
        self._turnCount += 1
        EstimazeBoard = self.secondBoard()
        self._suspiciousCells = [pos for pos in self._suspiciousCells if pos in self._cells]

        if self._suspiciousCells:  # truy tìm tàu vẫn dựa trên trọng số chứ chưa tự đoán được tàu nằm hướng nào để bắn
            maxValue = max(EstimazeBoard[x][y] for (x, y) in self._suspiciousCells)
            bestCells = [(x, y) for (x, y) in self._suspiciousCells if EstimazeBoard[x][y] == maxValue]
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
            return self.chooseTargetMode()
        else:
            return self.randomMode()
        
    def checkStreak(self):
        if self._streak[0][0] == self._streak[1][0]:
            self._suspiciousCells = self._suspiciousCells[2]
            self.hitHorizon()
        elif self._streak[0][1] == self._streak[1][1]:
            self._suspiciousCells = self._suspiciousCells[3]
            self.hitVertical()
    def hitHorizon(self,target):
        if self.checkTarget(target):
            self._suspiciousCells = self._suspiciousCells[2]
    def hitVertical(self, target):
        if self.checkTarget(target):
            self._suspiciousCells = self._suspiciousCells[3]
    def checkShips(self):
        for ship in ships:
            if all(self._board[posx][posy] == 1 for posx, posy in ship ):
                
ships = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    [(2, 2), (3, 2), (4, 2), (5, 2)],
    [(7, 0), (7, 1), (7, 2)],
    [(5, 5), (6, 5)],
    [(9, 9)]
]