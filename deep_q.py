import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Define the deep Q-network
def build_dqn(input_shape, output_size):
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=input_shape))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(output_size, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=0.001))
    return model

# Define the agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995  # Decay rate for exploration
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.model = build_dqn(state_size, action_size)

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def replay(self, batch_size, states, targets):
        self.model.fit(states, targets, batch_size=batch_size, epochs=1, verbose=0)

# Initialize the Solitaire Klondike environment
solitaire = SolitaireBoard()

# Initialize the DQNAgent   
state_size = solitaire.get_state().shape
action_size = len(legal_checker.get_legal_moves())
agent = DQNAgent(state_size, action_size)

# Training loop
episodes = 1000
batch_size = 32
for episode in range(episodes):
    # Generate initial board configuration
    initial_board = solitaire.generate_random()

    # Initialize the board with the initial configuration
    solitaire.initialize_board(initial_board)

    state = solitaire.get_state()
    done = False
    while not done:
        action = agent.choose_action(state)
        legal_moves = legal_checker.get_legal_moves()
        next_state, reward, done = solitaire.take_action(legal_moves[action])
        target = reward
        if not done:
            target = reward + agent.model.predict(next_state)[0][np.argmax(agent.model.predict(next_state))]
        target_vec = agent.model.predict(state)
        target_vec[0][action] = target
        agent.replay(batch_size, state, target_vec)
        state = next_state
        agent.update_epsilon()

    # Print episode information
    print("Episode:", episode+1, "Score:", solitaire.get_score())

# Test the agent
test_episodes = 10
for episode in range(test_episodes):
    initial_board = solitaire.generate_random()
    solitaire.initialize_board(initial_board)
    state = solitaire.get_state()
    done = False
    while not done:
        action = agent.choose_action(state)
        legal_moves = legal_checker.get_legal_moves()
        next_state, reward, done = solitaire.take_action(legal_moves[action])
        state = next_state
        solitaire.render()  # Render the game state for visualization
