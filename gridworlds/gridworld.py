import enum
from abc import ABC, abstractmethod


class Actions(enum.IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    STAY = 4


class Environment(ABC):
    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def action_space(self):
        pass

    @abstractmethod
    def print_environment(self):
        pass
