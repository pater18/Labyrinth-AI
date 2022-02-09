from Board import GREEN, Board
import pygame

class tree:
    def __init__(self, index) -> None:
        self.treeList = [None]

class treeNode:
    def __init__(self, index, layer, xstart, ystart, xend, yend, DISPLAY) -> None:
        self.index = index
        self.layer = layer
        self.xs = xstart
        self.ys = ystart
        self.xe = xend
        self.ye = yend
        self.wall = True
        self.display = DISPLAY
        

    def addNode(self):
        # Look up
        if (self.display.get_at((self.xs, self.ys - 66)) == GREEN ):
            nwNode = treeNode(self.index, self.layer + 1, self.xs, self.ys - 100, self.xe, self.ye, self.display)

        # Look Down 

        # Look Left

        # Look right

class pathFinder:
    def __init__(self, start, end, board) -> None:
        self.openList = []
        self.closedList = []
        self.board = board
        self.populateOpenList()

    def populateOpenList(self):
        for x in range(150, 751, 100):
            for y in range (150, 751, 100):
                self.openList.append((x,y))
    def run(self):
        root = tree(1)

    def test(self):
        for i in range(5):
            print (i)



        
    