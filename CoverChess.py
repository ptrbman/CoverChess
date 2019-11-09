
##
##    Create OpenAI Gym structure
##

import numpy as np
import random
import pygame

CELL_P = 4
CELL_W = 80
CELL_H = 80


##
##  PIECES
##

BLACK = -1
WHITE = 1

BROOK = 1
WROOK = 2

class Board:
    def __init__(self, size_):
        self.size = size_     
        self.matrix = ([0]*self.size*self.size)
        self.hitMatrix = ([0]*self.size*self.size)
        self.pieces = 0


    def __str__(self):
        string = ""        
        for row in range(self.size):
            rowString = ""            
            for col in range(self.size):
                s = str(self.m(row, col))                
                rowString = rowString + ((3-len(s))*" ") + s                
                # rowString = rowString + str(self.m(row, col))
            string = string + "\n" + rowString
        return string        

    ##
    ##  MATRIX ACCESS FUNCTIONS
    ##

    def m(self, row, col):
        return self.matrix[row*self.size + col]
    def mSet(self, row, col, val):
        self.matrix[row*self.size + col] = val

    def hm(self, row, col):
        return self.hitMatrix[row*self.size + col]
    def hmMod(self, row, col, value):
        self.hitMatrix[row*self.size + col] += value
    def hmSet(self, row, col, val):
        self.hitMatrix[row*self.size + col] = val        
        

    ##
    ##  INTERNAL FUNCTIONS
    ##

    def printHitMatrix(self):
        string = ""
        for row in range(self.size):
            rowString = ""
            for col in range(self.size):
                s = str(self.hm(row, col))
                rowString = rowString + ((3-len(s))*" ") + s
            string = string + "\n" + rowString
        print(string)


    ##
    ##  COVER FUNCTIONS
    ##
    def rookCover(self, row, col, color):
        for c in range(col-1, -1, -1):
            if (self.m(row, c) != 0):
                break
            else:
                self.hmMod(row, c, color)
                
        for c in range(col+1, self.size):
            if (self.m(row, c) != 0):
                break
            else:
                self.hmMod(row, c, color)


        for r in range(row-1, -1, -1):
            if (self.m(r, col) != 0):
                break
            else:
                self.hmMod(r, col, color)
                
        for r in range(row+1, self.size):
            if (self.m(r, col) != 0):
                break
            else:
                self.hmMod(r, col, color)                
            
        # for r in range(0, row):
        #     self.hmMod(r, col, color)
        # for r in range(row+1, self.size):
        #     self.hmMod(r, col, color)            

    ##
    ##  PUBLIC FUNCTIONS
    ##


    def DrawBoard(self, screen):
        self.UpdateHitMatrix()
        myfont = pygame.font.SysFont('Comic Sans MS', 60)
        
        for row in range(self.size):
            for col in range(self.size):

                    # pygame.draw.rect(screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)),
                pygame.draw.rect(screen, (230, 230, 230),                    
                                 pygame.Rect(row*CELL_H + CELL_P, col*CELL_W + CELL_P, CELL_H - CELL_P, CELL_W - CELL_P))


                if self.m(row, col) == 0:
                    if (self.hm(row, col) > 0):
                        txtcolor = (0, 180, 0)
                    elif (self.hm(row, col) < 0):
                        txtcolor = (180, 0, 0)
                    else:
                        txtcolor = (80, 80, 80)
                    textsurface = myfont.render(str(self.hm(row, col)), False, txtcolor)
                    screen.blit(textsurface,(row*CELL_H + CELL_P*2,col*CELL_W+CELL_P*2))
                elif self.m(row, col) == BROOK:
                    color = (0,0,0)
                    center = (int(row*CELL_H + CELL_H/2), int(col*CELL_W + CELL_W/2))
                    radius = int(CELL_W/2) - CELL_P*2
                    pygame.draw.circle(screen, color, center, radius, 0)
                elif self.m(row, col) == WROOK:
                    color = (255,255,255)
                    center = (int(row*CELL_H + CELL_H/2), int(col*CELL_W + CELL_W/2))
                    radius = int(CELL_W/2) - CELL_P*2
                    pygame.draw.circle(screen, color, center, radius, 0)


        (ws, bs) = self.GetScore()
        score = ws - bs
        if (score > 0):
            txtcolor = (0, 180, 0)
        elif (score < 0):
            txtcolor = (180, 0, 0)
        else:
            txtcolor = (80, 80, 80)                    

        pygame.draw.rect(screen, (180, 170, 80), pygame.Rect(self.size*CELL_H + CELL_P, 0, CELL_W, CELL_H))
        textsurface = myfont.render(str(score), False, txtcolor)
        screen.blit(textsurface,(self.size*CELL_H + CELL_P*2,0))
                    

    ## Places piece at (row, col)
    def PlacePiece(self, row, col, piece):
        self.mSet(row, col, piece)
        self.pieces += 1
    
    ## Refreshes the hit matrix
    def UpdateHitMatrix(self):
        for row in range(self.size):
            for col in range(self.size):
                self.hmSet(row, col, 0)

        for row in range(self.size):
            for col in range(self.size):
                if (self.m(row, col) == BROOK):
                    self.rookCover(row, col, BLACK)
                elif (self.m(row, col) == WROOK):
                    self.rookCover(row, col, WHITE)                    
                elif (self.m(row, col) != 0):
                    print("...", self.m(row, col))
                
        # self.printHitMatrix()

    def GetScore(self):
        whiteScore = 0
        blackScore = 0
        for row in range(self.size):
            for col in range(self.size):
                if (self.m(row, col) == 0):
                    if (self.hm(row, col) < 0):
                        blackScore += 1
                    elif (self.hm(row, col) > 0):
                        whiteScore += 1
        return (whiteScore, blackScore)

        
    def GetMoves(self):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.m(row, col) == 0:
                    moves.append((row, col))
        return moves




