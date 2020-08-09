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

        self._p1 = p1
        self._p2 = p2
        self._verbose = verbose
        self._HEIGHT = 6
        self._WIDTH = 7
        self._H1 = self._HEIGHT + 1
        self._moves = [] * self._SIZE
        self._SIZE = self._HEIGHT * self._WIDTH
        self._reset()


    def _reset( self ):
        """
        Resets Gameboard
        """
        self._board = [0] * 2
        self._turns = 0
        self._height = [ self._H1 * i for i in range( self._HEIGHT ) ]


    def _makemove( self, column ):
        """
        Places a stone in column
        """
        if self.islegal( column ):
            self._board[self._turns & 1] = self._height[column]


    def islegal( self, column ):
        """
        Checks if stone placement is legal
        """

def main():
    print( "Hello World!" )


if __name__ == "__main__":
    main()