#!/usr/bin/python3
# Implementation of a connect 4 game in python.
# Inspired by John Tromp: https://tromp.github.io/c4/c4.html

import sys

class FourWins:
    """
    Basic connect 4 game
    """

    def __init__( self, p1, p2, verbose ):
        """
        Initialize the board, set the variables
        p1/p2 are functions which get the board, the height and last history
        """

        self._players = [p1, p2]
        self._verbose = verbose
        self._HEIGHT = 6
        self._WIDTH = 7
        self._H1 = self._HEIGHT + 1
        self._SIZE = self._HEIGHT * self._WIDTH
        self._moves = [] * self._SIZE
        self._reset()


    def _reset( self ):
        """
        Resets Gameboard
        """
        self._board = [0] * 2
        self._turns = 0
        self._height = [ self._H1 * i for i in range( self._WIDTH ) ]
        print( self._height )


    def _makemove( self, column ):
        """
        Places a stone in column
        """
        self._board[self._turns & 1] = 1 << self._height[column]
        self._height[column] += 1
        self._moves[self._turns] = column
        self._turns += 1


    def _islegal( self, column ):
        """
        Checks if stone placement is legal
        """
        return isinstance( column, int ) and column >= 0 and column < self._WIDTH and self._height[column] < ( column + 1 ) * self._H1 - 1


    def _haswon( self ):
        """
        Checks if current player has won
        """
        return False


    def _terminate( self, player ):
        """
        Function to terminate game
        """
        print( "Player {} has won!".format( player + 1 ) )


    def _gameLoop( self ):
        """
        Main loop for game:
        1. Get column from player
        2. Place stone
        3. Check for winner
        """
        while self._turns < self._SIZE:
            # 1
            curr_player = self._turns & 1
            newcol = self._players[curr_player]( curr_player, self._board, self._height, self._moves )
            # 2
            if not self._islegal( newcol ):
                self._terminate( self._turns + 1 & 1 )
                return
            self._makemove( newcol )
            # 3
            if self._haswon():
                self._terminate( curr_player )
                return



def main():
    FourWins( None, None, 1 )


if __name__ == "__main__":
    main()