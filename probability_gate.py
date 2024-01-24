import random

from gridworld import Actions


class ProbabilityGate:
    def __init__(self, probability):
        self._probability = probability

    def __call__(self, x):
        if random.random() < self._probability:
            return Actions.UP
        else:
            return Actions.DOWN

    @property
    def probability(self):
        return self._probability
