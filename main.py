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
        p1/p2 are functions which get the board, the fullness and last history
        """

        self._p1 = p1
        self._p2 = p2
        self._verbose = verbose
        self._HEIGHT = 6
        self._WIDTH = 7
        self._moves = [] * self._SIZE
        self._SIZE = self._HEIGHT * self._WIDTH
        self._reset()


    def _reset( self ):
        """
        Resets Gameboard
        """
        self._board = [0] * 2
        self._turns = 0
        self._fullness = [0] * self._WIDTH


    def _makemove( self, column ):
        """
        Places a stone in column
        """
        if self.islegal( column ):
            self._board[self._turns & 1] = self._fullness[column]


    def islegal( self, column ):
        """
        Checks if stone placement is legal
        """