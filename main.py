import pygame
from sweeper import *
from pygame_sweeper import *


# Todo:
# Setup a grid of whatever chosing
# Tiles in the grid with their own sprites (maybe make an object type?)
# When you hover over the tiles, change sprite
# Click the sprite to reveal the number or bomb

# Later
# 

INPUT_BUFFER_TIME = 200 #ms
def main():
    
    #Pygame Setup
    pygame.init()
    font = pygame.font.SysFont("Arial" , 18 , bold = True)
    clock = pygame.time.Clock()
    #Window settings
    pygame.display.set_caption("Pysweeper")

    screen = pygame.display.set_mode((800,600))
    running = True
    
    #Game Setup
    levelSelect = 2
    level = Difficulty.MEDIUM
    firstTurn = True
    tileSize = 12

    startPos = (150,80)
    if level == Difficulty.EASY:
        tileSize = 52
        startPos = (90,100)
    if level == Difficulty.MEDIUM:
        tileSize = 26
    if level == Difficulty.HARD:
        startPos = (10,70)
        tileSize = 26 #easy = 52, medium = 26, hard  =

    game = Game(level)

    #Starting First Game
    populateEmptyTiles(game.tileMatrix,game.rows,game.cols)
    gameTileMatrix = [[0 for x in range(game.rows)] for y in range(game.cols)]
    populateGameTiles(game.rows,game.cols,gameTileMatrix,game.tileMatrix,startPos,tileSize)
    drawTileMatrix(game.rows,game.cols,gameTileMatrix,tileSize,screen)
    #Input Buffer Logic
    timeAtBuffer = 0
    currTime = 0
    prevPoint = None
    #Game loop
    while running:
        clock.tick()

        keyDown = None
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keyDown = event.key
        currTime = pygame.time.get_ticks()
        point = getTileOnMouse(game.rows,game.cols,startPos,tileSize)
        if game.active == True or firstTurn == True:
            
            game.time = currTime - game.startTime
            # Get and handle input
            mouseEvent = pygame.mouse.get_pressed(num_buttons=3)
            if(mouseEvent != (False,False,False) and point != None):
                if(currTime - timeAtBuffer > INPUT_BUFFER_TIME):
                    #Clear Board
                    rect = pygame.Rect(0,0,800,600)
                    pygame.draw.rect(screen,pygame.Color(0,0,0),rect)
                    timeAtBuffer = pygame.time.get_ticks()
                    if firstTurn:
                        startPos = (150,80)
                        if level == Difficulty.EASY:
                            tileSize = 52
                            startPos = (90,100)
                        if level == Difficulty.MEDIUM:
                            tileSize = 26
                            startPos = (150,80)
                        if level == Difficulty.HARD:
                            startPos = (10,70)
                            tileSize = 26 
                        game.startTime = currTime
                        game.active = True
                        firstTurn = False
                        #Start Game
                        populateTiles(game.tileMatrix,game.rows,game.cols,generateBombPositions(game.rows,game.cols,game.bombs,point))
                        populateGameTiles(game.rows,game.cols,gameTileMatrix,game.tileMatrix,startPos,tileSize)
                        tileType = handleMouseClick(gameTileMatrix[point[0]][point[1]],mouseEvent)
                        if(tileType != None):
                            if(tileType != -1):
                                tilesChecked = set()
                                massTileCheck(game.rows,game.cols,point,True,gameTileMatrix,tilesChecked,game)
                        drawTileMatrix(game.rows,game.cols,gameTileMatrix,tileSize,screen)
                    else:
                        tileType = handleMouseClick(gameTileMatrix[point[0]][point[1]],mouseEvent)
                        if(tileType != None):
                            if(tileType != -1):
                                tilesChecked = set()
                                massTileCheck(game.rows,game.cols,point,True,gameTileMatrix,tilesChecked,game)
                                if game.tilesLeft <= 0:
                                    game.active = False
                                    game.isVictory = True
                            else:
                                game.active = False
                        drawTileMatrix(game.rows,game.cols,gameTileMatrix,tileSize,screen)
            if keyDown == pygame.K_r:
                game = Game(level,currTime)
                populateEmptyTiles(game.tileMatrix,game.rows,game.cols)
                gameTileMatrix = [[0 for x in range(game.rows)] for y in range(game.cols)]
                populateGameTiles(game.rows,game.cols,gameTileMatrix,game.tileMatrix,startPos,tileSize)
                firstTurn = True
                drawTileMatrix(game.rows,game.cols,gameTileMatrix,tileSize,screen)
        else:
            #Tell Player they lost
            #Restart Prompt
            if keyDown == pygame.K_r:
                game = Game(level,currTime)
                populateEmptyTiles(game.tileMatrix,game.rows,game.cols)
                gameTileMatrix = [[0 for x in range(game.rows)] for y in range(game.cols)]
                populateGameTiles(game.rows,game.cols,gameTileMatrix,game.tileMatrix,startPos,tileSize)
                firstTurn = True
                drawTileMatrix(game.rows,game.cols,gameTileMatrix,tileSize,screen)

        displayDifficulty(levelSelect,font,screen)
        #fps_counter(clock,font,screen)
        if keyDown == pygame.K_UP:
            levelSelect += 1
            if levelSelect > 3:
                levelSelect = 1
            rect = pygame.Rect(0,0,800,600)
            pygame.draw.rect(screen,pygame.Color(0,0,0),rect)
            level = Difficulty(levelSelect)
            if level == Difficulty.EASY:
                tileSize = 52
                startPos = (90,100)
            if level == Difficulty.MEDIUM:
                tileSize = 26
                startPos = (150,80)
            if level == Difficulty.HARD:
                startPos = (10,70)
                tileSize = 26
            game = Game(level,currTime)
            populateEmptyTiles(game.tileMatrix,game.rows,game.cols)
            gameTileMatrix = [[0 for x in range(game.rows)] for y in range(game.cols)]
            populateGameTiles(game.rows,game.cols,gameTileMatrix,game.tileMatrix,startPos,tileSize)
            firstTurn = True
            drawTileMatrix(game.rows,game.cols,gameTileMatrix,tileSize,screen)
            point = (0,0)
            prevPoint = (0,0)
        if keyDown == pygame.K_DOWN:
            levelSelect -= 1
            if levelSelect < 1:
                levelSelect = 3
            rect = pygame.Rect(0,0,800,600)
            pygame.draw.rect(screen,pygame.Color(0,0,0),rect)
            level = Difficulty(levelSelect)
            if level == Difficulty.EASY:
                tileSize = 52
                startPos = (90,100)
            if level == Difficulty.MEDIUM:
                tileSize = 26
                startPos = (150,80)
            if level == Difficulty.HARD:
                startPos = (10,70)
                tileSize = 26
            game = Game(level,currTime)
            populateEmptyTiles(game.tileMatrix,game.rows,game.cols)
            gameTileMatrix = [[0 for x in range(game.rows)] for y in range(game.cols)]
            populateGameTiles(game.rows,game.cols,gameTileMatrix,game.tileMatrix,startPos,tileSize)
            firstTurn = True
            drawTileMatrix(game.rows,game.cols,gameTileMatrix,tileSize,screen)
            point = (0,0)
            prevPoint = (0,0)
        if game.active == True:
            timeCounter(game.time,font,screen)
        else:
            timeCounter(game.time,font,screen)
            displayText('You Won!',(6000,600),font,screen)
        if(point != None):
            if(point[0] <= game.cols):  
                drawSelectBorder(gameTileMatrix[point[0]][point[1]],screen)
                if(prevPoint != point and prevPoint != None):
                    drawTile(gameTileMatrix[prevPoint[0]][prevPoint[1]],tileSize,screen)
                    prevPoint = point
                prevPoint = point
        pygame.display.flip()

