class searchPlayer:
    """
    Gabriels implementation
    """

    def init( self ):
        self.HEIGHT = 6
        self.H1 = self.HEIGHT + 1
        self.WIDTH = 7
        self.SIZE = self.HEIGHT * self.WIDTH

    def isLegal( self, height, column ):
        """
        column needs to be int: 0 < column < WIDTH
        """
        return height[column] < ( column + 1 ) * self.H1 - 1