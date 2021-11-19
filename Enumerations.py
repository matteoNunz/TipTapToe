"""
Date: 18/11/2021
Author: Matteo Nunziante

Description: Enums for Tip Tap Toe game
"""

from enum import IntEnum


class CellState(IntEnum):
    """
    State of the node cell
    O_Value -> O
    X_Value -> X
    empty_Value -> empty cell
    """
    O_Value = -1,
    X_Value = 1,
    empty_Value = 0


class GameState(IntEnum):
    """
    State of the game
    WIN -> if the algorithm won
    LOOSE -> if the algorithm lose
    DRAW -> if the game ended but nobody won
    UNDEFINED -> if the game is still open
    """
    WIN = 0,
    LOOSE = 1,
    DRAW = 2,
    UNDEFINED = 3