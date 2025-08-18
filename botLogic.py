import random
class BotLogic:
    def __init__(self, enemyListShip, BOARD_SIZE=10):
        self._BOARD_SIZE = BOARD_SIZE
        self._board = [[0] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]
        self._cells = [(y, x) for y in range(self._BOARD_SIZE) for x in range(self._BOARD_SIZE)]
        self._turnCount = 0
        self._preSuspicious = []
        self._suspicious = []
        self._streak = []
        self._direction = None
        self._directionMode = None  # forward / backward
        self._rootCell = None
        self._ships = [5,4,3,3,2]
        self._result = None
        self.enemyListShip = enemyListShip
        self._remainShips = [5,4,3,3,2]
        self._remainShips2 = [5,4,3,3,2]
        self._contributions = None
    def secondBoard(self, ReCheck=False):
        if not ReCheck:
           remainShips = self._remainShips
        elif ReCheck:
           remainShips = self._remainShips2
        contributions = {shipSize: 0 for shipSize in remainShips}
        secondBoard = [[0] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]
        for shipSize in remainShips:

            # Ngang
            for y in range(self._BOARD_SIZE):
                for x in range(self._BOARD_SIZE - shipSize + 1):
                    positions = [(y, x + i) for i in range(shipSize)]
                    if all(self._board[py][px] == 0 for py, px in positions):
                        for py, px in positions:
                            secondBoard[py][px] += 1
                            contributions[shipSize] += 1

            # Dọc
            for x in range(self._BOARD_SIZE):
                for y in range(self._BOARD_SIZE - shipSize + 1):
                    positions = [(y + i, x) for i in range(shipSize)]
                    if all(self._board[py][px] == 0 for py, px in positions):
                        for py, px in positions:
                            secondBoard[py][px] += 1
                            contributions[shipSize] += 1
        if ReCheck:
            self._contributions = contributions
            return secondBoard, self._contributions
        return secondBoard
    
    def pickTargetLeastLikelyShip(self):
        secondboard, contributions = self.secondBoard(True)
        target_ship = min(contributions, key=contributions.get)
        # Gom tất cả vị trí hợp lệ của tàu đó
        positions_list = []
        for y in range(self._BOARD_SIZE):
            for x in range(self._BOARD_SIZE - target_ship + 1):
                pos = [(y, x+i) for i in range(target_ship)]
                if all(self._board[py][px] == 0 for py, px in pos):
                    positions_list.append(pos)
        for x in range(self._BOARD_SIZE):
            for y in range(self._BOARD_SIZE - target_ship + 1):
                pos = [(y+i, x) for i in range(target_ship)]
                if all(self._board[py][px] == 0 for py, px in pos):
                    positions_list.append(pos)
        if len(positions_list) == 0:
            self._remainShips2.remove(target_ship)
            if self._cells:
                return random.choice(self._cells), target_ship
            else:
                return None, target_ship
        candidate_cells = [pos[len(pos)//2] for pos in positions_list]
        if candidate_cells:
            best_cell = max(candidate_cells, key=lambda cell: secondboard[cell[0]][cell[1]])
            return best_cell, target_ship

        return None, target_ship

    def randomMode(self, ReCheck=False):
        if not ReCheck:
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
            
        elif ReCheck:
            target, shipMin = self.pickTargetLeastLikelyShip()
            if target is None and self._cells:
                target = random.choice(self._cells)
            return self.checkTarget(target)

    def checkTarget(self, target):
        if target not in self._cells or target is None:
            return 0, None
        shipSunk = []
        y, x = target
        self._cells.remove(target)
        self._turnCount += 1

        if self.enemyListShip[y][x]:  # trúng tàu
            self._board[y][x] = 1
            if self._directionMode == "backward":
                self._streak.insert(0, target)
            else:
                self._streak.append(target)

            # Cập nhật direction
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
            # Nếu streak dài bằng hoặc lớn hơn tàu còn lại, loại bỏ tàu lớn nhất
            return 1, (y, x)
        else:  # trượt
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
                    self._GuestShip += 1                        
            if self._directionMode == "backward":
                first_y, first_x = self._streak[0]
                ny, nx = first_y - dy, first_x - dx
                if (ny, nx) in self._cells:
                    return self.checkTarget((ny, nx))
                else:

                    ship_length = len(self._streak)
                    if ship_length in self._remainShips:
                        self._remainShips.remove(ship_length)
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

    def takeTurn(self):
        condition = self._direction or self._preSuspicious or self._streak
        if self._turnCount >= 25 and len(self._streak) == 0:
            self._result = self.randomMode(True)
        elif condition:
            self._result = self.huntMode()
        else:
            self._result = self.randomMode()
        return self._result
