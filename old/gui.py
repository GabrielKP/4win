
import tkinter as tk

class GUI:
    ''' comment '''

    def __init__(self, game, width=800, height=800):
        ''' Init of GUI '''

        self.game = game
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width = width, height = 1000, background="blue")
        self.canvas.pack()

        self.circlesize = int(min(width, height) / game._ncols)

        offset = self.circlesize * 0.1
        # Create Matrix of  circles
        self.circleMatrix = [[self.canvas.create_oval(offset + col * self.circlesize, offset + row*self.circlesize, col * self.circlesize + int(self.circlesize * 0.9), row * self.circlesize + int(self.circlesize * 0.9), fill="white") for col in range(game._ncols)] for row in range(game._nrows)]

        self.canvas.update()


    def update(self, position, player):
        ''' Inserts a stone into the given position for the player '''
        row, col = position
        # guiRow and gameRows are exactly the opposite -> swap
        guiRow = self.game._nrows - 1 - row
        self.canvas.itemconfig( self.circleMatrix[guiRow][col], fill="red" if player == 1 else "yellow" )
        self.canvas.update()


    def _initInteractive(self):
        ''' Sets up variables for GUI '''
        # Bind Mouse and Keyboard
        self.canvas.bind("<Button-1>", self._mousePress)
        self.canvas.config(cursor="crosshair")
        self.root.bind("<Key>", self._keyPress)
        # Flag to know when we are waiting
        self.waitInput = False


    def _keyPress(self, event):
        ''' Handles Key Press '''
        if self.waitInput:
            # Try to convert, if not put a char in variable to get into error handling in InteractivePlayer
            try:
                self.inputCol = int(event.char)
            except Exception:
                self.inputCol = event.char
            # Unmark Flag
            self.waitInput = False


    def _mousePress(self, event):
        ''' Returns X position of Mouse when Button pressed '''
        if self.waitInput:
            # Compute Column from mouseclick
            self.inputCol = int( event.x / self.circlesize)
            # Unmark Flag
            self.waitInput = False


    def _getInput(self):
        ''' Blocks until User clicks onto a field '''
        self.waitInput = True
        while self.waitInput:
            self.canvas.update()
        return self.inputCol


    def _displayMessage(self, message):
        ''' Displays message prominently on screen '''
        x = self.canvas.winfo_width() // 2
        y = self.canvas.winfo_height() - (self.canvas.winfo_height() // 10 )
        font = ('Arial',24,'bold')
        self.canvas.create_text(x, y, text=message, fill="black", font=font)

