from time import sleep
from turtle import position
from cv2 import cornerEigenValsAndVecs
from matplotlib.pyplot import draw
import pygame, sys, random
from pygame.locals import *
import numpy as np 
#from Board import Board
from pathFinder import pathFinder, Node
import copy
import os
from newBoard import *
from newPathFinder import* 
import cv2

BLUE    = (0,   0,   255)
GREEN   = (0,   255, 0  )
RED     = (255, 0,   0  )
GRAY    = (200, 200, 200)
LGRAY   = (150, 150, 150)
BLACK   = (0,   0,   0  )  
WINDOWWIDTH = 1200
WINDOWHEIGHT = 900
FPS = 10
DEFAULT_IMAGE_SIZE = (100, 100)

def initGame():
    global FPSCLOCK, DISPLAY, nodeSize
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Labyrinth')
    DISPLAY.fill((200, 200, 200))
    pygame.font.init()


def centerOfBox(mouseClick):
    # Returns the center of each board piece in x and y
    # TODO: change the hardcoded values to board pieces width and height 
    return mouseClick[0] - (mouseClick[0] % 100) + 50, mouseClick[1] - (mouseClick[1] % 100) + 50

def getPosition(position):
    # Resives a position in x and y and returns an index to the piece on the board corresponding to the position
    # TODO: Change the hardcoded values used in the modulus to the width of the piece in pixels
    xs = position[0] - (position[0] % 100) 
    ys = position[1] - (position[1] % 100)
    pos = (xs ) / 100 - 1 + ((ys) / 100 - 1) * 7

    return int(pos) 

def copyGameState(gameList):
    # This function is to copy the current state of the game. This is to revert to this state if it is not
    # possible to find a path from the two points on the board that is scearched. 
    
    # This function is nessesry because a move is made and then is a path scearced for. 
    # If there is no solution the scearced state, then the board is reverted to this saved state. It is overwritten if a valid path is found
    gameState = []
    for piece in gameList:
        newPiece = Piece(piece.name, piece.position, piece.orientation, piece.img)
        newPiece.index = piece.index
        gameState.append(newPiece)
    
    return gameState

def findIndexList(ls, value):
    # Takes a list and a value. 
    # Will return the index of that value in the list
    idx = 0
    for val in ls:
        if val == value:
            return idx
        idx += 1

    return None

def checkPositions(start, end, index):
    # Define the start and end indecies of the movable pieces
    moves = {
        1 : [1, 8, 15, 22, 29, 36, 43],
        2 : [3, 10, 17, 24, 31, 38, 45],
        3 : [5, 12, 19, 26, 33, 40, 47],

        4 : [13, 12, 11, 10, 9, 8, 7],
        5 : [27, 26, 25, 24, 23, 22, 21],
        6 : [41, 40, 39, 38, 37, 36, 35],

        7 : [47, 40, 33, 26, 19, 12, 5],
        8 : [45, 38, 31, 24, 17, 10, 3],
        9 : [43, 36, 29, 22, 15, 8, 1],

        10 : [35, 36, 37, 38, 39, 40, 41],
        11 : [21, 22, 23, 24, 25, 26,27],
        12 : [7, 8, 9, 10, 11, 12, 13]
    }

    # Find the index for the start position, if it is in, one of the lists above 
    newIdx = findIndexList(moves[index], start)
    if newIdx :
        if start == moves[index][-1]:
            start = moves[index][0] 
        else: 
            start = moves[index][newIdx + 1]

    # Find the index for the end position if it is in one of the lists above
    idxForEnd = findIndexList(moves[index], end)
    if idxForEnd:
        if end == moves[index][-1]:
            print ("Move is not possible. The piece will end op as the extra piece in the corner")
            end = None
        else:
            end = moves[index][idxForEnd + 1]

    return start, end

def checkForGoal(game, pos1, pos2, oldlist):
    # Function that takes the board, index to the start and end, and last a list of how the board is 
    # when the function is called

    goalFound = False
    indexPieceStart = getPosition(pos1)
    indexPieceEnd = getPosition(pos2)
    print ("Index that are beeing checked: (" + str(indexPieceStart) + ", " + str(indexPieceEnd) + ")\n")
    # The first range is because there are 12 places to push in a new piece and the second has four, because there are four different orientations
    for i in range (12):
        for orientaion in range(4):
            game.rotatePiece(49, orientaion)
            game.move(i + 1)
            
            # Check to make sure that the player moves with the pieces if they stand on them
            indexPieceStart, indexPieceEnd = checkPositions(indexPieceStart , indexPieceEnd, i + 1)
            if indexPieceEnd == None :
                break

            game.updateBoard()

            # Start the path finder, and try to find a path between the two points (start, end) 
            find = PathFinder(game, indexPieceStart, indexPieceEnd )
            if find.checkNode():    # Checks for a path and returns true if it finds one
                find.getPath()      # Gets the found path
                find.drawPath(DISPLAY) 
                oldlist = copyGameState(game.piecesList) # Set current board as the lastest 
                goalFound = True
                break
            else: 
                game.piecesList = copyGameState(oldlist)    # If a path was not found the board is rest to an earlier state
                indexPieceStart = getPosition(pos1)         # The same goes for the positions, since they could have been changed earlier
                indexPieceEnd = getPosition(pos2)
                game.updateBoard()                          # Draw the board again.
        if goalFound:
            break



def main(): 
    initGame()
    game = Board(DISPLAY)
    firstMouseClick = True
    game.drawValues()
    oldlist = copyGameState(game.piecesList) # Save the current state of the board 
    
    while (1):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            # Move the extra piece in from one of the sides, with the numbers 0 - 9 and the letters ('a' and 'b')
            if event.type == pygame.KEYDOWN :
                if event.key >= 49 and event.key <= 57:
                    game.move(event.key - 48)
                if event.key == 97 : # a
                    game.move(11) 
                if event.key == 98 : # b
                    game.move(12) 
                if event.key == 48 : # 0
                    game.move(10) 

            # Check by moving a piece in on all sides and try to find a path. 
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RETURN:
                    checkForGoal(game, pos1, pos2, oldlist)


                # Reset board to previous state
                if event.key == pygame.K_m:
                    game.piecesList = copyGameState(oldlist)
                    game.updateBoard()


            # Get the mouse input to select the two positions that we want to find a path between
            if event.type == pygame.MOUSEBUTTONDOWN : 
                if firstMouseClick :
                    pos1 = centerOfBox(pygame.mouse.get_pos())
                    firstMouseClick = False
                    print ("First position is " + str(pos1) + " at index " + str(getPosition(pos1)) )
                else :
                    pos2 = centerOfBox(pygame.mouse.get_pos())
                    print ("Second position is "  + str(pos2) + " at index " + str(getPosition(pos2)))
                    firstMouseClick = True


        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()