from __future__ import annotations

from agent import Agent, AgentBuilder
from environment import AgentManager


class Household(Agent):  # TODO: implement
    _size: int
    _friends: list[int]

    _employed: int
    _employable: int
    _employment: dict

    _savings: float

    def __init__(
            self,
            manager: AgentManager,
            unique_id: int,
            size: int,
            employed: int,
            employable: int,
            employment: dict,
            savings: float
    ):
        super().__init__(manager, unique_id, 'Household')

        self._size = size

        self._employed = employed
        self._employable = employable
        self._employment = employment

        self._savings = savings

    @property
    def friends(self):
        return self._friends

    def step(self) -> None:
        pass

    def consume(self) -> None:
        pass


class HouseholdBuilder(AgentBuilder):  # TODO: implement
    def __call__(self, manager: AgentManager, unique_id: int, **kwargs):
        """Creates and returns a household agent."""
        pass
