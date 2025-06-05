from __future__ import annotations

from typing import TypeVar
from collections import deque
import itertools

from agent import AgentFactory, Agent
from abc import ABC, abstractmethod


T = TypeVar('T', bound='Agent')
U = TypeVar('U', bound='AgentScheduler')


class AgentManager:
    _id_generator = itertools.count()
    _id_bank = deque([])

    _factory: AgentFactory
    _agents: dict[int, Agent]
    _agents_by_name: dict[str, set[int]]
    _config: list[dict]

    def __init__(self, build_dict: dict, config: list):
        self._factory = AgentFactory()
        self._register(build_dict)
        self._agents = {}
        self._agents_by_name = {}
        self.config = config
        if config:
            self.reload()

    def __iter__(self):
        return iter(self._agents.values())

    @property
    def config(self) -> list:
        """Get the agent configuration currently registered with the instance."""
        return self._config

    @config.setter
    def config(self, config: list) -> None:
        """Register a new agent configuration."""
        self._config = config

    @property
    def agent_ids(self):
        return list(self._agents.keys())

    def reload(self):
        """Load the agents into memory based on the build configuration."""
        self._agents.clear()
        self._agents_by_name.clear()

        if self._config:
            for agent_details in self._config:
                self._create_agents(agent_details)
        else:
            self._agents = {}
            self._agents_by_name = {}

    def create(self, name: str, **kwargs) -> Agent:
        """Build a new agent based on a specific set of attributes using the agent factory."""
        unique_id = self._next_id()
        agent = self._factory.create(name, manager=self, unique_id=unique_id, **kwargs)
        self._agents[unique_id] = agent
        self._agents_by_name.setdefault(name, set()).add(unique_id)
        return agent

    def destroy(self, unique_id: int) -> None:
        """Destroy an agent with a specific unique id and recover that id for later assignment."""
        agent = self._agents.pop(unique_id, None)
        if agent is None:
            return

        bucket = self._agents_by_name.get(agent.name)
        if bucket is not None:
            bucket.discard(unique_id)
            if not bucket:
                del self._agents_by_name[agent.name]

        agent.on_kill()
        self._recover_id(unique_id)

    def get_agent_by_id(self, unique_id: int) -> T | None:
        """Retrieve a single agent based on their unique id."""
        return self._agents.get(unique_id)

    def get_agents_by_attr(self, **kwargs) -> list[T]:
        """Retrieve multiple agents based on matching attributes."""
        agents = []
        for agent in self._agents.values():
            if self._match(agent, **kwargs):
                agents.append(agent)
        return agents

    def _register(self, build_dict: dict) -> None:
        """Register all builders in the factory member object."""
        for key, builder in build_dict.items():
            self._factory.register(key, builder)

    def _next_id(self) -> int:
        """Get the next unique id for an agent from an updated count or from past deleted agents."""
        if self._id_bank:
            return self._id_bank.popleft()
        return next(self._id_generator)

    def _recover_id(self, unique_id: int) -> None:
        """Save a unique id from a deleted agent for later assignment to a new agent ."""
        self._id_bank.append(unique_id)

    def _create_agents(self, agent_details: dict):
        """Loop through the config dict and create each agent based on the agent's specification."""
        for _ in range(agent_details['Count']):
            self.create(agent_details['Name'], **agent_details['Parameters'])

    @staticmethod
    def _match(agent: Agent, **query) -> bool:
        """Return True iff all attributes satisfy their predicates/values."""
        for attr, wanted in query.items():
            value = getattr(agent, attr, None)
            if callable(wanted):
                if not wanted(value):
                    return False
            elif value != wanted:
                return False
        return True


class AgentScheduler(ABC):
    _manager: AgentManager
    _agents: list[int]
    _order: list[int]

    def __init__(self, manager: AgentManager, order: list[int]):
        self._manager = manager
        self._agents = manager.agent_ids
        self._order = order

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    def refresh(self) -> None:
        """Synchronise with any agents created/destroyed since last step."""
        live = set(self._manager.agent_ids)
        self._agents = [unique_id for unique_id in self._agents if unique_id in live]
        self._agents.extend(live.difference(self._agents))
        self._reorder()

    @abstractmethod
    def step(self) -> None:
        """Run each agent according to the prescribed order."""
        pass

    @abstractmethod
    def _reorder(self) -> None:
        """Reorder agent execution."""
        pass


class Environment(ABC):
    _manager: AgentManager
    _scheduler: AgentScheduler
    _iterations: int

    def __init__(self, manager: AgentManager, scheduler: U, iterations: int):
        self._manager = manager
        self._scheduler = scheduler
        self._iterations = iterations

    def run(self) -> None:
        for _ in range(self._iterations):
            self._scheduler.step()
            self._scheduler.refresh()

    @abstractmethod
    def load(self, configuration: dict) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def render(self):
        pass
