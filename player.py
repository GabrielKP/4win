# Player functions for 4wins

import random

def interactivePlayer( player, x, y, moves ):
    return int( input( "Player {}! Input a number between 0 and 6!".format( player + 1 ) ) )


def randomPlayer( player, boards, height, moves ):
    """
    plays randomly unless enemy can win or heself can win
    """
    HEIGHT = 6
    H1 = HEIGHT + 1
    WIDTH = 7
    while True:
        newcol = random.randint( 0, WIDTH - 1 )
        if( height[newcol] < ( newcol + 1 ) * H1 - 1 ):
            return newcol


class gabrielPlayer:


    def __init__( self, verbose = 0 ):
        self._verbose = verbose
        self._HEIGHT = 6
        self._WIDTH = 7
        self._H1 = self._HEIGHT + 1
        self._SIZE = self._HEIGHT * self._WIDTH
        self._shifts = []
        self._shifts.append( self._HEIGHT ) # Diagonal \
        self._shifts.append( self._H1 + 1 ) # Diagonal /
        self._shifts.append( self._H1 )     # Horizontal -
        self._shifts.append( 1 )            # Vertikal |
        self._maxHeight = [ 6,13,20,27,34,41,48 ]

        # 6 13 20 27 34 41 48 55
        # 5 12 19 26 33 40 47 54
        # 4 11 18 25 32 39 46 53
        # 3 10 17 24 31 38 45 52
        # 2  9 16 23 30 37 44 51
        # 1  8 15 22 29 36 43 50
        # 0  7 14 21 28 35 42 49


    def _canWin( self, board ):
        """
        Checks if given board has 4 in the row
        """
        for shift in self._shifts:
            shifted = ( board >> shift ) & board
            if( shifted & ( shifted >> shift * 2 ) != 0 ):
                return True
        return False


    def _checkPositions( self, board, height ):
        """
        Checks every position
        """
        for col in range( self._WIDTH ):
            if height[col] != self._maxHeight:
                newboard = board ^ ( 1 << height[col] )
                if self._canWin( newboard ):
                    return col
        return -1


    def nextMove( self, pnum, boards, height, moves ):
        """
        determines the next move
        """
        myboard = boards[pnum]
        # 1. Check if winnable
        res = self._checkPositions( myboard, height )
        if res != -1:
            return res
        # 2. Check if enemy can win somewhere

        return 0