def drawTile(tile,size,window):
    sprite = tile.sprite
    pos = tile.position
    scale = size / 26
    sprite_scaled = pygame.transform.scale(sprite,(26*scale,26*scale))
    #pygame.draw.rect(window,gameTileMatrix[x][y].color,gameTileMatrix[x][y].rect)
    window.blit(sprite_scaled,pos)


#Checks Tiles
def massTileCheck(rows,cols,pos,isFirst,matrix,checkedTiles,game):
    x = pos[0]
    y = pos[1]

    if (x,y) in checkedTiles:
        return
    checkedTiles.add((x,y))
    tileType = matrix[x][y].tile.type()

    if tileType != 0:
        if tileType != -1:
            matrix[x][y].tile.check()
            game.tilesLeft -= 1
            print(game.tiles-game.tilesLeft)
        return 
    if not isFirst and matrix[x][y].tile.isChecked == True:
        return 
    matrix[x][y].tile.check()
    game.tilesLeft -= 1
    print(game.tiles-game.tilesLeft)
        
    #Top Left
    if x - 1 != -1 and y - 1 != -1:
        massTileCheck(rows,cols,(x-1,y-1),tileType,matrix,checkedTiles,game)
    # Top Mid
    if y - 1 != -1:
        massTileCheck(rows,cols,(x,y-1),tileType,matrix,checkedTiles,game)
    # Top Right
    if x + 1 < cols - 1 and y - 1 != -1:
        massTileCheck(rows,cols,(x+1,y-1),tileType,matrix,checkedTiles,game)
    # Left
    if x - 1 != -1:
        massTileCheck(rows,cols,(x-1,y),tileType,matrix,checkedTiles,game)
    # Right
    if x + 1 <= cols - 1:
        massTileCheck(rows,cols,(x+1,y),tileType,matrix,checkedTiles,game)
    # Bot Left
    if x - 1 != -1 and y + 1 <= rows - 1:
        massTileCheck(rows,cols,(x-1,y+1),tileType,matrix,checkedTiles,game)
    # Bot Mid
    if y + 1 <= rows - 1:
        massTileCheck(rows,cols,(x,y+1),tileType,matrix,checkedTiles,game)
    # Bot Right
    if x + 1 <= cols - 1 and y + 1 <= rows - 1:
        massTileCheck(rows,cols,(x+1,y+1),tileType,matrix,checkedTiles,game)
    return
    
