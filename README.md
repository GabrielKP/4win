# 4wins

This is a Python version of the old classic 4wins!
Goal is to have a competition who builds the best 4wins player!

## Startup
You will need python3. Clone this repository and you are ready to go! The Game startup can be changed in [4win.py](4win.py)

## Structure
Built modular:

    .
    ├── 4win.py                  # This is the Basegame, all commits regarding it go directly to master
    ├── StandardPlayer.py        # The Standard Player Implementation, commits -> master
    ├── InteractivePlayer.py     # An interactive Player, if you want to play yourself!
    ├── ExamplePlayer.py         # An example Player to copy and then, commits -> master
    ├── [otherplayers].py      # Specific other players, commits -> own branch
    └── README.md

## Player

### Player Conditions
(numbers still can change)
- The Player cannot take more then 60 seconds on initialization
- The Player cannot take more then 10 seconds in each turn
- The Player shall not return a wrong column to place the stone in (e.g. a full column)
- The Player does not touch any variables of the Game directly! (use getter functions)
- The Player is not built by using existing frameworks (e.g. TensorFlow)
- The Player idea is built by your own logic and not using code from the internet

### What does the player need to have?
- The Player needs to have following variables: playerName
- The Player needs to have following functions: nextTurn
- Look at the ExamplePlayer for further information