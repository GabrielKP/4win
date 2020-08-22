# Player functions for 4wins

import random
import copy
import sys

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


class GabrielPlayer:


    class GameState:
        """
        Gamestate represents a specific state of the game with
        both boards, the height and the amount of turns
        """

        def __init__( self, boards, height, turns, bc ):
            self.boards = boards
            self.height = height
            self.turns = turns
            self.bc = bc


    def __init__( self, steps = 11, verbose = 0 ):
        self._verbose = verbose
        self._STEPS = steps
        self._HEIGHT = 6
        self._WIDTH = 7
        self._H1 = self._HEIGHT + 1
        self._SIZE = self._HEIGHT * self._WIDTH
        self._shifts = []
        self._shifts.append( self._HEIGHT ) # Diagonal \
        self._shifts.append( self._H1 + 1 ) # Diagonal /
        self._shifts.append( self._H1 )     # Horizontal -
        self._shifts.append( 1 )            # Vertikal |
        self._maxHeight = [ 5,12,19,26,33,40,47 ]

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
            if height[col] < self._maxHeight[col]:
                newboard = board ^ ( 1 << height[col] )
                if self._canWin( newboard ):
                    return col
        return -1


    def _printBoard( self, boards ):
        """
        Prints board
        """
        b0 = bin( boards[0] )
        b0len = len(b0) - 2
        b1 = bin( boards[1] )
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
        print( '\n'.join( [ ' '.join( row ) for row in reversed( matrix ) ] ) )


    def _boardcode( self, boards, turns ):
        """
        Returns unique code for each board
        """
        return boards[turns & 1] + boards[0] + boards[1]


    def _backtrack( self, gamestate, stepsLeft ):
        """
        Go stepsLeft deep into the tree of possible gamestates
        and compute scores for them
        """
        bc = gamestate.bc
        currentp = gamestate.turns & 1

        if self._canWin( gamestate.boards[0] ): # 1. Check for win player 0
            ret = [10 * stepsLeft, 0]
            self._statedic[bc] = ret
            return ret

        if self._canWin( gamestate.boards[1] ): # 2. Check for win player 1
            ret = [0, 10 * stepsLeft]
            self._statedic[bc] = ret
            return ret

        if stepsLeft == 0:                      # 3. Recursion Anker
            self._statedic[bc] = [0, 0]
            return [0, 0]

        ret = [0, 0]                            # 4. Substates
        for col in range( 0, self._WIDTH ):
            if gamestate.height[col] < self._maxHeight[col]:
                newboards = gamestate.boards[:]
                newboards[currentp] = gamestate.boards[currentp] ^ ( 1 << gamestate.height[col] )
                newheight = gamestate.height[:]
                newheight[col] += 1
                # No state creation needed if it is in dic already
                newbc = newboards[(gamestate.turns + 1) & 1] + newboards[0] + newboards[1]
                if newbc in self._statedic:
                    p1, p2 = self._statedic[newbc]
                else:
                    newstate = self.GameState( newboards, newheight, gamestate.turns + 1, newbc )
                    p1, p2 = self._backtrack( newstate, stepsLeft - 1 )
                ret[0] += p1
                ret[1] += p2

        self._statedic[bc] = ret
        return ret


    def nextMove( self, turns, boards, height, moves ):
        """
        determines the next move
        """
        currentp = turns & 1
        enemyp = ( currentp + 1) % 2

        # 1. Check if winnable
        res = self._checkPositions( boards[currentp], height )
        if res != -1:
            return res
        # 2. Check if enemy can win somewhere
        res = self._checkPositions( boards[enemyp], height )
        if res != -1:
            return res

        # Create current game as Node:
        root = self.GameState( boards, height, turns, self._boardcode( boards, turns ) )

        self._statedic = {}
        for col in range( 0, self._WIDTH ):
            if root.height[col] < self._maxHeight[col]:
                newboards = root.boards[:]
                newboards[currentp] = root.boards[currentp] ^ ( 1 << root.height[col] )
                newheight = root.height[:]
                newheight[col] += 1
                newbc = newboards[(root.turns + 1) & 1] + newboards[0] + newboards[1]
                if newbc in self._statedic:
                    ret = self._statedic[newbc]
                else:
                    newstate = self.GameState( newboards, newheight, root.turns + 1, newbc )
                    ret = self._backtrack( newstate, self._STEPS )
                print( "Col {}: {}".format( col, ret ) )

        return 0
