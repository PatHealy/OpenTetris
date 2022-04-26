# Open Tetris
Code to run a Tetris game on various displays.

## Controls
- WASD to move (w to snap)
- R to rotate
- x to close the game
- In the multiplayer mode, Arrows to move, RControl to rotate

## Run in a PyGame GUI
To run the GUI, run app.py with no parameters:
```bash
python app.py
```
This requires you have pygame installed.

## Run Multiplayer Game 
```bash
python app.py multiplayer
```
This requires you have pygame installed.

## Run in Terminal
To run in terminal, run app.py with parameter "terminal":
```bash
python app.py terminal
```
This requires the package sty. Given how it uses colored text, I can only confirm it to run on Linux terminals 
(tested on Ubuntu terminal for Windows).

# AI Stuff

## Train Single Player Agent
```bash
python app.py trainP1
```

## Test Single Player Agent
```bash
python app.py testP1
```

## Play multiplayer against the single player agent
```bash
python app.py vsAI
```

## Run on an LED board

This isn't finished yet!


