"""
Date: 21/10/2021
Author: Matteo Nunziante

Description: Tip Tap Toe game
"""

import numpy as np
from enum import Enum
SIZE = 3  # toDo: add this as a parameter in the game -> from the Menu object the user can change it (in the GUI)


class CellState(Enum):
    """
    State of the node cell
    O_Value -> O
    X_Value -> X
    """
    O_Value = 0,
    X_Value = 1


class GameState(Enum):
    """
    State of the game
    WIN -> if the algorithm won
    LOOSE -> if the algorithm lose
    NOBODY -> if the game ended but nobody won
    UNDEFINED -> if the game is still open
    """
    WIN = 0,
    LOOSE = 1,
    NOBODY = 2,
    UNDEFINED = 3


class Node:
    def __init__(self , data , h , predecessor = None):
        """
        Initialize the node parameter
        :param data: is the value of the configuration
        :param h: is the h value of that configuration
        :param predecessor: is the predecessor of the current node
        """
        self.size = SIZE
        # Create the empty configuration -> all cells are initialized to None
        # self.node = np.empty((self.size , self.size) , dtype = State)
        self.data = data
        # Initialize the predecessor and the successor
        self.predecessor = predecessor
        self.successor = None
        # Initialize the h value of the node
        self.h = h

    def generateTree(self):
        """
        Recursive function that generate a tree starting from self.data value as root
        :return: the root of the tree
        """
        # toDo: maybe this method will go in GameHandler


class GameHandler:
    def __init__(self):
        """
        Initialize something
        """
        self.size = SIZE
        # Initialize the root ot the tree -> the empty node
        self.node = Node(np.empty((self.size , self.size) , dtype = CellState) , 0)
        # Save the active player
        self.active = False  # True if it's the turn of the algorithm, False otherwise
        # Save the symbol of the algorithm: O or X
        self.symbol = CellState.X_Value

    def generateTree(self , node):
        """
        Method used to generate the whole tree starting from the configuration sent as parameter
        :param node: is the configuration to expand until the final configuration
        """

    def h(self , node):
        """
        Function that given a node calculate the h function
        :param node: is the node of which calculate the h function
        :return: the value of h
        """

    def isFinalConfiguration(self , node):
        """
        Method that said if a configuration is final
        :param node: the node to analyse
        :return: a pair of:
                    -> True if it is final, False otherwise
                    -> a GameState element according to the situation
        """

    def isWon(self , node , elementToCheck):
        """
        Method used to verify is someone won
        :param node: is the node to analyse
        :param elementToCheck: check if there is a tris of elementToCheck (CellState = O_Value pr X_Value)
        :return: True if it won, False otherwise
        """

    def process(self):
        """
        Method that handles the game interaction
        """
        # Random choose of the first player -> 1: X , 2: O

        # Start the loop

        # Generate the whole tree

        # Analyse it and chose the best action to do (In case of first player just say to put in the middle)

        # Do the action

        # Update the GUI

        # Wait for the move of the enemy

        # Repeat until isFinalConfiguration = False


if __name__ == '__main__':
    gameHandler = GameHandler()
    gameHandler.process()


