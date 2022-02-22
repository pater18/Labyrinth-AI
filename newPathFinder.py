import pygame
from newBoard import *


class PathFinder:
    def __init__(self, Board, start, end) -> None:
        self.tree = []
        self.closedList = []
        self.finalPath = []
        self.board = Board
        self.start = start  # Should be the index of the pieces list 
        self.end = end      # Should also be the index of the pieces list. 
        
        pass

    def checkPositions(self):
        # Define the start and end indecies of the movable pieces
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

        
        pass


    def checkNode(self):
        
        self.tree.append((self.board.piecesList[self.start], None))
        self.closedList.append(self.start)
        parentIndex = 0
        for node, pIndex in self.tree:
            if node.index == self.end:
                print ("Goal has been found")
                return True
            
            # Get the pieces that the player can move to from the current position
            pieceAbove, pieceRight, pieceBelow, pieceLeft = self.get4piecesAround(node.index)
            
            # The orientation to look at 
            #   # 0 #  # 0 #
            #   3 # 1  3 # 1
            #   # 2 #  # 2 #
            
            #   # 0 #  # 0 #
            #   3 # 1  3 # 1
            #   # 2 #  # 2 #
            
            # Look up 
            if pieceAbove is not None:
                if pieceAbove.orientation[2] == 1 and node.orientation[0] == 1:
                    if not self.inClosedList(pieceAbove.index): 
                        self.tree.append((pieceAbove, parentIndex))
                        self.closedList.append(pieceAbove.index)

            # Look down            
            if pieceBelow is not None:
                if pieceBelow.orientation[0] == 1 and node.orientation[2] == 1:
                    if not self.inClosedList(pieceBelow.index): 
                        self.tree.append((pieceBelow, parentIndex))
                        self.closedList.append(pieceBelow.index)
            
            # Look right
            if pieceRight is not None:
                if pieceRight.orientation[3] == 1 and node.orientation[1] == 1:
                    if not self.inClosedList(pieceRight.index): 
                        self.tree.append((pieceRight, parentIndex))
                        self.closedList.append(pieceRight.index)

            # Look left
            if pieceLeft is not None:
                if pieceLeft.orientation[1] == 1 and node.orientation[3] == 1:
                    if not self.inClosedList(pieceLeft.index): 
                        self.tree.append((pieceLeft, parentIndex))
                        self.closedList.append(pieceLeft.index)
                
            parentIndex += 1
        print ("Could not find goal")
        return False
        

    def inClosedList(self, index):
        for i in self.closedList:
            if i == index:
                return True
        return False    
        
    def getPath(self):
        idx = 0
        for i in range(len(self.tree) - 1, 0, - 1):
            if self.tree[i][0].index == self.end: 
                idx = self.tree[i][1]
                self.finalPath.append(self.tree[i][0])
                break
        
        # for piece, parent in self.tree:
        #     print ("Piece position = " + str(piece.position) + ", parent index: " + str(parent) + ", index: " + str(piece.index))

        while idx is not None:
            self.finalPath.append(self.tree[idx][0])
            idx = self.tree[idx][1]
            pass

        # for piece in self.finalPath:
        #     print (piece.index)

    def drawPath(self, display):
        for i in range (len (self.finalPath) - 1):
            startpos = self.finalPath[i].position[0] + int(DEFAULT_IMAGE_SIZE[0] / 2), self.finalPath[i].position[1] + int(DEFAULT_IMAGE_SIZE[1] / 2)
            endpos = self.finalPath[i + 1].position[0] + int(DEFAULT_IMAGE_SIZE[0] / 2), self.finalPath[i + 1].position[1] + int(DEFAULT_IMAGE_SIZE[1] / 2)
            pygame.draw.line(display, (255,0,0), startpos, endpos, 4)

    def get4piecesAround(self, index):
        above = self.board.piecesList[index - 7]        if index > 6 else None 
        rightSide = self.board.piecesList[index + 1]    if index % 7 < 6 else None
        below = self.board.piecesList[index + 7]        if index < 42 else None
        leftSide = self.board.piecesList[index - 1]     if index % 7 > 0 else None 
        return above, rightSide, below, leftSide