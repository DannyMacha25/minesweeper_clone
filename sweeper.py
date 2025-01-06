import random
import time
from enum import Enum

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Game:
    def __init__(self,difficulty=Difficulty.MEDIUM,startTime = 0) -> None:
        
        if difficulty == Difficulty.EASY:
            self.rows = 9
            self.cols = 9
            self.bombs = 10
        if difficulty == Difficulty.MEDIUM:
            self.rows = 16
            self.cols = 16
            self.bombs = 40
        if difficulty == Difficulty.HARD:
            self.rows = 16
            self.cols = 30
            self.bombs = 99

        self.active = False
        self.time = 0
        self.startTime = startTime
        self.tiles = (self.cols * self.rows) - self.bombs
        self.flags = 0
        self.tilesLeft =  self.tiles
        self.difficulty = difficulty
        self.isVictory = False
        self.tileMatrix = [[0 for x in range(self.rows)] for y in range(self.cols)]
        

class Tile:
    def __init__(self) -> None:
        self.isChecked = False
        self.isFlagged = False
    def flag(self):
        if self.isChecked != True:
            if self.isFlagged == False:
                self.isFlagged = True
            else:
                self.isFlagged = False
    def check(self):
        if self.isFlagged != True:
            if self.isChecked == False:
                self.isChecked = True
    def display(self):
        print("N")

class Mine(Tile):
    def check(self):
        super().check()
        self.explode()
        return self.type()
    def explode(self):
        print('Bomb exploded: TBI')
    def display(self):
        return 'b'
    def type(self):
        return -1

class Empty(Tile):
    def __init__(self) -> None:
        super().__init__()
        self.proximity = 0
    def display(self):
        return str(self.proximity)
    def type(self):
        return self.proximity
    def check(self):
        super().check()
        return self.type()

# Return a set of points(x,y)
def generateBombPositions(rows,cols,numBombs,pos):
    random.seed(time.time)
    bombPoses = set()
    noBombsSet = set()
    for x in range(-1,2,1):
        for y in range(-1,2,1):
            noBombsSet.add((pos[1] + x,pos[0] + y))

    for x in range(numBombs):
        newPoint = (random.randint(0,rows),random.randint(0,cols))
        if newPoint in noBombsSet:
            x = x - 1
        else:
            if newPoint in bombPoses:
                x = x - 1
            else:
                print(newPoint)
                print(x)
                bombPoses.add(newPoint)
    
    return bombPoses
    
# Fills out the given matrix with empty tiles
def populateEmptyTiles(matrix,rows,cols):
    for x in range(cols):
        for y in range (rows):
            newTile = Empty()
            matrix[x][y] = newTile
            newTile.proximity = 0
# Fills out the given matrix with the proper tiles    
def populateTiles(matrix,rows,cols,bombPoses):
    # Iterate through matrix
    for x in range(cols):
        for y in range (rows):
            # Initialize Point
            point = (y,x)
            # Place Bomb
            if point in bombPoses:
                matrix[x][y] = Mine()
            # Place Empty tile, give it a proper proximity
            else:
                newTile = Empty()
                matrix[x][y] = newTile
                newTile.proximity = calculateProximity(y,x,rows,cols,bombPoses)

    
# Returns a proximity number based on number of bombs surrounding the position
def calculateProximity(x,y,rows,cols,bombPoses):
    proxim = 0;
    # Top Left
    if x - 1 != -1 and y - 1 != -1:
        if (x-1,y-1) in bombPoses:
            proxim = proxim + 1
    # Top Mid
    if y - 1 != -1:
        if(x,y-1) in bombPoses:
            proxim = proxim + 1
    # Top Right
    if x + 1 <= rows - 1 and y - 1 != -1:
        if(x+1,y-1) in bombPoses:
            proxim = proxim + 1
    # Left
    if x - 1 != -1:
        if(x-1,y) in bombPoses:
            proxim = proxim + 1
    # Right
    if x + 1 <= rows - 1:
        if(x+1,y) in bombPoses:
            proxim = proxim + 1
    # Bot Left
    if x - 1 != -1 and y + 1 <= cols - 1:
        if(x-1,y+1) in bombPoses:
            proxim = proxim + 1
    # Bot Mid
    if y + 1 <= cols - 1:
        if(x,y+1) in bombPoses:
            proxim = proxim + 1
    # Bot Right
    if x + 1 <= rows - 1 and y + 1 <= cols - 1:
        if(x+1,y+1) in bombPoses:
            proxim = proxim + 1
    
    return proxim
