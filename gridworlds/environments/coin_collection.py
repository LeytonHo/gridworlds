import random
import itertools
from gridworlds.gridworld import Environment


ENV_DIMENSION = 5
MAX_INT = 100000
example_environment = [
    [3, None, None, '#', 1],
    [None, '#', None, '#', None],
    [None, None, 'A', None, None],
    [None, '#', None, None, 1],
    [1, '#', 2, None, None]
]


class CoinCollectionEnvironment(Environment):
    def __init__(self, max_walls=5, min_timesteps=5, max_timesteps=10):
        self.max_walls = max_walls
        self.min_timesteps = min_timesteps
        self.max_timesteps = max_timesteps
        self.environment, self.agent_coordinates, self.episode_timesteps = self.generate_environment()

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
        environment = [[None] * ENV_DIMENSION for _ in range(ENV_DIMENSION)]
        wall_count = 0
        agent_assigned = False
        agent_coordinates = MAX_INT, MAX_INT

        coordinate_pairs = list(itertools.product(range(ENV_DIMENSION), range(ENV_DIMENSION)))

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
            if wall_count < self.max_walls and abs(row - agent_coordinates[0]) + abs(col - agent_coordinates[1]) != 1:
                if random.random() < 0.2:
                    environment[row][col] = '#'
                    wall_count += 1
                    continue

            # Place coins randomly
            if random.random() < 0.2:
                environment[row][col] = random.randint(1, 8)

        episode_timesteps = random.randint(self.min_timesteps, self.max_timesteps)
        return environment, agent_coordinates, episode_timesteps

    def setup(self):
        pass

    def reset(self):
        self.environment, self.agent_coordinates, self.episode_timesteps = self.generate_environment()

    def step(self, action):
        pass

    def action_space(self):
        pass

    def print_environment(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.environment]))
