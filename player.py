# Player functions for 4wins

import random

def interactivePlayer( turns, x, y, moves ):
    return int( input( "Player {}! Input a number between 0 and 6!".format( ( turns & 1 ) + 1 ) ) )


def randomPlayer( turns, boards, height, moves ):
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
