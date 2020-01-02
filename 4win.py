#!/usr/bin/python3
# 4 wins
# Authors:
# Gabriel Kressin

import sys, copy, random, importlib

class FourWins:
    ''' Includes all Game functions for 4 wins '''

    def __init__(self, playerName1="standard", playerName2="standard"):
        ''' Initializes the Game '''
        # Set Variables

        # The single underscore means you should NOT access those variables!
        # To get the matrix Data use respective getter and setter functions!
        self._matrix = self._matrixCreate()
        self._fullness = self._fullnessCreate()

        # Init players
        self.player1 = self._playerInit(playerName1)
        self.player2 = self._playerInit(playerName2)

        self.playerOnTurn()


    def _matrixCreate(self, cols=7, rows=7):
        ''' The Matrix shows where which stone is '''
        # This is how it is adressed:
        # [0][0] [0][1] [0][2] ... [0][6]
        # [1][0] ...
        # ...
        # [6][0] ...           ... [6][6]
        return [[0] * cols for i in range(rows)]

    def matrixGet(self):
        ''' Returns a copy of the Matrix '''
        return copy.deepcopy( self._matrix )

    def matrixGetStone(self, col, row):
        ''' Returns the stone in specific row and column '''
        return self._matrix[col][row]

    def _fullnessCreate(self, cols=7):
        ''' The fullness shows how many stones are in a column of the matrix '''
        return [0] * cols

    def fullnessGet(self):
        ''' Returns a copy of the fullness '''
        return copy.copy( self._fullness )

    def _playerInit(self, playerName):
        ''' Initializes and imports Player Object, respective player file needs to be included above '''

        # Import and return Standard Player
        if playerName == "standard":
            mod = importlib.import_module( "StandardPlayer" )
            return mod.StandardPlayer()
        # Import and return an Interactive Player
        elif playerName == "interactive":
            mod = importlib.import_module( "InteractivePlayer" )
            return mod.InteractivePlayer()
        # Import and return Example Player
        elif playerName == "exampleName":
            # Copy this Code and adapt it to your player
            mod = importlib.import_module( "examplePlayer" )
            return mod.ExamplePlayer()
        # In Case of not finding a Player end execution
        else:
            print( "No such player {}, using standard player".format(playerName) )
            sys.exit(-1)



def main():
    fwins = FourWins()

if __name__ == "__main__":
    main()