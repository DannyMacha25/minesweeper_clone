import pygame
BLANK_TILE = 'sprites/complete_sprites/blank_tile.png'
FLAGGED_TILE = 'sprites/complete_sprites/flagged_tile.png'
BOMB = 'sprites/complete_sprites/bomb.png'
BLANK_CHECKED = 'sprites/complete_sprites/pushed_blank_tile.png'
ONE = 'sprites/complete_sprites/one.png'
TWO = 'sprites/complete_sprites/two.png'
THREE = 'sprites/complete_sprites/three.png'
FOUR = 'sprites/complete_sprites/four.png'
FIVE = 'sprites/complete_sprites/five.png'
SIX = 'sprites/complete_sprites/six.png'
SEVEN = 'sprites/complete_sprites/seven.png'
EIGHT = 'sprites/complete_sprites/eight.png'
class SweeperGameTile:
    def __init__(self,pos = (0,0),size=0,tile=None):
        self.position = pos
        self.size = size
        self.sprite = pygame.image.load(BLANK_TILE).convert()
        self.uncheckedSprite = None
        self.tile = tile
        #Debug
        self.rect = pygame.Rect(pos[0],pos[1],size,size)
        self.color = (0,0,0)
        if self.tile.type() == -1:
            self.color = (255,0,0)
        else:
            self.color = (0,255,0)
    def updateSprite(self):
        if self.tile.isChecked == False:
            if self.tile.isFlagged == True:
                self.sprite = pygame.image.load(FLAGGED_TILE)
            else:
                self.sprite = pygame.image.load(BLANK_TILE)
        else:
            #TO CHANGE
            self.sprite = numberSprite(self.tile.type())
        

def numberSprite(num):
    if num == 0:
        return pygame.image.load(BLANK_CHECKED)
    if num == 1:
        return pygame.image.load(ONE)      
    if num == 2:
        return pygame.image.load(TWO)
    if num == 3:
        return pygame.image.load(THREE)
    if num == 4:
        return pygame.image.load(FOUR)  
    if num == 5:
        return pygame.image.load(FIVE) 
    if num == 6:
        return pygame.image.load(SIX) 
    if num == 7:
        return pygame.image.load(SEVEN) 
    if num == 8:
        return pygame.image.load(EIGHT) 
    if num == -1:
        return pygame.image.load(BOMB) 



        