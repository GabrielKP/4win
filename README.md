# 4wins

This is a Python version of the old classic connect 4!
Goal is to have a competition who builds the best 4wins player!

## Startup
You will need python3. Clone this repository and you are ready to go! The Game startup can be changed in [main.py](main.py)

To start a game, in the `main()` function of `main`:
0. Initialize player objects if needed
1. Create a 4wins object: `fw = FourWins( player1NextMove, player2NextMove, verbosity )
    - player1NextMove/player2NextMove are the functions of the respective player
    - verbosity toggles the console output of the main game (not the players), 0 no output, 1 output
2. Call `fw.start()`, it will return the winners id ( player1 has 0, player2 has 1 )

## Structure
    .
    ├── main.py                 # class included connect 4 game
    ├── player.py               # all player functions and classes
    ├── gui.py                  # file with some code for gui, not functional yet
    ├── old                     # folder including old (slower) connect 4 implementation
    └── README.md

## Game
The game is based on John Tromps implementation of connect 4: https://tromp.github.io/c4/c4.html

There also is a detailed explanation how it works: https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md

## Player

### Player Conditions
(numbers still can change)
- The Player cannot take more then 60 seconds on initialization
- The Player cannot take more then 10 seconds in each turn
- The Player shall not return a wrong column to place the stone in (e.g. a full column)

### What does the player need to have?
For the connect 4 game to work your player(class) needs to implement a nextMove function which takes `boards`, `height`, `moves` and `turns` as argument and returns a valid column as int:
- `boards` is a list of two int, representing a bitmap for each player.
    - `boards[0]` for player 0 and `boards[1]` for player 1.
- `height` is a list, including an int for each column, which next bit in `boards` is free.
- `moves` is the a list of all moves since the beginning
- `turns` is the amount of turns

You can find a detailed explanation [here](https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md)
