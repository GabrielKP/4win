#!/usr/bin/python3
# 4 wins
# Authors:
# Gabriel Kressin

import sys, copy, random, importlib

# TODOS:
# Time measurement
# TEST TEST TEST

class FourWins:
    ''' Includes all Game functions for 4 wins '''

    def __init__(self,
                playerName1="standard",             # Playername of first player
                playerName2="standard",             # Playername of second player
                ncols=7,                            # Number of columns
                nrows=6,                            # Number of rows
                verbose=1,                          # How much output on the console should be given: 0=None, 1=Basic, 2=Extrem
                gui=True                            # GUI
                ):
        ''' Initializes the Game '''
        # Set Variables
        # The single underscore means you should NOT access those variables!
        # To get the matrix Data use respective getter and setter functions!

        self._verbose = verbose
        self._winner = 0                 # # 0 not determined, 1, 2 if respective player won, 3 for a draw
        self._turns = 0                  # Number of turns
        self._lastStone = None           # Tuple of last placed Stone (row, col)
        self._ncols = ncols
        self._nrows = nrows
        self._matrix = self._matrixCreate( self._ncols, self._nrows )
        self._fullness = self._fullnessCreate( self._ncols )
        self._maxTurns = (self._ncols * self._nrows)

        # Init GUI
        self.guiactive = gui
        self._gui = None
        if gui:
            self._initGUI()

        # Init players
        self._player1 = self._playerInit(playerName1, 1)
        self._player2 = self._playerInit(playerName2, 2)

        # Player 1 always begins
        self._currentPlayer = 1

        # Start Game
        self._gameLoop()


    def fprint(self, message, verbosity=1):
        ''' Prints messages depending on verbosity level'''
        # 0 if always printed, 1 for normal, 2 for extended
        if verbosity <= self._verbose:
            return print( message )


    def getMatrix(self):
        ''' Returns a copy of the Matrix '''
        return copy.deepcopy( self._matrix )


    def getStone(self, row, col):
        ''' Returns the stone in specific row and column '''
        return self._matrix[row][col]


    def getLastStone(self):
        ''' Returns last placed Stone '''
        return self._lastStone


    def getnrows(self):
        ''' Returns number of rows '''
        return self._nrows


    def getncols(self):
        ''' Returns number of columns '''
        return self._ncols


    def _fullnessCreate(self, cols):
        ''' The fullness shows how many stones are in a column of the matrix '''
        return [0] * cols


    def getFullness(self):
        ''' Returns a copy of the fullness '''
        return copy.copy( self._fullness )


    def getFullnessCol(self, col):
        ''' Return how many stones are in a specific column '''
        return self._fullness[col]


    def getTurns(self):
        ''' Returns how many turns have happened already '''
        return self._turns


    def moveLegal(self, pos):
        ''' Check if pos is an allowed column to place a stone in '''
        return isinstance(pos, int) and 0 <= pos and pos < self._ncols and self._fullness[pos] <= 6


    def _initGUI(self):
        ''' Initiliazes GUI '''
        mod = importlib.import_module( "gui" )
        self._gui = mod.GUI( game=self )


    def _playerInit(self, playerName, pnumber):
        ''' Initializes and imports Player Object, respective player file needs to be included above '''
        # Import and return Standard Player
        try:
            if playerName == "InteractivePlayer":
                mod = importlib.import_module( playerName )
                return mod.Player(self, pnumber, self._gui)
            else:
                mod = importlib.import_module( playerName )
                return mod.Player(self, pnumber)
        except:
            self.fprint( "No such player as \"{}\", aborting".format(playerName), 0 )
            sys.exit(-1)


    def _matrixCreate(self, cols, rows):
        ''' The Matrix shows where which stone is '''
        # This is how it is adressed:
        # [6][0] [6][1] [6][2] ... [6][6]
        # [5][0] [5][1] ...        [5][6]
        # ...
        # [1][0] [1][1] ...        [1][6]
        # [0][0] [0][1] [0][2] ... [0][6]
        return [[0] * cols for i in range(rows)]


    def _matrixPrint(self):
        ''' Prints the entire Matrix '''
        message = '\n'.join([' '.join(str(x) for x in row) for row in reversed(self._matrix)])
        self.fprint(message, 2)


    def _fullnessCreate(self, cols):
        ''' The fullness shows how many stones are in a column of the matrix '''
        return [0] * cols


    def _flipPlayer(self, x):
        ''' Flips player Number '''
        if x == 1:
            self.fprint( "flipPlayer: Flipped player from {} to {}".format(1, 2), 3 )
            return 2
        self.fprint( "flipPlayer: Flipped player from {} to {}".format(2, 1), 3 )
        return 1


    def _placeStone(self, pos):
        ''' Places a Stone on pos in matrix '''
        self._matrix[self._fullness[pos]][pos] = self._currentPlayer
        self._lastStone = (self._fullness[pos], pos)
        self.fprint( "placeStone: Placed Stone to {:2}, {:2}".format(self._fullness[pos], pos), 3 )
        self._fullness[pos] += 1


    def _checkWinner(self):
        ''' If 4 in a row, sets _winner to current player '''
        lrow, lcol = self._lastStone
        self.fprint( "checkWinner: Laststone {:2}, {:2}".format(lrow, lcol), 3 )

        ### Vertical
        counter = 0
        # Cant be vertical 4 in the row if the last stone is not in 4th row
        if lrow >= 3:
            curr = lrow - 1
            # Count how many same colored stones are under last stone
            while self.getStone(curr, lcol) == self._currentPlayer and counter < 3:
                counter += 1
                curr -= 1
            if counter == 3:
                self._winner = self._currentPlayer
                self.fprint( "checkWinner: Player {} won: 4 vertical stones starting in position {:2}, {:2}".format(self._currentPlayer, curr + 1, lcol), 3 )
                return
        self.fprint( "checkWinner: Did not find 4 in a vertical row!", 3 )

        ### Horizontal
        counter = 0
        sLeft = max(0, lcol - 3)
        sRight = min(self._nrows - 1, lcol + 3)
        # Count how many same colored stones are between sLeft and sRight
        curr = sLeft
        while curr <= sRight and counter < 4:
            if self.getStone(lrow, curr) == self._currentPlayer:
                counter += 1
            else:
                counter = 0
            curr += 1
        if counter == 4:
            self._winner = self._currentPlayer
            self.fprint( "checkWinner: Player {} won: 4 horizontal stones starting in position {:2}, {:2}".format(self._currentPlayer, lrow, curr - 1), 3 )
            return
        self.fprint( "checkWinner: Did not find 4 in a horizontal row!", 3 )

        ### Diagonal NW -> SE
        # Get to NW point
        ccol = max(0, lcol - 3)
        crow = lrow + lcol - ccol
        # Corner case when you are too far up
        if crow >= self._nrows:
            correction = crow - (self._nrows - 1)
            ccol += correction
            crow -= correction
        # Determine ending fields
        erow = max(0, lrow - 3)
        ecol = min(self._ncols - 1, lcol + 3)
        # Count amount of stones in the diagonal
        counter = 0
        while crow >= erow and ccol <= ecol and counter < 4:
            if self.getStone(crow, ccol) == self._currentPlayer:
                counter += 1
            else:
                counter = 0
            crow -= 1
            ccol += 1
        if counter == 4:
            self._winner = self._currentPlayer
            self.fprint( "checkWinner: Player {} won: 4 diagonal SE to NW stones starting in position {:2}, {:2}".format(self._currentPlayer, crow + 1, ccol - 1), 3 )
            return
        self.fprint( "checkWinner: Did not find 4 in a diagonal NW to SE row!", 3 )

        ### Diagonal SW -> NE
        # Get to SW point
        ccol = max(0, lcol - 3)
        crow = lrow - lcol + ccol
        # Corner case when you are too far down
        if crow < 0:
            ccol -= crow
            crow = 0
        # Determine ending col / row for check
        erow = min(self._nrows - 1, lrow + 3)
        ecol = min(self._ncols - 1, lcol + 3)
        # Count amount of stones in the diagonal
        counter = 0
        while ccol <= ecol and crow <= erow and counter < 4:
            if self.getStone(crow, ccol) == self._currentPlayer:
                counter += 1
            else:
                counter = 0
            crow += 1
            ccol += 1
        if counter == 4:
            self._winner = self._currentPlayer
            self.fprint( "checkWinner: Player {} won: 4 diagonal NE to SW stones starting in position {:2}, {:2}".format(self._currentPlayer, crow - 1, ccol - 1), 3 )
            return
        self.fprint( "checkWinner: Did not find 4 in a diagonal SW to NE row!", 3 )
        # No winner was found
        self.fprint( "checkWinner: Did not find 4 in the row.", 3 )
        return


    def _gameLoop(self):
        ''' Main Game Loop '''
        # Execute each turn in this loop
        while( self._winner == 0 and self._turns < self._maxTurns):
            # 1. Increment Turn
            self._turns +=1
            self.fprint( "Game: -- Turn {:2} --".format(self._turns) )
            # 2. Get Placement from Player
            self.fprint( "Game: Turn of player {}: \"{}\" ".format(self._currentPlayer, self._player1.name if self._currentPlayer == 1 else self._player2.name) )
            if self._currentPlayer == 1 :
                newPos = self._player1.nextTurn()
            else:
                newPos = self._player2.nextTurn()
            self.fprint( "Game: Player {}: \"{}\" placed in column {}".format(self._currentPlayer, self._player1.name if self._currentPlayer == 1 else self._player2.name, newPos) )
            # 3. Check if move was legal, if not, other player won
            if not self.moveLegal( newPos ):
                self._winner = self._flipPlayer( self._currentPlayer )
                self.fprint( "Game: Placement was illegal!" )
            # 4. Place the Stone
            self._placeStone( newPos )
            # Draw Gameboard and print matrix
            self._matrixPrint()
            if self.guiactive:
                self._gui.update( self._lastStone, self._currentPlayer )
            # Check for winner
            self.fprint( "Game: Entering checkWinner()", 3 )
            self._checkWinner()
            if self._winner != 0:
                break
            # Change Player
            self._currentPlayer = self._flipPlayer( self._currentPlayer )

        if self._turns == self._maxTurns:
            self._winner = 3
            drawMessage = "Game: Draw! Nobody looses or wins!"
            self.fprint( drawMessage )
            if self.guiactive:
                self._gui._displayMessage(drawMessage[6:])
                self._gui._getInput()
        else:
            winMessage = "Game: Player {}: \"{}\" wins after {:2} turns!".format(self._currentPlayer, self._player1.name if self._currentPlayer == 1 else self._player2.name, self._turns)
            self.fprint( winMessage )
            if self.guiactive:
                self._gui._displayMessage(winMessage[6:])
                self._gui._getInput()

        return self._winner



def main():
    FourWins(verbose=3, playerName1="StandardPlayer", playerName2="InteractivePlayer", gui=True)

if __name__ == "__main__":
    main()