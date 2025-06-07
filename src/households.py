from __future__ import annotations

from agent import Agent, AgentBuilder
from environment import AgentManager
from network import SocialNetwork
from workers import Worker


class Household(Agent):  # TODO: implement
    _size: int
    _social_network: SocialNetwork
    _friends: list[int]

    _workers: list[Worker]
    _savings: float

    def __init__(
            self,
            manager: AgentManager,
            unique_id: int,
            size: int,
            workers: list[Worker],
            savings: float
    ):
        super().__init__(manager, unique_id, 'Household')

        self._size = size

        self._workers = workers
        self._savings = savings

    @property
    def friends(self):
        return self._friends

    @property
    def workers(self):
        return self._workers

    def step(self) -> None:
        pass

    def consume(self) -> None:
        pass


class HouseholdBuilder(AgentBuilder):  # TODO: implement
    def __call__(self, manager: AgentManager, unique_id: int, **kwargs):
        """Creates and returns a household agent."""
        pass
