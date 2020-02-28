# Interactive Player for the 4wins game
# Author: Gabriel Kressin

class InteractivePlayer:
    ''' A player to allow a human to play the 4wins game '''

    def __init__(self, game, pnumber):
        ''' Init function '''

        self.name = "Interactive Player"
        self.game = game
        self.pnumber = pnumber
        self.gui = self.game.gui
        self.gui._initInteractive()


    def nextTurn(self):
        ''' Returns col in which the next stone should be placed '''
        newPos = -1
        wrongInput = False

        while not self.game.moveLegal(newPos):
            # Get User Input
            if wrongInput:
                print( "{} is not a valid Input! Please type an integer between 0 and 6 in a column which is not full!".format(newPos) )
            # Console
            # newPos = int(input( "Place a Stone! integer 0-6: " ))
            # GUI
            newPos = self.gui._getInput()

            wrongInput = True

        return newPos