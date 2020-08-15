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

    def canWin( self, board ):
        """
        Checks if given board has 4 in the row
        """
        for shift in self._shifts:
            shifted = ( board >> shift ) & board
            if( shifted & ( shifted >> shift * 2 ) != 0 ):
                return True
        return False


    def nextMove( self, pnum, boards, height, moves ):
        """
        determines the next move
        """
        # 1. Check if winnable
        # 2. Check if enemy can win somewhere

        return 0
