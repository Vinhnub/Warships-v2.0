import random
class BotLogic:
    def __init__(self, BOARD_SIZE=10):
        self._BOARD_SIZE = BOARD_SIZE
        self._board = [[0] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]
        self._cells = [(y, x) for y in range(self._BOARD_SIZE) for x in range(self._BOARD_SIZE)]

        self._turnCount = 0
        self._preSuspicious = []
        self._suspicious = []
        self._streak = []
        self._direction = None
        self._directionMode = None  # forward / backward
        self._remainShips = []
        self._rootCell = None
        self._ships = []
        self._result = None
        self.enemyListShip = None
    def set_enemy_player(self, enemy_player):
        self.enemyListShip = enemy_player.getListPosShip()

    def secondBoard(self):
        secondBoard = [[0] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]
        for shipSize in self._remainShips:
            # Ngang
            for y in range(self._BOARD_SIZE):
                for x in range(self._BOARD_SIZE - shipSize + 1):
                    positions = [(y, x + i) for i in range(shipSize)]
                    if all(self._board[py][px] == 0 for py, px in positions):
                        for py, px in positions:
                            secondBoard[py][px] += 1
            # Dọc
            for x in range(self._BOARD_SIZE):
                for y in range(self._BOARD_SIZE - shipSize + 1):
                    positions = [(y + i, x) for i in range(shipSize)]
                    if all(self._board[py][px] == 0 for py, px in positions):
                        for py, px in positions:
                            secondBoard[py][px] += 1
        return secondBoard

    def randomMode(self):
        EstimazeBoard = self.secondBoard()
        self._preSuspicious = [pos for pos in self._preSuspicious if pos in self._cells]

        if self._preSuspicious:
            maxValue = max(EstimazeBoard[py][px] for (py, px) in self._preSuspicious)
            bestCells = [(py, px) for (py, px) in self._preSuspicious if EstimazeBoard[py][px] == maxValue]
        else:
            maxValue = max(max(row) for row in EstimazeBoard)
            bestCells = [(y, x) for y in range(self._BOARD_SIZE)
                         for x in range(self._BOARD_SIZE)
                         if EstimazeBoard[y][x] == maxValue and (y, x) in self._cells]

        if bestCells:
            return self.checkTarget(random.choice(bestCells))
        elif self._cells:
            return self.checkTarget(random.choice(self._cells))
        else:
            return False, None

    def checkTarget(self, target):
        if target not in self._cells:
            return 0, None

        print(f"Bot bắn ô: {target}")
        self._cells.remove(target)
        self._turnCount += 1
        y, x = target

        for ship in list(self._ships):
            if target in ship:
                self._board[y][x] = 1
                if self._directionMode == "backward":
                    self._streak.insert(0, target)
                else:
                    self._streak.append(target)
                if len(self._streak) == 1:
                    self._rootCell = target
                    self._preSuspicious.extend(self.getNeighbors(y, x))
                elif len(self._streak) == 2 and self._direction is None:
                    if self._streak[0][0] == y:
                        self._direction = (0, 1 if self._streak[1][1] > self._streak[0][1] else -1)
                        self._directionMode = "forward"
                    elif self._streak[0][1] == x:
                        self._direction = (1 if self._streak[1][0] > self._streak[0][0] else -1, 0)
                        self._directionMode = "forward"

                if self.isShipSunk(ship):
                    sunk_size = len(ship)
                    self._ships.remove(ship)
                    self._remainShips.remove(sunk_size)
                    self.resetTargeting()
                    return True, (y,x)
                return 1, (y, x)
        self._board[y][x] = -1
        return 0, (y, x)

    def huntMode(self):
        if self._direction:
            dy, dx = self._direction
            if self._directionMode == "forward":
                last_y, last_x = self._streak[-1]
                ny, nx = last_y + dy, last_x + dx
                if (ny, nx) in self._cells:
                    return self.checkTarget((ny, nx))
                else:
                    self._directionMode = "backward"

            if self._directionMode == "backward":
                first_y, first_x = self._streak[0]
                ny, nx = first_y - dy, first_x - dx
                if (ny, nx) in self._cells:
                    return self.checkTarget((ny, nx))
                else:
                    neighbors = []
                    for (y, x) in self._streak:
                        neighbors.extend(self.getNeighbors(y, x))
                    neighbors = list(set(neighbors))
                    neighbors = [pos for pos in neighbors if pos in self._cells]
                    if neighbors:
                        return self.checkTarget(neighbors[0])
                    else:
                        self.resetTargeting()
                        return self.randomMode()
        else:
            return self.randomMode()

    def getNeighbors(self, y, x):
        possible = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        return [p for p in possible if p in self._cells]

    def resetTargeting(self):
        self._direction = None
        self._directionMode = None
        self._streak.clear()
        self._suspicious.clear()
        self._preSuspicious.clear()

    def isShipSunk(self, ship):
        return all(self._board[py][px] == 1 for (py, px) in ship)

    def takeTurn(self):
        if self._direction or self._preSuspicious or self._streak:
            self._result = self.huntMode()
        else:
            self._result = self.randomMode()
        return self._result
