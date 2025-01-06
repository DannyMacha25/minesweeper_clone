from sweeper import *

def main():
    bombs = generateBombPositions(10,10,8)
    Matrix = [[0 for x in range(10)] for y in range(10)] 
    populateTiles(Matrix,10,10,bombs)
    displayString = ''
    for x in range(10):
        for y in range(10):
            displayString = displayString + Matrix[x][y].display() + ' '
        displayString = displayString + '\n'
    print(displayString)
            

if __name__ == '__main__':
    main()