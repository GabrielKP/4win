# The very Basic Player for a 4wins game
# Author: Gabriel Kressin

import random

class StandardPlayer:
    ''' A basic 4wins player '''

    def __init__(self, game):
        ''' Init function '''

        self.name = "Standard Player"
        self.game = game
        self.pnumber = pnumber
        self._lastOwnPlacedCol = -1


    def nextTurn(self):
        ''' Returns col in which the next stone should be placed '''