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


    def canWinAtPos(self, lrow, lcol, player):
        ''' Check if player can win if stone placed at lrow, lcol '''
        # Check Vertical
        counter = 0
        if lrow >= 3:
            crow = lrow - 1
            while self.game.getStone(crow, lcol) == player and counter < 3:
                counter += 1
                crow -= 1
            if counter == 3:
                return True

        # Check Horizontal
        endCol = min(6, lcol + 3)
        ccol = max(0, lcol - 3)
        counter = 0
        while ccol <= endCol and counter < 4:
            if self.game.getStone(lrow, ccol) == player or ccol == lcol:
                counter += 1
            else:
                counter = 0
            ccol += 1
        if counter == 4:
            return True

        # Check Diagonal UPLEFT -> DOWNRIGHT (NW -> SE)
        # Determine NW point
        ccol = max(0, lcol - 3)
        crow = lrow + lcol - ccol
        # Corner case when you are too far up
        if crow >= 7:
            correction = crow - 6
            ccol += correction
            crow -= correction
        # Determine ending fields
        erow = max(0, lrow - 3)
        ecol = min(self.game._ncols - 1, lcol + 3)
        # Count amount of stones in the diagonal
        counter = 0
        while crow >= erow and ccol <= ecol and counter < 4:
            if self.game.getStone(crow, ccol) == player or ccol == lcol:
                counter += 1
            else:
                counter = 0
            crow -= 1
            ccol += 1
        if counter == 4:
            return True

        # Check Diagonal DOWNLEFT -> UPRIGHT (SW -> NE)
        # Determine SW point
        ccol = max(0, lcol - 3)
        crow = lrow - lcol + ccol
        # Corner case when you are too far down
        if crow < 0:
            ccol -= crow
            crow = 0
        # Determine ending col / row for check
        erow = min(6, lrow + 3)
        ecol = min(6, lcol + 3)
        # Count amount of stones in the diagonal
        counter = 0
        while ccol <= ecol and crow <= ecol and counter < 4:
            if self.game.getStone(crow, ccol) == player or ccol == lcol:
                counter += 1
            else:
                counter = 0
            crow += 1
            ccol += 1
        if counter == 4:
            return True
        return False


    def tryWin(self):
        ''' Returns the column to place stone, when player can win there, if not -1 '''
        # Check every position stone can be placed in
        for col in range(0, self.game._ncols):
            row = self.game.getFullnessCol(col)
            if row == 7:
                continue
            if self.canWinAtPos(row, col, self.pnumber):
                return col

        return -1


    def tryDef(self):
        ''' Returns col if Player needs to defend from other player placing 4 in the row, if not -1 '''
        enemy = (self.pnumber % 2) + 1
        # Check every position enemy can place stone in
        for col in range(0, self.game._ncols):
            row = self.game.getFullnessCol(col)
            if row == 7:
                continue
            if self.canWinAtPos(row, col, enemy):
                return col

        return -1


    def nextTurn(self):
        ''' Returns col in which the next stone should be placed '''
        winCol = self.tryWin()
        if winCol != -1:
            return winCol

        defCol = self.tryDef()
        if defCol != -1:
            return defCol

        newPos = -1
        while not self.game.moveLegal(newPos):
            newPos = random.randint(0,6)
        return newPos