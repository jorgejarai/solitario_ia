#!/usr/bin/env python3

"""
DQN for Unity ML-Agents Environments using PyTorch
Includes examples of the following DQN training algorithms:
  -> Vanilla DNQ, 
  -> Double-DQN (DDQN)

The example uses a modified version of the Unity ML-Agents Banana Collection Example Environment.
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
import json
import sys
import torch
import time
import random
import numpy as np
from collections import deque
from dqn_agent import Agent
from legal_moves import LegalMoveChecker
from solitaire_board import SolitaireBoard

"""
###################################
STEP 1: Set the Training Parameters
======
        num_episodes (int): maximum number of training episodes
        epsilon (float): starting value of epsilon, for epsilon-greedy action selection
        epsilon_min (float): minimum value of epsilon
        epsilon_decay (float): multiplicative factor (per episode) for decreasing epsilon
        scores (float): list to record the scores obtained from each episode
        scores_average_window (int): the window size employed for calculating the average score (e.g. 100)
        solved_score (float): the average score required for the environment to be considered solved
        (here we set the solved_score a little higher than 13 [i.e., 14] to ensure robust learning).
    """
num_episodes = 2000
epsilon = 1.0
epsilon_min = 0.05
epsilon_decay = 0.99
scores = []
scores_average_window = 100
solved_score = 100000


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
# action_size = brain.vector_action_space_size
action_size = 856

# Set the size of state observations or state size
# state_size = brain.vector_observation_space_size
state_size = 4080


"""
###################################
STEP 5: Create a DQN Agent from the Agent Class in dqn_agent.py
A DQN agent initialized with the following state, action and DQN hyperparameters.
    DQN Agent Parameters
    ======
    state_size (int): dimension of each state (required)
    action_size (int): dimension of each action (required)
    dqn_type (string): can be either 'DQN' for vanillia dqn learning (default) or 'DDQN' for double-DQN.
    replay_memory size (int): size of the replay memory buffer (default = 1e5)
    batch_size (int): size of the memory batch used for model updates (default = 64)
    gamma (float): parameter for setting the discounted value of future rewards (default = 0.99)
    learning_rate (float): specifies the rate of model learning (default = 5e-4)
    seed (int): random seed for initializing training point (default = 0)

The DQN agent specifies a local and target neural network for training.
The network is defined in model.py. The input is a real (float) value vector of observations.
(NOTE: not appropriate for pixel data). It is a dense, fully connected neural network,
with 2 x 128 node hidden layers. The network can be modified by changing model.py.

Here we initialize an agent using the Unity environments state and action size determined above 
and the default DQN hyperparameter settings.
"""
seed = random.randint(1, 2**31 - 1)
agent = Agent(state_size=state_size, action_size=action_size, dqn_type="DQN", seed=seed)

# Save seed for reproducibility
timestr = time.strftime("%Y%m%d-%H%M%S")
seed_file = open(f"seed-{timestr}.txt", "w")
seed_file.write(str(seed))
seed_file.close()


"""
###################################
STEP 6: Run the DQN Training Sequence
The DQN RL Training Process involves the agent learning from repeated episodes of behaviour 
to map states to actions the maximize rewards received via environmental interaction.
The artificial neural network is expected to converge on or approximate the optimal function 
that maps states to actions. 

The agent training process involves the following:
(1) Reset the environment at the beginning of each episode.
(2) Obtain (observe) current state, s, of the environment at time t
(3) Use an epsilon-greedy policy to perform an action, a(t), in the environment 
    given s(t), where the greedy action policy is specified by the neural network.
(4) Observe the result of the action in terms of the reward received and 
	the state of the environment at time t+1 (i.e., s(t+1))
(5) Calculate the error between the actual and expected Q value for s(t),a(t),r(t) and s(t+1)
	to update the neural network weights.
(6) Update episode score (total reward received) and set s(t) -> s(t+1).
(7) If episode is done, break and repeat from (1), otherwise repeat from (3).

