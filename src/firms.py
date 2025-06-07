from __future__ import annotations

from dataclasses import dataclass

from agent import Agent, AgentBuilder
from environment import AgentManager
from labour import Skill


@dataclass(slots=True)
class JobPosting:
    firm_id: int
    offered_wage: float
    required_skill: Skill = None


class Firm(Agent):  # TODO: implement
    _job_postings: dict[int, JobPosting]

    def __init__(
            self,
            manager: AgentManager,
            unique_id: int
    ):
        super().__init__(manager, unique_id, 'Worker')

    def step(self) -> None:
        pass


class FirmBuilder(AgentBuilder):  # TODO: implement
    def __call__(self, manager: AgentManager, unique_id: int, **kwargs):
        """Creates and returns a firm agent."""
        pass
