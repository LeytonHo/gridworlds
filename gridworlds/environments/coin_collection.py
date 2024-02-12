import random
import itertools
import copy
from gridworlds.gridworld import Environment, Actions


MAX_INT = 100000
example_environment = [
    [3, None, None, '#', 1],
    [None, '#', None, '#', None],
    [None, None, 'A', None, None],
    [None, '#', None, None, 1],
    [1, '#', 2, None, None]
]


class CoinCollectionEnvironment(Environment):
    def __init__(self, max_walls=5, min_timesteps=6, max_timesteps=12, coin_min=1, coin_max=8):
        self._max_walls = max_walls
        self._min_timesteps = min_timesteps
        self._max_timesteps = max_timesteps
        self._coin_min = coin_min
        self._coin_max = coin_max
        self.ENV_DIMENSION = 5
        self.game_over = False

        self._episode_reward = 0

        self._environment, self._agent_coordinates, self._episode_timesteps = self.generate_environment()

        # Save the original configuration since we will mutate the above variables
        self._base_environment = copy.deepcopy(self._environment)
        self._base_agent_coordinates = copy.deepcopy(self._agent_coordinates)
        self._base_episode_timesteps = copy.deepcopy(self._episode_timesteps)

    def generate_environment(self):
        '''
        Stochastically generates a Gridworld environment containing the agent, coins, and walls.

        Invariants:
            - There are no surrounding walls around the agent
            - There are a maximum number of walls in the environment
            - The episode lasts between min_timesteps and max_timesteps

        Returns:
            - A Gridworld environment
            - The starting position of the agent
            - The number of timesteps before the episode terminates
        '''
        environment = [[None] * self.ENV_DIMENSION for _ in range(self.ENV_DIMENSION)]
        wall_count = 0
        agent_assigned = False
        agent_coordinates = MAX_INT, MAX_INT

        coordinate_pairs = list(itertools.product(range(self.ENV_DIMENSION), range(self.ENV_DIMENSION)))

        # We want to process each square in the Gridworld sequentially, but without bias
        # This avoid issues like frequently placing the agent in the top left corner, for example
        random.shuffle(coordinate_pairs)

        for row, col in coordinate_pairs:
            # Place the agent randomly
            if not agent_assigned:
                environment[row][col] = 'A'
                agent_assigned = True
                agent_coordinates = (row, col)
                continue

            # Place walls randomly, ensuring that there are no surrounding walls around the agent
            if wall_count < self._max_walls and abs(row - agent_coordinates[0]) + abs(col - agent_coordinates[1]) != 1:
                if random.random() < 0.2:
                    environment[row][col] = '#'
                    wall_count += 1
                    continue

            # Place coins randomly
            if random.random() < 0.2:
                environment[row][col] = random.randint(self._coin_min, self._coin_max)

        episode_timesteps = random.randint(self._min_timesteps, self._max_timesteps)
        return environment, agent_coordinates, episode_timesteps

    def setup(self):
        '''
        Generates a new environment configuration.
        '''
        self._environment, self._agent_coordinates, self._episode_timesteps = self.generate_environment()

    def reset(self):
        '''
        Resets the environment to its original configuration.
        '''
        self._environment = copy.deepcopy(self._base_environment)
        self._agent_coordinates = copy.deepcopy(self._base_agent_coordinates)
        self._episode_timesteps = copy.deepcopy(self._base_episode_timesteps)
        self._episode_reward = 0
        self.game_over = False

    def move(self, delta_x, delta_y):
        current_row, current_col = self._agent_coordinates
        new_row, new_col = current_row + delta_x, current_col + delta_y
        move_reward = 0

        if self._environment[new_row][new_col] is not None:
            self._episode_reward += self._environment[new_row][new_col]
            move_reward = self._environment[new_row][new_col]

            # Reward collected, remove the coin
            self._environment[new_row][new_col] = 'A'

        self._agent_coordinates = new_row, new_col
        self._environment[current_row][current_col] = None
        return move_reward

    def step(self, action):
        valid_actions = self.action_space()
        assert action in valid_actions, "Invalid action - action must be one of {}".format(valid_actions)

        if action == Actions.UP:
            step_reward = self.move(-1, 0)
        elif action == Actions.DOWN:
            step_reward = self.move(1, 0)
        elif action == Actions.LEFT:
            step_reward = self.move(0, -1)
        elif action == Actions.RIGHT:
            step_reward = self.move(0, 1)

        self._episode_timesteps -= 1

        if self._episode_timesteps == 0:
            self.game_over = True
            return 0
        else:
            return step_reward

    def action_space(self):
        current_row, current_col = self._agent_coordinates
        valid_actions = []

        if current_row > 0 and self._environment[current_row - 1][current_col] != '#':
            valid_actions.append(Actions.UP)

        if current_row < self.ENV_DIMENSION - 1 and self._environment[current_row + 1][current_col] != '#':
            valid_actions.append(Actions.DOWN)

        if current_col > 0 and self._environment[current_row][current_col - 1] != '#':
            valid_actions.append(Actions.LEFT)

        if current_col < self.ENV_DIMENSION - 1 and self._environment[current_row][current_col + 1] != '#':
            valid_actions.append(Actions.RIGHT)

        return valid_actions

    def print_environment(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self._environment]))
