from tkinter import Y
import pygame
import random


class BoardCornerPiece :
    def __init__(self, positionX, positionY, combination = None) -> None:
        self.orientations = [(1,5),(5,7),(7,3),(3,1)]
        if combination == None:
            self.orientation = self.orientations[random.randint(0,3)]
        else: 
            self.orientation = self.orientations[combination]
        self.x = positionX
        self.y = positionY
        self.windowSize = 700
        self.layout = [None] * 9 # create an empty list of length 9
        self.initPiece()

    def initPiece(self):
        nodeSize = self.windowSize / (3 * 7)

        #These four are always false
        self.layout[0] = pygame.Rect(self.x, self.y, nodeSize , nodeSize  ), False
        self.layout[2] = pygame.Rect(self.x + nodeSize * 2, self.y, nodeSize, nodeSize  ) , False
        self.layout[6] = pygame.Rect(self.x, self.y + nodeSize * 2, nodeSize, nodeSize ) , False
        self.layout[8] = pygame.Rect(self.x + nodeSize * 2, self.y + nodeSize * 2, nodeSize, nodeSize) , False
        
        # Number 4 is always true 
        self.layout[4] = pygame.Rect(self.x + nodeSize, self.y + nodeSize, nodeSize, nodeSize) , True
        
        self.layout[1] = pygame.Rect(self.x + nodeSize, self.y, nodeSize, nodeSize) , False    
        self.layout[3] = pygame.Rect(self.x, self.y + nodeSize, nodeSize, nodeSize ) , False
        self.layout[5] = pygame.Rect(self.x + nodeSize * 2, self.y + nodeSize, nodeSize, nodeSize) , False
        self.layout[7] = pygame.Rect(self.x + nodeSize, self.y  + nodeSize * 2, nodeSize, nodeSize) , False

        # Set the pieces with the correct orientation
        self.layout[self.orientation[0]] = self.layout[self.orientation[0]][0], True
        self.layout[self.orientation[1]] = self.layout[self.orientation[1]][0], True
    
    def updateLocation(self, newPosition):
        self.x = newPosition[0]
        self.y = newPosition[1]
        self.initPiece()

    def getLocation(self) :
        return self.x, self.y
    
    def getOrientation(self):
        for i in range(len(self.orientations )):
            if set(self.orientation) == set(self.orientations[i]) :
                return i 
        return None




  
class BoardStraightPiece:
    
    def __init__(self, positionX, positionY, combination = None) -> None:
        self.orientationsStraight = [(1,7),(5,3)]
        if combination == None:
            self.orientation = self.orientationsStraight[random.randint(0,1)]
        else:
            self.orientation = self.orientationsStraight[combination]
        self.x = positionX
        self.y = positionY
        self.windowSize = 700
        self.layout = [None] * 9 # create an empty list of length 9
        
        self.initPiece()
        pass

    def initPiece(self):
        nodeSize = self.windowSize / (3 * 7)

        #These four are always false
        self.layout[0] = pygame.Rect(self.x, self.y, nodeSize , nodeSize  ), False
        self.layout[2] = pygame.Rect(self.x + nodeSize * 2, self.y, nodeSize, nodeSize  ) , False
        self.layout[6] = pygame.Rect(self.x, self.y + nodeSize * 2, nodeSize, nodeSize ) , False
        self.layout[8] = pygame.Rect(self.x + nodeSize * 2, self.y + nodeSize * 2, nodeSize, nodeSize) , False
        
        # Number 4 is always true 
        self.layout[4] = pygame.Rect(self.x + nodeSize, self.y + nodeSize, nodeSize, nodeSize) , True
        
        self.layout[1] = pygame.Rect(self.x + nodeSize, self.y, nodeSize, nodeSize) , False    
        self.layout[3] = pygame.Rect(self.x, self.y + nodeSize, nodeSize, nodeSize ) , False
        self.layout[5] = pygame.Rect(self.x + nodeSize * 2, self.y + nodeSize, nodeSize, nodeSize) , False
        self.layout[7] = pygame.Rect(self.x + nodeSize, self.y  + nodeSize * 2, nodeSize, nodeSize) , False

        # Set the pieces with the correct orientation
        self.layout[self.orientation[0]] = self.layout[self.orientation[0]][0], True
        self.layout[self.orientation[1]] = self.layout[self.orientation[1]][0], True

    def updateLocation(self, newPosition):
        self.x = newPosition[0]
        self.y = newPosition[1]
        self.initPiece()

    def getLocation(self) :
        return self.x, self.y

    def getOrientation(self):
        for i in range(len(self.orientationsStraight )):
            if set(self.orientation) == set(self.orientationsStraight[i]) :
                return i 
        return None

class BoardTPiece:


    def __init__(self, positionX, positionY, combination = None) -> None:
        # The three arguments it takes is a x-positon, y-position, and maybe an orientation
        self.orientationsT = [(1,3,5),(1,5,7),(7,5,3),(7,3,1)]  
        self.windowSize = 700
        self.layout = [None] * 9 # create an empty list of length 9
        self.x = positionX
        self.y = positionY
        
        if combination == None :
            self.orientation = self.orientationsT[random.randint(0,3)] # This takas a random combination from the list above
        else : 
            self.orientation = self.orientationsT[combination]
        self.initPiece()
    

    def initPiece(self):
        nodeSize = self.windowSize / (3 * 7)

        #These four are always false
        self.layout[0] = pygame.Rect(self.x, self.y, nodeSize , nodeSize  ), False
        self.layout[2] = pygame.Rect(self.x + nodeSize * 2, self.y, nodeSize, nodeSize  ) , False
        self.layout[6] = pygame.Rect(self.x, self.y + nodeSize * 2, nodeSize, nodeSize ) , False
        self.layout[8] = pygame.Rect(self.x + nodeSize * 2, self.y + nodeSize * 2, nodeSize, nodeSize) , False
        
        # Number 4 is always true 
        self.layout[4] = pygame.Rect(self.x + nodeSize, self.y + nodeSize, nodeSize, nodeSize) , True
        
        self.layout[1] = pygame.Rect(self.x + nodeSize, self.y, nodeSize, nodeSize) , False    
        self.layout[3] = pygame.Rect(self.x, self.y + nodeSize, nodeSize, nodeSize ) , False
        self.layout[5] = pygame.Rect(self.x + nodeSize * 2, self.y + nodeSize, nodeSize, nodeSize) , False
        self.layout[7] = pygame.Rect(self.x + nodeSize, self.y  + nodeSize * 2, nodeSize, nodeSize) , False


        # Set the pieces with the correct orientation, by choosing 
        self.layout[self.orientation[0]] = self.layout[self.orientation[0]][0], True
        self.layout[self.orientation[1]] = self.layout[self.orientation[1]][0], True
        self.layout[self.orientation[2]] = self.layout[self.orientation[2]][0], True

    def updateLocation(self, newPosition):
        self.x = newPosition[0]
        self.y = newPosition[1]
        self.initPiece()
    
    def getLocation(self) :
        return self.x, self.y
    
    def getOrientation(self):
        for i in range(len(self.orientationsT )):
            if set(self.orientation) == set(self.orientationsT[i]) :
                return i 
        return None