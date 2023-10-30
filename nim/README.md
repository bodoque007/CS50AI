# Nim AI
This is the fourth proyect of the course. It's an AI that teaches itself to play [Nim](https://en.wikipedia.org/wiki/Nim) through reinforcement learning using a [Q-learning algorithm.](https://en.wikipedia.org/wiki/Q-learning)
In the game Nim, we begin with some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from any one non-empty pile. Whoever removes the last object loses.

## Usage
Run the following on a terminal inside the project's folder:
`python3 play.py {number of training matches to play against itself} "{initial piles as Python's list representation}"`
## Example usage
`python3 play.py 42 "[1,5,7,9]"                                                                                                                                                                                                                                                                                                                                      