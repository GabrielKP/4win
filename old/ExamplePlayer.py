# The very Basic Player for a 4wins game
# Author: Gabriel Kressin

class Player:
    ''' A 4wins player template '''

    def __init__(self, game, pnumber):
        ''' Init function '''
        # This function will be called once at the start
        # Here you initialize your player, set up your data structures and
        # if needed for your player you can do some preprocessing

        # Basic Variable setting
        self.name = "Example Player"
        self.game = game
        self.pnumber = pnumber

        # Do your init stuff here

    # Define other functions in here

    def nextTurn(self):
        ''' Returns col in which the next stone should be placed '''
        # This function will be called upon your turn
        # Here you define what happens for each of your turns
        # At the end, an integer in range [0,6] will be expected as return value
        return 4