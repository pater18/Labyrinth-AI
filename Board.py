import random
from matplotlib.pyplot import xscale
import pygame 
from BoardPiece import *
#from Labyrinth import DEFAULT_IMAGE_SIZE

BLUE    = (0,   0,   255)
GREEN   = (0,   255, 0  )
RED     = (255, 0,   0  )
GRAY    = (200, 200, 200)
LGRAY   = (150, 150, 150)
BLACK   = (0,   0,   0  ) 
BOARDSIZE = 7
DEFAULT_IMAGE_SIZE = (100,100)


def importAndScaleImage(path):
    
    Piece = pygame.image.load(os.path.join("images", "Corrected", path))
    Piece = pygame.transform.scale(Piece, DEFAULT_IMAGE_SIZE)
    return Piece 

pictures = {

    1 : importAndScaleImage("corner.png"), # corner
    2 : importAndScaleImage("straight.png"),
    3 : importAndScaleImage("1.png"),
    4 : importAndScaleImage("2.png"),
    5 : importAndScaleImage("3.png"),
    6 : importAndScaleImage("4.png"),
    7 : importAndScaleImage("5.png"),
    8 : importAndScaleImage("6.png"),
    9 : importAndScaleImage("7.png"),
    10 : importAndScaleImage("8.png"),
    11 : importAndScaleImage("9.png"),
    12 : importAndScaleImage("10.png"),
    13 : importAndScaleImage("11.png"),
    14 : importAndScaleImage("12.png"),

}