def AI(board, color):
    moves = board.GetMoves()
    if not moves:
        return False
    row, col = random.choice(moves)
    if (color == BLACK):
        board.PlacePiece(row, col, BROOK)
    else:
        board.PlacePiece(row, col, WROOK)
        
    return True


def Player(board, color):
    moves = board.GetMoves()
    for i in range(len(moves)):
        print(i, "> ", moves[i])
    selected = -1
    while (selected < 0 or selected >= len(moves)):
        selected = int(input(">>>"))
        
    row, col = moves[selected]
    if (color == BLACK):
        board.PlacePiece(row, col, BROOK)
    else:
        board.PlacePiece(row, col, WROOK)
        
    return True




def xToCol(x):
    return int(x/CELL_W)

def yToRow(y):
    return int(y/CELL_H)    

pygame.init()
b = Board(4)
screen = pygame.display.set_mode((400, 400))

pieces = 8
done = False
gameOver = False
color = WHITE

myfont = pygame.font.SysFont('Comic Sans MS', 30)


pygame.event.set_allowed(None)


while not done:

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    
                    (y,x) = pos
                    (row,col) = (yToRow(y), xToCol(x))

                    ## Special Commands
                    if (row >= b.size or col >= b.size):
                        if (row == b.size and col == 0):
                            b.UpdateHitMatrix()
                            b.GetScore()
                    elif not gameOver and b.m(row, col) == 0:
                        if (color == BLACK):
                            b.PlacePiece(row, col, BROOK)
                        else:
                            b.PlacePiece(row, col, WROOK)
                        color *= -1
                    
                    # clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

        if color == BLACK:
            AI(b, color)
            color *= -1

        b.DrawBoard(screen)
        pygame.display.flip()
        
        if (b.pieces == 4 and not gameOver):
            b.UpdateHitMatrix()
            b.GetScore()
            gameOver = True

        pygame.time.wait(50)





