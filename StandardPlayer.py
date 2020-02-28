# The very Basic Player for a 4wins game
# Author: Gabriel Kressin

import random

class StandardPlayer:
    ''' A basic 4wins player '''

    def __init__(self, game, pnumber):
        ''' Init function '''

        self.name = "Standard Player"
        self.game = game
        self.pnumber = pnumber
        self._lastOwnPlacedCol = -1


    def nextTurn(self):
        ''' Returns col in which the next stone should be placed '''
        winCol = self.tryWin()
        if winCol != -1:
            self._lastOwnPlacedCol = winCol
            return winCol

        defCol = self.tryDef()
        if defCol != -1:
            self._lastOwnPlacedCol = defCol
            return defCol
        
        newPos = -1
        while self.game.moveLegal(newPos):
            newPos = random.randint(0,6)
        self._lastOwnPlacedCol = newPos
        return newPos


    def tryWin(self):
        ''' Returns the column to place stone, when player can win there, if not -1 '''
        # Check for "affected" places if you
        # a. can place a stone there
        # b. you can win with that stone

        # "affected" Places are determined by the two last placed stones:
        # 1. The place above enemies placed stone
        # 2. Horizontal/Vertical/Diagonal Places from own last placed stone

        # 1. Check Place above enemies placed stone
        lrow, lcol = self.game.getLastStone()
        # Check Horizontal
        endCol = min(6, lcol + 3)
        ccol = max(0, lcol - 3)
        count = 0
        while ccol < endCol and count < 4:
            if self.game.getStone(lrow + 1, ccol) == self.pnumber or ccol == lcol:
                count += 1
            else:
                count = 0
        if count == 4:
            return lcol
        # Check Diagonal

        return -1


    def tryDef(self):
        ''' Returns col if Player needs to defend from other player placing 4 in the row, if not -1 '''