Below we also exit the training process early if the environment is solved. 
That is, if the average score for the previous 100 episodes is greater than solved_score.
"""

won_games = 0
boards = []

if len(sys.argv) > 1:
    json_files = sys.argv[1:]
    boards = []

    for json_file in json_files:
        with open(json_file, "r") as f:
            board_json = f.read()
            board_json = json.loads(board_json)

        boards.append(SolitaireBoard.generate_from_json(board_json))

    num_episodes = len(boards)

try:
    # create log file
    timestr = time.strftime("%Y%m%d-%H%M%S")
    log_file = open(f"score-{timestr}.csv", "w")

    # loop from num_episodes
    for i_episode in range(1, num_episodes + 1):
        # reset the unity environment at the beginning of each episode
        # env_info = env.reset(train_mode=True)[brain_name]
        env = (
            boards[i_episode - 1]
            if len(sys.argv) > 1
            else SolitaireBoard.generate_random()
        )
        legal_checker = LegalMoveChecker(env)

        # get initial state of the unity environment
        # state = env_info.vector_observations[0]
        state = env.encode_board()

        # set the initial episode score to zero.
        score = 0

        # Run the episode training loop;
        # At each loop step take an epsilon-greedy action as a function of the current state observations
        # Based on the resultant environmental state (next_state) and reward received update the Agent network
        # If environment episode is done, exit loop...
        # Otherwise repeat until done == true
        i = 0
        while True:
            # Clear screen (ANSI escape code)
            print("\033[2J\033[H", end="")
            print((i, score, legal_checker.get_legal_moves()))
            env.print_game()

            # determine epsilon-greedy action from current state
            try:
                action = agent.act(state, epsilon, legal_checker)
            except ValueError:
                print("Unwinnable game")
                break

            # if i % 200 == 0:
            #     env.print_game()
            #     print(legal_checker.decode_move(action))

            # send the action to the environment and receive resultant environment information
            # env_info = env.step(action)
            reward = env.play_move_reward(legal_checker.decode_move(action))

            next_state = env.encode_board()  # get the next state
            # reward = env_info.rewards[0]  # get the reward
            done = env.check_if_won()  # see if episode has finished

            # Send (S, A, R, S') info to the DQN agent for a neural network update
            agent.step(state, action, reward, next_state, done)

            # set new state to current state for determining next action
            state = next_state

            # Update episode score
            score += reward

            if done:
                won_games += 1
                print("Won game")
                env.print_game()
                break

            # If unity indicates that episode is done,
            # then exit episode loop, to begin new episode
            if i > 500:
                break

            i += 1

        # Add episode score to Scores and...
        # Calculate mean score over last 100 episodes
        # Mean score is calculated over current episodes until i_episode > 100
        scores.append(score)
        average_score = np.mean(
            scores[i_episode - min(i_episode, scores_average_window) : i_episode + 1]
        )

        # Decrease epsilon for epsilon-greedy policy by decay rate
        # Use max method to make sure epsilon doesn't decrease below epsilon_min
        epsilon = max(epsilon_min, epsilon_decay * epsilon)

        # (Over-) Print current average score
        print(
            "{},{:.2f},{:.2f}".format(i_episode, average_score, won_games / i_episode)
        )

        # Write to log file
        log_file.write(
            "{},{:.2f},{:.2f}\n".format(i_episode, average_score, won_games / i_episode)
        )

        # Flush log file
        log_file.flush()

        # Check to see if the task is solved (i.e,. avearge_score > solved_score).
        # If yes, save the network weights and scores and end training.
        if won_games / i_episode > 0.75:
            print(
                "\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}".format(
                    i_episode, average_score
                )
            )

            # Save trained neural network weights
            timestr = time.strftime("%Y%m%d-%H%M%S")
            nn_filename = "dqnAgent_Trained_Model_" + timestr + ".pth"
            torch.save(agent.network.state_dict(), nn_filename)

            # Save the recorded Scores data
            scores_filename = "dqnAgent_scores_" + timestr + ".csv"
            np.savetxt(scores_filename, scores, delimiter=",")
            break
except KeyboardInterrupt:
    print("\nEnvironment solved")

    # Save trained neural network weights
    timestr = time.strftime("%Y%m%d-%H%M%S")
    nn_filename = "dqnAgent_Trained_Model_" + timestr + ".pth"
    torch.save(agent.network.state_dict(), nn_filename)

    # Save the recorded Scores data
    scores_filename = "dqnAgent_scores_" + timestr + ".csv"
    np.savetxt(scores_filename, scores, delimiter=",")

"""
###################################
STEP 7: Everything is Finished -> Close the Environment.
"""
# env.close()

# END :) #############
