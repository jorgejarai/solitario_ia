#!/usr/bin/env python3

"""
Test DQN Model for Unity ML-Agents Environments using PyTorch

This example tests a trained DQN NN model on a modified version of the Unity ML-Agents Banana Collection Example Environment.
The environment includes a single agent, who can turn left or right and move forward or backward.
The agent's task is to collect yellow bananas (reward of +1) that are scattered around an square
game area, while avoiding purple bananas (reward of -1). For the version of Bananas employed here,
the environment is considered solved when the average score over the last 100 episodes > 13. 

Example Developed By:
Michael Richardson, 2018
Project for Udacity Danaodgree in Deep Reinforcement Learning (DRL)
Code Expanded and Adapted from Code provided by Udacity DRL Team, 2018.
"""

"""
This file has been modified from the original version made by Michael Richardson,
originally licensed under the GPLv3 license.

solitario_ia
Copyright (C) 2023 Aníbal Ibaceta, Sebastián Hevia & Jorge Jara

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

###################################
# Import Required Packages
import torch
import time
import random
import numpy as np
from dqn_agent import Agent
from legal_moves import LegalMoveChecker
from solitaire_board import SolitaireBoard
import sys

"""
###################################
STEP 1: Set the Test Parameters
======
        num_episodes (int): number of test episodes
"""
num_episodes = 1


"""
###################################
STEP 2: Start the Unity Environment
# Use the corresponding call depending on your operating system 
"""
# env = UnityEnvironment(file_name="Banana.app")
# - **Mac**: "Banana.app"
# - **Windows** (x86): "Banana_Windows_x86/Banana.exe"
# - **Windows** (x86_64): "Banana_Windows_x86_64/Banana.exe"
# - **Linux** (x86): "Banana_Linux/Banana.x86"
# - **Linux** (x86_64): "Banana_Linux/Banana.x86_64"
# - **Linux** (x86, headless): "Banana_Linux_NoVis/Banana.x86"
# - **Linux** (x86_64, headless): "Banana_Linux_NoVis/Banana.x86_64"

"""
#######################################
STEP 3: Get The Unity Environment Brian
Unity ML-Agent applications or Environments contain "BRAINS" which are responsible for deciding 
the actions an agent or set of agents should take given a current set of environment (state) 
observations. The Banana environment has a single Brian, thus, we just need to access the first brain 
available (i.e., the default brain). We then set the default brain as the brain that will be controlled.
"""
# Get the default brain
# brain_name = env.brain_names[0]

# Assign the default brain as the brain to be controlled
# brain = env.brains[brain_name]


"""
#############################################
STEP 4: Determine the size of the Action and State Spaces
# 
# The simulation contains a single agent that navigates a large environment.  
# At each time step, it can perform four possible actions:
# - `0` - walk forward 
# - `1` - walk backward
# - `2` - turn left
# - `3` - turn right
# 
# The state space has `37` dimensions and contains the agent's velocity, 
# along with ray-based perception of objects around agent's forward direction.  
# A reward of `+1` is provided for collecting a yellow banana, and a reward of 
# `-1` is provided for collecting a purple banana. 
"""

# Set the number of actions or action size
action_size = 856

# Set the size of state observations or state size
state_size = 4080


"""
###################################
STEP 5: Initialize a DQN Agent from the Agent Class in dqn_agent.py
A DQN agent initialized with the following state, action and DQN hyperparameters.
    DQN Agent Parameters
    ======
    state_size (int): dimension of each state (required)
    action_size (int): dimension of each action (required)

The DQN agent specifies a local and target neural network for training.
The network is defined in model.py. The input is a real (float) value vector of observations.
(NOTE: not appropriate for pixel data). It is a dense, fully connected neural network,
with 2 x 128 node hidden layers. The network can be modified by changing model.py.

Here we initialize an agent using the Unity environments state and action size determined above 
We also load the model parameters from training
"""

if len(sys.argv) != 3:
    print("Usage: ./test.py <agent_path> <seed>")
    exit(1)

weights_path = sys.argv[1]
seed = random.randint(1, 2**31 - 1)

# Initialize Agent
agent = Agent(state_size=state_size, action_size=action_size, seed=seed)


# Load trained model weights
agent.network.load_state_dict(torch.load(weights_path))

"""
###################################
STEP 6: Play Banana for specified number of Episodes
"""
i = 0
# loop from num_episodes
for i_episode in range(1, num_episodes + 1):
    # reset the unity environment at the beginning of each episode
    # set train mode to false
    env = SolitaireBoard.generate_random()
    legal_checker = LegalMoveChecker(env)

    # get initial state of the unity environment
    state = env.encode_board()

    # set the initial episode score to zero.
    score = 0

    # Run the episode loop;
    # At each loop step take an action as a function of the current state observations
    # If environment episode is done, exit loop...
    # Otherwise repeat until done == true
    while True:
        env.print_game()
        print("Score: ", score)

        # determine epsilon-greedy action from current sate
        try:
            action = agent.act(state, 0)
        except ValueError:
            print("Unwinnable game")
            break

        print("Action: ", legal_checker.decode_move(action))

        # send the action to the environment and receive resultant environment information
        # env_info = env.step(action)[brain_name]

        reward = env.play_move_reward(legal_checker.decode_move(action))

        print("Reward: ", reward)

        # wait for key press
        input("Press Enter to continue...")

        next_state = np.hstack(
            (env.encode_board(), legal_checker.encode_legal_moves())
        )  # get the next state
        # reward = env_info.rewards[0]  # get the reward
        done = env.check_if_won()  # see if episode has finished

        # set new state to current state for determining next action
        state = next_state

        # Update episode score
        score += reward

        # If unity indicates that episode is done,
        # then exit episode loop, to begin new episode
        if done or i > 1000:
            break

        i += 1

    # (Over-) Print current average score
    print("\rEpisode {}\tAverage Score: {:.2f}".format(i_episode, score), end="")


"""
###################################
STEP 7: Everything is Finished -> Close the Environment.
"""
# env.close()

# END :) #############