class Board:
    def __init__(self, height, width, DISPLAY) -> None:
        self.height = height
        self.width = width
        self.piecesList = [None] * 50 # Create an empty list
        self.display = DISPLAY
        self.constPieces()
        self.addPieces()
        self.drawBoard()
        self.drawValues()
        #self.writeIndex()
        
    def constPieces(self):
        y = 100
        x = 100

        self.piecesList[0] = BoardCornerPiece(x * 1, y * 1, 1)
        self.piecesList[2] = BoardTPiece(x * 3, y * 1, 2)
        self.piecesList[4] = BoardTPiece(x * 5, y * 1, 2)
        self.piecesList[6] = BoardCornerPiece(x * 7, y * 1,  2)
        self.piecesList[14] = BoardTPiece(x * 1, y * 3, 1)
        self.piecesList[16] = BoardTPiece(x * 3, y * 3, 1)
        self.piecesList[18] = BoardTPiece(x * 5, y * 3, 2)
        self.piecesList[20] = BoardTPiece(x * 7, y * 3, 3)
        self.piecesList[28] = BoardTPiece(x * 1, y * 5, 1)
        self.piecesList[30] = BoardTPiece(x * 3, y * 5, 0)
        self.piecesList[32] = BoardTPiece(x * 5, y * 5, 3)
        self.piecesList[34] = BoardTPiece(x * 7, y * 5, 3)
        self.piecesList[42] = BoardCornerPiece(x * 1, y * 7, 0)
        self.piecesList[44] = BoardTPiece(x * 3, y * 7, 0)
        self.piecesList[46] = BoardTPiece(x * 5, y * 7, 0)
        self.piecesList[48] = BoardCornerPiece(x * 7, y * 7, 3)

        # Add the extra piece to the next move
        self.piecesList[49] = BoardTPiece(0, 0, 0)


        


    def addPieces(self):
  
        xStart = 100
        yStart = 100

        for i in range(BOARDSIZE):
            for j in range (BOARDSIZE):
                index = j * BOARDSIZE + i
                if self.piecesList[index] == None: 
                    choice = random.randint(0, 2)
                    if choice == 0: 
                        self.piecesList[index] = BoardCornerPiece(xStart * (i + 1), yStart * (j + 1))
                    elif choice == 1:
                        self.piecesList[index] = BoardStraightPiece(xStart * (i + 1), yStart * (j + 1))
                    elif choice == 2: 
                        self.piecesList[index] = BoardTPiece(xStart * (i + 1), yStart * (j + 1))
        
        return self.piecesList
        
    def drawBoard(self):

        
        for piece in self.piecesList:
            if piece :
                for layout, color in piece.layout:
                    if color :
                        pygame.draw.rect(self.display, GREEN, layout)
                    elif not color :
                        pygame.draw.rect(self.display, RED, layout) 

        for x in range(7):
            for y in range(7):
                self.display.blit(pictures[random.randint(1,14)], ((x + 1) * 100, (y + 1) * 100 ))
         

    def drawValues(self): 
        
        font = pygame.font.SysFont('Comic Sans MS', 40)
        locations = []
        
        for i in range(0, 3):
            locations.append((240 + i * 200, 40))
        for i in range(0, 3):
            locations.append((830 , 220 + i * 200))
        for i in range(0, 3):
            locations.append((640 - i * 200, 820))
        for i in range(0, 3):
            locations.append((35 , 620 - i * 200))
        
        for i in range (1, len(locations) + 1):
            text = font.render(str(i), False, BLUE)
            self.display.blit(text, locations[i - 1])

    def convertPositionToIndex (self, x, y):
        return int((x - 50) / 100 - 1 + ((y - 50) / 100 -1) * 7)

    def writeIndex(self):
        # Function to draw index values on the board. 
        # The function is used for test purpose
        font = pygame.font.SysFont('Comic Sans MS', 20)
        index = 0
        for i in range(len(self.piecesList))  :
            rect = self.piecesList[i]
            text = font.render(str(i), False, BLUE)
            self.display.blit(text, (rect.x + 40, rect.y + 35))
            
    def movePiece(self, index, orientation = 0, currentPosition = ((0 , 0),(0 , 0)) ):


        xs = currentPosition[0][0]      # x start position
        ys = currentPosition[0][1]      # y end position
        xe = currentPosition[1][0]      # x start position
        ye = currentPosition[1][1]      # y end position

        # Define the range of indexes that needs to be moved
        moves = {
            1 : (1, 43),
            2 : (3, 45),
            3 : (5, 47),
            4 : (13, 7),
            5 : (27, 21),
            6 : (41, 35),
            7 : (47, 5),
            8 : (45, 3),
            9 : (43, 1),
            10 : (35, 41),
            11 : (21 ,27),
            12 : (7, 13)
        }

        # Copy the extra piece to a variable
        extraType = type(self.piecesList[49])                   # What type is the extra piece
        x, y = self.piecesList[moves[index][0]].getLocation()   # Where should the extra piece go in the end.
        extra = extraType(x,y, orientation)                                  # Create a new piece object with above parameters

        # Create a copy of the piece that is pushed out and save it in a new variable and store it as the extra piece in index 49
        # Only the type is needed since index 49 is only to show the extra piece and the orientation does not matter. 
        pushedPieceType = type(self.piecesList[moves[index][1]]) 
        


        if index <= 3 :

            # When a the piece you stand on is moved out of the board, then you are moved to the piece that is pushed in to the board
            if (self.convertPositionToIndex(xs,ys) == moves[index][1] ) :
                ys = 150

            # Move all the pieces in coloumn 1, 2 and 3 one down
            for i in range (moves[index][1], moves[index][0], - 7):
                # Get the values to create a new piece object that can replace the previous in the list
                tmpType = type(self.piecesList[i - 7])                      # Get the type of the piece above 
                tmpOrientation = self.piecesList[i - 7].getOrientation()    # Get the orientaion piece above
                newx, newy = self.piecesList[i].getLocation()               # Get the location that the piece is moved to
                self.piecesList[i] = tmpType(newx, newy, tmpOrientation)    # Create the object and place it in the list
                pass

            # Lastly place the extra piece in the top of the board (index 1,2 or 3)
            self.piecesList[moves[index][0]] = extra


        elif index >= 4 and index <= 6 :

            # When a the piece you stand on is moved out of the board, then you are moved to the piece that is pushed in to the board
            if (self.convertPositionToIndex(xs,ys) == moves[index][1] ) :
                xs = 750

            # Move all the pieces in row 4, 5 and 6 one to the left
            for i in range(moves[index][1], moves[index][0]):
                # Get the values to create a new piece object that can replace the previous in the list
                tmpType = type(self.piecesList[i + 1])                      # Get the type of the piece above 
                tmpOrientation = self.piecesList[i + 1].getOrientation()    # Get the orientaion piece above
                newx, newy = self.piecesList[i].getLocation()               # Get the location that the piece is moved to
                self.piecesList[i] = tmpType(newx, newy, tmpOrientation)    # Create the object and place it in the list
                pass

            # Lastly place the extra piece in the top of the board (index 1,2 or 3)
            self.piecesList[moves[index][0]] = extra 
        
        elif index >= 7 and index <= 9:

            # When a the piece you stand on is moved out of the board, then you are moved to the piece that is pushed in to the board
            if (self.convertPositionToIndex(xs,ys) == moves[index][1] ) :
                ys = 750

            # Move all the pieces in coloumn 7, 8 and 9 one up
            for i in range(moves[index][1], moves[index][0], 7):
                 # Get the values to create a new piece object that can replace the previous in the list
                tmpType = type(self.piecesList[i + 7])                      # Get the type of the piece above 
                tmpOrientation = self.piecesList[i + 7].getOrientation()    # Get the orientaion piece above
                newx, newy = self.piecesList[i].getLocation()               # Get the location that the piece is moved to
                self.piecesList[i] = tmpType(newx, newy, tmpOrientation)    # Create the object and place it in the list
                pass

            # Lastly place the extra piece in the top of the board (index 1,2 or 3)
            self.piecesList[moves[index][0]] = extra 

        elif index >= 10 :

            # When a the piece you stand on is moved out of the board, then you are moved to the piece that is pushed in to the board
            if (self.convertPositionToIndex(xs,ys) == moves[index][1] ) :
                xs = 150

            for i in range(moves[index][1], moves[index][0], - 1):
                # Get the values to create a new piece object that can replace the previous in the list
                tmpType = type(self.piecesList[i - 1])                      # Get the type of the piece above 
                tmpOrientation = self.piecesList[i - 1].getOrientation()    # Get the orientaion piece above
                newx, newy = self.piecesList[i].getLocation()               # Get the location that the piece is moved to
                self.piecesList[i] = tmpType(newx, newy, tmpOrientation)    # Create the object and place it in the list
                pass

            # Lastly place the extra piece in the top of the board (index 1,2 or 3)
            self.piecesList[moves[index][0]] = extra

        self.piecesList[49] = pushedPieceType(0, 0)             # Create the new piece object and store it in index 49
        return xs, ys, xe, ye




        
        