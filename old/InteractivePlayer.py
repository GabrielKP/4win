# Interactive Player for the 4wins game
# Author: Gabriel Kressin

class Player:
    ''' A player to allow a human to play the 4wins game '''

    def __init__(self, game, pnumber, gui):
        ''' Init function '''

        self.name = "Interactive Player"
        self.game = game
        self.pnumber = pnumber
        self.gui = gui
        self.ncols = self.game.getncols()
        if self.gui != None:
            self.gui._initInteractive()


    def nextTurn(self):
        ''' Returns col in which the next stone should be placed '''
        newPos = -1
        wrongInput = False

        while not self.game.moveLegal(newPos):
            # Get User Input
            if wrongInput:
                print( "{} is not a valid Input! Please type an integer between 0 and {} in a column which is not full!".format(newPos, self.ncols - 1) )
            # Use GUI if it is on
            if self.gui != None:
                newPos = self.gui._getInput()
            else:
                newPos = int(input( "Place a Stone! integer 0-{}: ".format(self.ncols - 1) ))

            wrongInput = True

        return newPos