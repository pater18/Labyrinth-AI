import os
from turtle import update
from matplotlib import collections
import pygame
import random
import copy
from time import sleep


DEFAULT_IMAGE_SIZE = (100, 100)
FIRST_IMAGE_POSITION = (100, 100) # This will create a boarder around the board
BLUE    = (0,   0,   255)
GREEN   = (0,   255, 0  )
RED     = (255, 0,   0  )
GRAY    = (200, 200, 200)
LGRAY   = (150, 150, 150)
BLACK   = (0,   0,   0  )  

finished = 0

class Piece:
    def __init__(self, name, position, orientation, img = None) -> None:
        # An orientation could be discriped as [1, 1, 1, 0 ] which corresponds to [3, 5, 7] for a T piece
        # A corner piece could then look like [1, 1, 0, 0] which corresponds to [1, 5]
        # A straight piece could be [1, 0, 1, 0] which is the same as [1, 7] 
        self.orientation = orientation
        self.position = position # An x and y position
        self.name = name
        self.img = img
        self.index = None
        if self.img == None:
            self.loadBoardPiece()

    def loadBoardPiece(self):
        global finished
        self.img = pygame.image.load(os.path.join("images", "Corrected", self.name + ".png"))
        self.img = pygame.transform.scale(self.img, DEFAULT_IMAGE_SIZE)
        finished += 2
        print ("Loading is " + str(finished) + "% done")
    
    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position


