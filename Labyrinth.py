import pygame, sys, random
from pygame.locals import *
import numpy as np 
from Board import Board
from pathFinder import pathFinder

BLUE    = (0,   0,   255)
GREEN   = (0,   255, 0  )
RED     = (255, 0,   0  )
GRAY    = (200, 200, 200)
LGRAY   = (150, 150, 150)
BLACK   = (0,   0,   0  )  
WINDOWWIDTH = 900
WINDOWHEIGHT = 900
FPS = 10

def initGame():
    global FPSCLOCK, DISPLAY, nodeSize
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Labyrinth')
    DISPLAY.fill((200, 200, 200))
    pygame.font.init()


def main(): 
    initGame()
    game = Board(WINDOWHEIGHT, WINDOWWIDTH, DISPLAY)
    path = pathFinder(1,1, game)

    path.test()

    while (1):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.KEYDOWN :
                if event.key >= 49 and event.key <= 57:
                    game.movePiece(event.key - 48)
                    game.drawBoard()
                if event.key == 97 :
                    game.movePiece(11)
                    game.drawBoard()
                if event.key == 98 :
                    game.movePiece(12)
                    game.drawBoard()
                if event.key == 48 :
                    game.movePiece(10)
                    game.drawBoard()


        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()