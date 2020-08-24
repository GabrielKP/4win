# Player functions for 4wins

import random
import copy
import sys
import multiprocessing as mp

WIDTH = 7
HEIGHT = 6


def boards2matrix( boards ):
    """
    Returns a matrix given boards
    """
    H1 = HEIGHT + 1
    b0 = bin( boards[0] )
    b0len = len( b0 )
    b1 = bin( boards[1] )
    b1len = len( b1 )
    matrix = [ ["0"] * WIDTH for x in range( HEIGHT ) ]
    for r in range( HEIGHT ):
        for c in range( WIDTH ):
            pos = c * H1 + r
            if b0len > pos and b0[-pos - 1] == '1':
                matrix[r][c] = "1"
            elif b1len > pos and b1[-pos - 1] == '1':
                matrix[r][c] = "2"
            else:
                matrix[r][c] = "0"

    return matrix


def printBoards( boards ):
        """
        Prints the game in console given "boards"
        """
        H1 = HEIGHT + 1
        b0 = bin( boards[0] )
        b0len = len(b0) - 2
        b1 = bin( boards[1] )
        b1len = len(b1) - 2
        matrix = [ ["0"] * WIDTH for x in range( HEIGHT ) ]
        for r in range( HEIGHT ):
            for c in range( WIDTH ):
                pos = c * H1 + r
                if b0len > pos and b0[-pos - 1] == '1':
                    matrix[r][c] = "1"
                elif b1len > pos and b1[-pos - 1] == '1':
                    matrix[r][c] = "2"
                else:
                    matrix[r][c] = "0"
        print( '\n'.join( [ ' '.join( row ) for row in reversed( matrix ) ] ) )


def interactivePlayer( turns, x, y, moves ):
    """
    waits for console input, does not have error handling
    """
    return int( input( "Player {}! Input a number between 0 and 6!".format( ( turns & 1 ) + 1 ) ) )


def randomPlayer( turns, boards, height, moves ):
    """
    plays randomly unless enemy can win or itself can win
    """
    H1 = HEIGHT + 1
    while True:
        newcol = random.randint( 0, WIDTH - 1 )
        if( height[newcol] < ( newcol + 1 ) * H1 - 1 ):
            return newcol


class GabrielPlayer:
    """
    multicore connect 4 player, steps is how many steaps ahead the player will look
    """
    # Improvements:
    # - Better score computation
    #   - (Taking difference is too simple)
    #   - Special cases score bonus( zwickmühle )
    # - procedural statedic synchronisation between processes
    # - Adaptive amount of steps
    #   - Heuristic when to use more, when less


    def __init__( self, steps = 9, verbose = 0 ):
        self._verbose = verbose
        self._STEPS = steps
        self._HEIGHT = HEIGHT
        self._WIDTH = WIDTH
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
            if height[col] < self._maxHeight[col]:
                newboard = board ^ ( 1 << height[col] )
                if self._canWin( newboard ):
                    return col
        return -1


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
        modifier = (stepsLeft + 1) ** 4
        boards = gamestate[0]
        height = gamestate[1]
        turns = gamestate[2]
        bc = gamestate[3]
        currentp = turns & 1

        if self._canWin( boards[0] ): # 1. Check for win player 0
            ret = [modifier, 0]
            self._statedic[bc] = ret
            return ret

        if self._canWin( boards[1] ): # 2. Check for win player 1
            ret = [0, modifier]
            self._statedic[bc] = ret
            return ret

        if stepsLeft == 0:                      # 3. Recursion Anker
            self._statedic[bc] = [0, 0]
            return [0, 0]

        ret = [0, 0]                            # 4. Substates
        for col in range( 0, self._WIDTH ):
            if height[col] < self._maxHeight[col]:
                newboards = boards[:]
                newboards[currentp] = boards[currentp] ^ ( 1 << height[col] )
                newheight = height[:]
                newheight[col] += 1
                # No repeated function call needed if it is in dic already
                newbc = newboards[(turns + 1) & 1] + newboards[0] + newboards[1]
                if newbc in self._statedic:
                    p1, p2 = self._statedic[newbc]
                else:
                    newstate = ( newboards, newheight, turns + 1, newbc, )
                    p1, p2 = self._backtrack( newstate, stepsLeft - 1 )
                ret[0] += p1
                ret[1] += p2

        self._statedic[bc] = ret
        return ret


    def _startBacktrack( self, column, gamestate, turns, plock, result ):
        """
        Starts Backtrace on its own, meant to be called by own process
        """
        currentp = turns & 1
        ret = self._backtrack( gamestate, self._STEPS )
        score = currentp * ( ret[1] - ret[0] )  + ( not currentp ) * ( ret[1] - ret[0])
        result.put( ( score, column ) )
        plock.acquire()
        print( "Column {}: {}, score {}".format( column, ret, score ) )
        plock.release()
        return 0


    def nextMove( self, turns, boards, height, moves ):
        """
        determines the next move
        """
        currentp = turns & 1
        enemyp = ( currentp + 1) % 2

        # 1. Check if winnable
        res = self._checkPositions( boards[currentp], height )
        if res != -1:
            print( "Placing in column {}".format( res ) )
            return res
        # 2. Check if enemy can win somewhere
        res = self._checkPositions( boards[enemyp], height )
        if res != -1:
            print( "Placing in column {}".format( res ) )
            return res

        # Create current game as Tupel:
        root = ( boards, height, turns, self._boardcode( boards, turns ), )

        self._statedic = {}

        result = mp.Queue( 7 )
        ps = []
        plock = mp.Lock()

        for col in range( 0, self._WIDTH ):
            if root[1][col] < self._maxHeight[col]:
                # Prepare new state
                newboards = root[0][:]
                newboards[currentp] = root[0][currentp] ^ ( 1 << root[1][col] )
                newheight = root[1][:]
                newheight[col] += 1
                newbc = newboards[(root[2] + 1) & 1] + newboards[0] + newboards[1]
                newstate = ( newboards, newheight, root[2] + 1, newbc, )

                # init process
                p = mp.Process( target=self._startBacktrack, args=( col, newstate, turns, plock, result, ) )
                p.start()
                ps.append( p )

        # Wait for processes to finish
        for p in ps:
            p.join()

        maxval, newcol = result.get()
        while not result.empty():
            sr = result.get()
            if sr[0] > maxval:
                maxval, newcol = sr

        print( "Placing in column {}".format( newcol ) )

        return newcol
