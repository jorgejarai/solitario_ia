import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import numpy as np
import legal_moves

# entrada: 4965
# salida: 885


# Define the neural network architecture
class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(
            input_size, 6000
        )  # 6000 = numero de neuronas de la siguiente capa
        self.fc2 = nn.Linear(6000, output_size)
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.loss = nn.MSELoss()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.to(self.device)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Define the agent


class DQNAgent:
    def __init__(self, input_size, output_size, learning_rate=0.001):
        self.input_size = input_size
        self.output_size = output_size
        self.epsilon = 1.00  # Exploration rate
        self.epsilon_decay = 0.999  # Decay rate for exploration
        self.epsilon_min = 0.01  # minimiun exploration rate
        self.gamma = 0.99  # weights of future rewards
        self.model = DQN(input_size, output_size)
        
        
        # memory but i dont know if it works
        self.mem_size = 100000
        self.state_memory = np.zeros((self.mem_size, *input_size), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_size), dtype=np.float32)

        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool_)
        
    def choose_action(self, state):
        #si un numero random es mayor que epsilon tomamos la mejor opcion posible 
        if np.random.random() > self.epsilon:

        else:
            return random.randint(0, len())


