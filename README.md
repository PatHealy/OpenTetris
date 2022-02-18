# Open Tetris
Code to run a Tetris game on various displays.


Currently, one display method is supported but 2 others are in development.

## Run in Terminal
To run in terminal, simply run app.py, which will call runners.terminal.terminal_runner.py:
```bash
python app.py
```

This requires the package sty. Given how it uses colored text, I can only confirm it to run on Linux terminals 
(tested on Ubuntu terminal for Windows).

## Run in a PyGame GUI
To run the GUI, run app.py with a parameter "GUI" like this:
```bash
python app.py GUI
```

## Run on an LED board

This isn't finished yet!


