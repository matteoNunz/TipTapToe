"""
Date: 18/11/2021
Author: Matteo Nunziante

Description: Player for Tip Tap Toe game
"""
import pickle

import numpy as np


class Player:
    def chooseAction(self , positions):
        pass

    def addState(self , state):
        pass

    def feedReward(self , reward):
        pass

    def reset(self):
        pass


class ArtificialPlayer(Player):

    def __init__(self , name , symbol , exp_rate = 0.4):
        self.name = name
        self.symbol = symbol
        self.states = []  # To save all positions taken
        self.states_value = {}  # State -> value
        # Epsilon-greedy method to balance between exploration and exploitation
        self.exp_rate = exp_rate  # 30% of the time random actions
        self.lr = 0.5
        self.gamma = 0.9

    def getHash(self , board , board_rows = 3 , board_cols = 3):
        boardHash = str(board.reshape(board_rows * board_cols))
        return boardHash

    def chooseAction(self , positions , board):
        if np.random.uniform(0 , 1) <= self.exp_rate:
            # Take a random action
            if (1 , 1) in positions:
                action = (1 , 1)
                return action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            if (1 , 1) in positions:
                action = (1 , 1)
                return action
            valueMax = -999
            action = None
            for p in positions:
                # Make a copy of the board
                next_board = board.copy()
                # Add the symbol in a possible position
                next_board[p] = self.symbol
                # Take the next board hash
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None \
                    else self.states_value.get(next_boardHash)
                print("Value: " , value)
                if value >= valueMax:
                    valueMax = value
                    action = p
        print("{} takes action {}".format(self.name , action))
        return action

    def addState(self , state):
        self.states.append(state)

    def feedReward(self , reward):
        # Back propagation of the reward
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            self.states_value[state] = (1 - self.lr) * self.states_value[state] \
                                       + self.lr * (reward + self.gamma * self.states_value[state])
            #  reward = self.states_value[state]

    def reset(self):
        self.states = []

    def savePolicy(self):
        print("Saving configuration...")
        file = open('Files/policy_' + str(self.name) , 'wb')
        pickle.dump(self.states_value , file)
        file.close()
        print("Configuration saved!")

    def loadPolicy(self , f):
        print("Loading policy...")
        file = open(f , 'rb')
        self.states_value = pickle.load(file)
        file.close()
        print("Policy loaded")


class HumanPlayer(Player):
    def __init__(self , name , symbol):
        self.name = name
        self.symbol = symbol

    def chooseAction(self , positions):
        while True:
            try:
                row = int(input("Input your action row: "))
                col = int(input("Input your action col: "))
                if type(row) != int or type(col) != int:
                    raise Exception()
            except Exception:
                continue

            action = (row , col)
            if action in positions:
                return action

    def reset(self):
        self.name = None
        self.symbol = None