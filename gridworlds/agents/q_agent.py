import random
from gridworlds.gridworld import Environment, Actions


class QAgent():
    def __init__(self, environment: Environment, epsilon=0.05, alpha=0.1, gamma=1):
        self.environment = environment
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

        self.q_table = {}
        for row in range(environment.ENV_DIMENSION):
            for col in range(environment.ENV_DIMENSION):
                self.q_table[(row, col)] = {Actions.UP: 0, Actions.DOWN: 0, Actions.LEFT: 0, Actions.RIGHT: 0}

    def next_action(self, valid_actions):
        # Explore
        if random.random() < self.epsilon:
            action = valid_actions[random.randint(0, len(valid_actions) - 1)]

        # Exploit
        else:
            q_state = self.q_table[self.environment._agent_coordinates]
            max_q = max(v for k, v in q_state.items() if k in valid_actions)
            action = random.choice([k for k, v in q_state.items() if v == max_q and k in valid_actions])

        return action

    def learn(self, old_state, reward, new_state, action):
        """Updates the Q-value table using Q-learning"""
        new_q = self.q_table[new_state]
        max_new_q = max(new_q.values())
        current_q = self.q_table[old_state][action]

        updated_q = (1 - self.alpha) * current_q + self.alpha * (
            reward + self.gamma * max_new_q
        )
        self.q_table[old_state][action] = updated_q