class Board:
    def __init__(self, DISPLAY) -> None:
        self.piecesList = [None] * 50 # Create an empty list
        self.display = DISPLAY
        self.finalPath = []
        self.initializePiecesList()
        self.setNonConstantPieces()
        self.updateBoard()
        self.writeIndex()
        # self.orientationTest()
    
    def initializePiecesList(self):
        # This function should initalize the list with all the constant pieces that cannot be moved on the board
        x, y = FIRST_IMAGE_POSITION
        size = DEFAULT_IMAGE_SIZE[0]

        self.piecesList[0] = Piece("CornerRed", (x, y), [0, 1, 1, 0] )  # (100, 100)
        self.piecesList[2] = Piece("Book", (x + 2 * size, y + 0 * size), [0, 1, 1, 1] )  
        self.piecesList[4] = Piece("MoneyBag", (x + 4 * size, y + 0 * size), [0, 1, 1, 1])
        self.piecesList[6] = Piece("CornerYellow", (x + 6 * size, y + 0 * size), [0, 0, 1, 1])
        self.piecesList[14] = Piece("Map", (x + 0 * size, y + 2 * size), [1, 1, 1, 0])
        self.piecesList[16] = Piece("Crown", (x + 2 * size, y + 2 * size), [1, 1, 1, 0])
        self.piecesList[18] = Piece("Keys", (x + 4 * size, y + 2 * size), [0, 1, 1, 1])
        self.piecesList[20] = Piece("Skull", (x + 6 * size, y + 2 * size), [1, 0, 1, 1])
        self.piecesList[28] = Piece("Ring", (x + 0 * size, y + 4 * size), [1, 1, 1, 0])
        self.piecesList[30] = Piece("MoneyChest", (x + 2 * size, y + 4 * size), [1, 1, 0, 1])
        self.piecesList[32] = Piece("Diamond", (x + 4 * size, y + 4 * size), [1, 0, 1, 1])
        self.piecesList[34] = Piece("Sword", (x + 6 * size, y + 4 * size), [1, 0, 1, 1])
        self.piecesList[42] = Piece("CornerGreen", (x + 0 * size, y + 6 * size), [1, 1, 0, 0]) 
        self.piecesList[44] = Piece("Candle", (x + 2 * size, y + 6 * size), [1, 1, 0, 1])
        self.piecesList[46] = Piece("Helmet", (x + 4 * size, y + 6 * size), [1, 1, 0, 1])
        self.piecesList[48] = Piece("CornerBlue", (x + 6 * size, y + 6 * size), [1, 0, 0, 1])
    
    def setNonConstantPieces(self):
        # Nine corners and 11 straights

        # The list to contain the pieces that are placed one the board
        leftOverPieces = []

        cornerOrientations = [[1, 0, 0, 1,], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1] ]
        TOrientations = [[1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0], [0, 1, 1, 1]]
        straightOrientations = [[1, 0, 1, 0], [0, 1, 0, 1]]

        # First are the corners added to the list with a random orientation. The correct position is not set yet
        for corners in range(10):
            randOrientation = random.randint(0,3) 
            newPiece = Piece("Corner", (0,0) , cornerOrientations[randOrientation] )
            for i in range (randOrientation):
                newPiece.img = pygame.transform.rotate(newPiece.img, 270) # Rotate 90 degrees clockwise
            leftOverPieces.append(newPiece)
            

        # Second are the straight pieces added to the list
        for straights in range(12):
            randOrientation = random.randint(0,1)
            newPiece = Piece("Straight", (0,0) , straightOrientations[randOrientation] )
            for i in range(randOrientation):
                newPiece.img = pygame.transform.rotate(newPiece.img, 270)
            leftOverPieces.append(newPiece)

        # Lastly are the pieces with drawings added to the list. They are only corners and T pieces. 
        # The orientation is set to be the same for all of them
        for i in range(12):
            name = str(i+1) 
            randOrientation = random.randint(0,3) 
            if i <= 5:
                orientation = TOrientations[randOrientation]
                newPiece = Piece(name, (0,0), orientation)
            else:
                orientation = cornerOrientations[randOrientation]
                newPiece = Piece(name, (0,0), orientation)

            for i in range(randOrientation):
                newPiece.img = pygame.transform.rotate(newPiece.img, 270)
            leftOverPieces.append(newPiece)

        # The list is then randomized
        random.shuffle(leftOverPieces)

        # Finaly is the original list updated so it does not contain any None elements
        index = 0
        for i in range(49):
            if self.piecesList[i] == None:
                oldPosition = self.piecesList[i - 1].getPosition() # Take the position of the piece before
                if oldPosition[0] >= FIRST_IMAGE_POSITION[0] + (DEFAULT_IMAGE_SIZE[0] * 6): # If the piece before is all the way at the end set the next piece at the front
                    newPosition = FIRST_IMAGE_POSITION[0], oldPosition[1] + DEFAULT_IMAGE_SIZE[1]
                else :
                    newPosition = oldPosition[0] + DEFAULT_IMAGE_SIZE[0], oldPosition[1]    
                
                leftOverPieces[index].position = newPosition
                self.piecesList[i] = leftOverPieces[index]
                index += 1

        # The extra piece in the corner.     
        self.piecesList[49] = leftOverPieces[index]
        self.convertPositionToIndex()

    def rotatePiece(self, index, times = 1):
        for i in range (times):
            piece = self.piecesList[index]
            newOrientation = [piece.orientation[3], piece.orientation[0], piece.orientation[1], piece.orientation[2] ] # Shift one to the right
            self.piecesList[index].img = pygame.transform.rotate(piece.img, 270) # Rotate 90 degrees clockwise
            self.piecesList[index].orientation = newOrientation

        self.updateBoard()
        
    def updateBoard(self):    
        for piece in self.piecesList:
            if piece is not None:
                self.display.blit(piece.img, piece.position)
        pygame.display.update()

    def move(self, index):

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

        tmpList = []
        for piece in self.piecesList:
            tmpList.append(piece)

        tmpList[49].position = tmpList[moves[index][0]].position
        self.piecesList[moves[index][0]] = tmpList[49]

        if index <= 3:
            for i in range (moves[index][0], moves[index][1], 7):
                tmpList[i].position = self.piecesList[i + 7].position
                self.piecesList[i + 7] = tmpList[i]

        elif index >= 4 and index <= 6 :
            for i in range (moves[index][0], moves[index][1], - 1):
                tmpList[i].position = self.piecesList[i - 1].position
                self.piecesList[i - 1] = tmpList[i]
        
        elif index >= 7 and index <= 9:
            for i in range (moves[index][0], moves[index][1] - 1, -7):
                tmpList[i].position = self.piecesList[i - 7].position
                self.piecesList[i - 7] = tmpList[i]
        
        elif index >= 10 :
            for i in range (moves[index][0], moves[index][1]):
                tmpList[i].position = self.piecesList[i + 1].position
                self.piecesList[i + 1] = tmpList[i]


        tmpList[moves[index][1]].position = (0,0) 
        self.piecesList[49] = tmpList[moves[index][1]]
        self.convertPositionToIndex()
        self.updateBoard()
        pass

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

    def convertPositionToIndex (self, x = None, y = None):
        
        # If i want to convert another position to index 
        if x is not None: 
            if x >= DEFAULT_IMAGE_SIZE[0] and x <= DEFAULT_IMAGE_SIZE[0] * 7:   # These two if statements check that and index is only calculated if it is a valid position
                if y >= DEFAULT_IMAGE_SIZE[1] and y <= DEFAULT_IMAGE_SIZE[1] * 7:
                    return int(x / DEFAULT_IMAGE_SIZE[0] - 1 + (y / DEFAULT_IMAGE_SIZE[0] - 1) * 7) # 800/100 - 1 = 7       100 / 100 - 1 * 7 = 0
                else:
                    return None                                                                         # 100/100 - 1 = 0       200 / 100 - 1 * 7 = 7   

        for piece in self.piecesList: 
            x, y = piece.position
            piece.index = int(x / DEFAULT_IMAGE_SIZE[0] - 1 + (y / DEFAULT_IMAGE_SIZE[0] - 1) * 7)

    def writeIndex(self):

        # Function to draw index values on the board. 
        # The function is used for test purpose
        font = pygame.font.SysFont('Comic Sans MS', 20)
        index = 0
        for i in range(len(self.piecesList))  :
            rect = self.piecesList[i].position
            text = font.render(str(i), False, BLUE)
            self.display.blit(text, (rect[0] + 40, rect[1] + 35))

    def orientationTest(self):

        for piece in self.piecesList:
            print("Index = " + str(piece.index) + " orientation = " + str(piece.orientation) )

   
    def resetBoard2PreviousMove(self):
        pass
