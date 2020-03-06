# The professional Player for a 4wins game
# Author: Janek Belka

class Player:
    ''' A 4wins player template '''

    def __init__(self, game, pnumber):
        ''' Init function '''
        # This function will be called once at the start
        # Here you initialize your player, set up your data structures and
        # if needed for your player you can do some preprocessing

        # Basic Variable setting
        self.name = "JanekPlayer"
        self.game = game
        self.pnumber = pnumber

        # Do your init stuff here

    def abfrage(self):
        matrix = self.game.getMatrix()
        print (matrix)

    def test(self,sp,re,player):

        #Vertikaler Check
        i = 0
        if re >= 3:
            aRe = re - 1
            while self.game.getStone(aRe, sp) == player and i < 3:
                i += 1
                aRe -= 1
            if i == 3:
                return True

        #Horizontaler Check
        i = 0
        rEndSp = min(6, sp + 3)
        lEndSp = max(0, sp - 3)

        while lEndSp < rEndSp and i < 4:
            if self.game.getStone(re,lEndSp) == player or lEndSp == sp:
                i += 1
            else:
                i = 0
            lEndSp +=1
        if i == 4:
            return True

        #Diagonaler Check




    def testWin (self):
        #

    def testLoose(self):
        #

    # Define other functions in here

    def nextTurn(self):
        ''' Returns col in which the next stone should be placed '''
        # This function will be called upon your turn
        # Here you define what happens for each of your turns
        # At the end, an integer in range [0,6] will be expected as return value
        return 4

#def main():
#    JanekPlayer.abfrage(self)

#if __name__ == "__main__":
#    main()
