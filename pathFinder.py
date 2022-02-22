from newBoard import GREEN, Board
import pygame

class Node:
    def __init__(self, parentIndex, x, y) -> None:
        self.parentIndex = parentIndex
        self.x = x
        self.y = y
    
    def __del__(self):
        pass

class pathFinder():
    def __init__(self, xstart, ystart, xend, yend, DISPLAY) :
        self.closedList = []
        self.display = DISPLAY
        self.xs = xstart
        self.ys = ystart
        self.xe = xend
        self.ye = yend
        self.tree = []
        self.FinalPath = []

        self.tree.append(Node(None, self.xs, self.ys))
        self.closedList.append(self.convertPositionToIndex(self.xs, self.ys))
        
        
        #self.checkNode()

        # for i in range (len(self.tree)):
        #     print ("The list index of the parent: " + str(self.tree[i].parentIndex))
        #     idx = self.convertPositionToIndex(self.tree[i].x,self.tree[i].y)
        #     print ("The list index of the piece: " + str(i))
        #     print ("The board index of the piece: " + str(idx) + " : \n")
        
        #self.getFinalPath()
        #self.drawPath()

    def __del__(self) :
        pass

    def inClosedList(self, index):
        for i in self.closedList:
            if i == index:
                return True
        return False

    def convertPositionToIndex (self, x, y):
        return int((x - 50) / 100 - 1 + ((y - 50) / 100 -1) * 7)

    def checkNode(self):

        parentIndex = 0
        for node in self.tree:
            # print ("The x values = ( " + str(node.x) + ", " + str(self.xe) + " )"  )
            # print ("The y values = ( " + str(node.y) + ", " + str(self.ye) + " )"  )
            # print ("Index being checked = " + str(self.convertPositionToIndex(node.x, node.y)) + "\n")
            if (node.x == self.xe and node.y == self.ye):
                #self.tree.append(Node(parentIndex, node.x, node.y))
                print ("Goal has been found" )
                return True
            
            # Look up
            if (self.display.get_at((node.x, node.y - 66)) == GREEN and self.display.get_at((node.x, node.y - 33)) == GREEN):
                indexOfPiece = self.convertPositionToIndex( node.x, node.y - 100)
                if (not self.inClosedList(indexOfPiece)):
                    self.tree.append(Node(parentIndex, node.x, node.y - 100))
                    self.closedList.append(indexOfPiece)

            # Look down    
            if (self.display.get_at((node.x, node.y + 66)) == GREEN and self.display.get_at((node.x, node.y + 33)) == GREEN):
                indexOfPiece = self.convertPositionToIndex( node.x, node.y + 100)
                if (not self.inClosedList(indexOfPiece)):
                    self.tree.append(Node(parentIndex, node.x, node.y + 100))
                    self.closedList.append(indexOfPiece)
            
            # Look right
            if (self.display.get_at((node.x + 66, node.y)) == GREEN and self.display.get_at((node.x + 33, node.y)) == GREEN):
                indexOfPiece = self.convertPositionToIndex( node.x + 100, node.y)
                if (not self.inClosedList(indexOfPiece)):
                    self.tree.append(Node(parentIndex, node.x + 100, node.y))
                    self.closedList.append(indexOfPiece)

            # Look left
            if (self.display.get_at((node.x - 66, node.y)) == GREEN and self.display.get_at((node.x - 33, node.y)) == GREEN):
                indexOfPiece = self.convertPositionToIndex( node.x - 100, node.y )
                if (not self.inClosedList( indexOfPiece)):
                    self.tree.append(Node(parentIndex, node.x - 100, node.y))
                    self.closedList.append(indexOfPiece)
            

   
            parentIndex += 1
        print ("Could not find path")
        return False 


    def getFinalPath(self):
        idx = 0
        for i in (range (len (self.tree) - 1,0, - 1)):
            if self.tree[i].x == self.xe and self.tree[i].y == self.ye:
                idx = i
                break 
        
        while idx != None:
            self.FinalPath.append(self.tree[idx])
            idx = self.tree[idx].parentIndex

    def drawPath(self):
        for i in range (len (self.FinalPath) - 1):
            startpos = self.FinalPath[i].x, self.FinalPath[i].y
            endpos = self.FinalPath[i+1].x, self.FinalPath[i+1].y
            pygame.draw.line(self.display, (0,0,0), startpos, endpos, 2)
            
    