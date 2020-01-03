#!/usr/bin/python3
# 4 wins
# Authors:
# Gabriel Kressin

import sys, copy, random, importlib

# TODOS:
# Standard Player: Defense, "Attack" and Random placement
# Example Player
# GUI
# Interactive Player
# Check for Winner

class FourWins:
    ''' Includes all Game functions for 4 wins '''

    def __init__(self, playerName1="standard", playerName2="standard"):
        ''' Initializes the Game '''
        # Set Variables
        # The single underscore means you should NOT access those variables!
        # To get the matrix Data use respective getter and setter functions!

        # winner has 4 states:
        self._winner = 0                 # # 0 not determined, 1, 2 if respective player won, 3 for a draw
        self._turns = 0                  # Number of turns
        self._lastStone = None           # Tuple of last placed Stone
        self._matrix = self._matrixCreate()
        self._fullness = self._fullnessCreate()

        # Init players
        self._player1 = self._playerInit(playerName1)
        self._player2 = self._playerInit(playerName2)

        self._currentPlayer = random.randint(1,2)


    def _matrixCreate(self, cols=7, rows=7):
        ''' The Matrix shows where which stone is '''
        # This is how it is adressed:
        # [6][0] [6][1] [6][2] ... [6][6]
        # [5][0] [5][1] ...        [5][6]
        # ...
        # [1][0] [1][1] ...        [1][6]
        # [0][0] [0][1] [0][2] ... [0][6]
        return [[0] * cols for i in range(rows)]


    def matrixGet(self):
        ''' Returns a copy of the Matrix '''
        return copy.deepcopy( self._matrix )


    def matrixGetStone(self, row, col):
        ''' Returns the stone in specific row and column '''
        return self._matrix[row][col]


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
            return mod.StandardPlayer(self)
        # Import and return an Interactive Player
        elif playerName == "interactive":
            mod = importlib.import_module( "InteractivePlayer" )
            return mod.InteractivePlayer(self)
        # Import and return Example Player
        elif playerName == "exampleName":
            # Copy this Code and adapt it to your player
            mod = importlib.import_module( "examplePlayer" )
            return mod.ExamplePlayer(self)
        # In Case of not finding a Player end execution
        else:
            print( "No such player {}, using standard player".format(playerName) )
            sys.exit(-1)


    def _moveLegal(self, pos):
        ''' Check if Player can place another stone '''
        return 0 <= pos and pos <= 6 and self._fullness[pos] < 6


    def _flipPlayer(self, x):
        ''' Flips player Number '''
        if x == 1:
            return 2
        return 1


    def _placeStone(self, pos):
        ''' Places a Stone on pos in matrix '''
        self._matrix[pos][self._fullness[pos]] = self._currentPlayer
        self._lastStone = (pos, self._fullness[pos])
        self._fullness[pos] += 1


    def _gameLoop(self):
        ''' Main Game Loop '''

        while( self._winner == 0 ):
            # 1. Increment Turn
            self._turns +=1
            # 2. Get Placement from Player
            if self._currentPlayer == 1 :
                newPos = self._player1.nextTurn()
            else:
                newPos = self._player2.nextTurn()
            # 3. Check if move was legal, if not, other player won
            if not self._moveLegal( newPos ):
                self._winner = self._flipPlayer( self._currentPlayer )
            # 4. Place the Stone
            self._placeStone( newPos )
            # Check for winner

            # Change Player
            self._currentPlayer = self._flipPlayer( self._currentPlayer )



def main():
    fwins = FourWins()

if __name__ == "__main__":
    main()