# Need to add size and support for tilematrix
# Returns which tile in the matrix the mouse is currently hovering over
def getTileOnMouse(rows,cols,initialPos,size):
    mousePos = pygame.mouse.get_pos()
    for x in range(cols):
        for y in range(rows):
            topLeftOfTile = (initialPos[0]+(size*x), initialPos[1] + (size * y))        
            if((mousePos[0] >= topLeftOfTile[0] and mousePos[0] <= topLeftOfTile[0] + size) and
            (mousePos[1] >= topLeftOfTile[1] and mousePos[1] <= topLeftOfTile[1] + size )):
                return(x,y)           

# Deprecated Lol
def populateSpriteMatrix(rows,cols,spriteMatrix):
    topLeft = (30,30)
    for x in range(rows):
        for y in range(cols):
            rect = pygame.Rect(80 + (40 * x), 80 + (40 * y), 40, 40)
            spriteMatrix[x][y] = rect

# Draws the sprite matrix
def drawSpriteMatrix(rows,cols,spriteMatrix,window):
    color = (255,0,0)
    for x in range(rows):
        for y in range(cols):
            pygame.draw.rect(window,color,spriteMatrix[x][y])
def drawTileMatrix(rows,cols,gameTileMatrix,size,window):
    for x in range(cols):
        for y in range(rows):
            gameTileMatrix[x][y].updateSprite()
            sprite = gameTileMatrix[x][y].sprite
            pos = gameTileMatrix[x][y].position
            scale = size / 26
            sprite_scaled = pygame.transform.scale(sprite,(26*scale,26*scale))
            #pygame.draw.rect(window,gameTileMatrix[x][y].color,gameTileMatrix[x][y].rect)
            window.blit(sprite_scaled,pos)

# Populates a matrix of Game Tile Objects
def populateGameTiles(rows,cols,gameTileMatrix,tileMatrix,initialPos,size):
    for x in range(cols):
        for y in range(rows):
            pos = (initialPos[0] + (size * x), initialPos[1] + (size * y))
            tile = Tile()
            gameTileMatrix[x][y] = SweeperGameTile(pos,size,tileMatrix[x][y])

def drawSelectBorder(tile,window):
    pygame.draw.rect(window,(50,50,50),tile.rect,2)

def handleMouseClick(tile,mouse):
    if (mouse == (False,False,True)):
        tile.tile.flag()
        return None
    if(mouse == (True,False,False)):
        return tile.tile.check()
        
def fps_counter(clock,font,window):
    rect = pygame.Rect(0,0,30,30)
    pygame.draw.rect(window,pygame.Color(0,0,0),rect)
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps ,3, pygame.Color("RED"))
    window.blit(fps_t,(0,0))

def displayDifficulty(level,font,window):
    rect = pygame.Rect(400,0,180,30)
    pygame.draw.rect(window,pygame.Color(0,0,0),rect)
    diff = "e"
    if level == 1:
        diff = "Easy"
    if level == 2:
        diff = "Medium"
    if level == 3:
        diff = "Hard"
    difficulty_str = "Difficulty: {0}".format(diff)
    difficulty_t = font.render(difficulty_str,5,pygame.Color("RED"))
    window.blit(difficulty_t,(400,0))
def timeCounter(time,font,window):
    time = int(time/1000)
    rect = pygame.Rect(200,0,80,30)
    pygame.draw.rect(window,pygame.Color(0,0,0),rect)
    time_str = "Time : {0}".format(time)
    time_t = font.render(time_str ,5, pygame.Color("RED"))
    window.blit(time_t,(200,0))
def displayText(text,pos,font,window):
    rect = pygame.Rect(pos[0],pos[1],80,30)
    pygame.draw.rect(window,pygame.Color(0,0,0),rect)
    text_t = font.render(text,5, pygame.Color("RED"))
    window.blit(text_t,(pos[0],pos[1]))

if __name__ == '__main__':
    main()
