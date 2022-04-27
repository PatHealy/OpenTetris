# Open Tetris
Code to run a Tetris game on various displays.

## Controls
- WASD to move (w to snap)
- R to rotate
- x to close the game
- In the multiplayer mode, Arrows to move, RControl to rotate

## Play a Single Player Game
To run with a pygame GUI, run app.py with one parameter "play":
```bash
python app.py play [cell-size]
```
This requires you have pygame installed. For any of these commands you can include an additional int parameter "cell-size", which is the width of each Tetris tile in pixels. The default value is 50.

## Run Multiplayer Game 
```bash
python app.py multiplayer [cell-size]
```
This requires you have pygame installed.

# AI Stuff

## Train Single Player Agent
```bash
python app.py trainP1 [cell-size]
```
This agent is trained using a genetic algorithm using the parameters defined in /core/utilities.py

## Test Single Player Agent
```bash
python app.py testP1 [cell-size]
```
![A gif demonstrating the single player agent in action](/single_player/demonstration.gif)

## Play multiplayer against the single player agent
```bash
python app.py vsAI [cell-size]
```

## Train the multiplayer agent
```bash
python app.py train2P [cell-size]
```
This agent is trained using a genetic algorithm using the parameters defined in /core/utilities.py, playing against the single player agent.

## Test the multiplayer agent
```bash
python app.py test2P [cell-size]
```
Tests the multiplayer-trained agent against the single player agent.

![A gif demonstrating the multiplayer agent in action. Multiplayer on the left, single-player on the right.](/multiplayer/demonstration.gif)


## Play multiplayer against the multiplayer agent
```bash
python app.py vsMPAI [cell-size]
```

# Alternative Displays

## Run in Terminal
To run in terminal, run app.py with parameter "terminal":
```bash
python app.py terminal
```
This requires the package sty. Given how it uses colored text, I can only confirm it to run on Linux terminals 
(tested on Ubuntu terminal for Windows).

## LED Panel

An LED panel display driver is currently in development.

