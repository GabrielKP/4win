#!/usr/bin/python3
# Implementation of a connect 4 game in python.
# Inspired by John Tromp: https://tromp.github.io/c4/c4.html

import sys
from player import *

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
        self._moves = []
        self._reset()
        self._gameLoop()


    def _reset( self ):
        """
        Resets Gameboard
        """
        self._board = [0] * 2
        self._turns = 0
        self._height = [ self._H1 * i for i in range( self._WIDTH ) ]


    def _makemove( self, column ):
        """
        Places a stone in column
        """
        self._board[self._turns & 1] ^= 1 << self._height[column]
        self._height[column] += 1
        self._moves.append( column )


    def _islegal( self, column ):
        """
        Checks if stone placement is legal
        """
        return isinstance( column, int ) and column >= 0 and column < self._WIDTH and self._height[column] < ( column + 1 ) * self._H1 - 1


    def _haswon( self ):
        """
        Checks if current player has won
        """
        cboard = self._board[self._turns & 1]

        # Diagonal \
        shifted = ( cboard >> self._HEIGHT ) & cboard
        if( shifted & ( shifted >> self._HEIGHT * 2 ) != 0 ):
            return True

        # Diagonal /
        shifted = ( cboard >> ( self._H1 + 1 ) ) & cboard
        if( shifted & ( shifted >> ( self._H1 + 1 ) * 2 ) != 0 ):
            return True

        # Horizontal -
        shifted = ( cboard >> self._H1 ) & cboard
        if( shifted & ( shifted >> self._H1 * 2 ) != 0 ):
            return True

        # Vertical |
        shifted = ( cboard >> 1 ) & cboard
        if( shifted & ( shifted >> 2 ) != 0 ):
            return True

        return False


    def _terminate( self, player ):
        """
        Function to terminate game
        """
        self._printBoard()
        print( "Player {} has won!".format( player + 1 ) )


    def _printBoard( self ):
        """
        Prints board
        """
        b0 = bin( self._board[0] )
        b0len = len(b0) - 2
        b1 = bin( self._board[1] )
        b1len = len(b1) - 2
        matrix = [ ["0"] * self._WIDTH for x in range( self._HEIGHT ) ]
        for r in range( self._HEIGHT ):
            for c in range( self._WIDTH ):
                pos = c * self._H1 + r
                if b0len > pos and b0[-pos - 1] == '1':
                    matrix[r][c] = "1"
                elif b1len > pos and b1[-pos - 1] == '1':
                    matrix[r][c] = "2"
                else:
                    matrix[r][c] = "0"
        print( " Turn ", self._turns )
        print( '\n'.join( [ ' '.join( row ) for row in reversed( matrix ) ] ) )


    def _gameLoop( self ):
        """
        Main loop for game:
        0. Print or draw
        1. Get column from player
        2. Place stone
        3. Check for winner
        """
        while self._turns < self._SIZE:
            # 0
            if self._verbose > 0:
                self._printBoard()
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
            self._turns += 1


def main():
    FourWins( interactivePlayer, randomPlayer, 1 )


if __name__ == "__main__":
    main()