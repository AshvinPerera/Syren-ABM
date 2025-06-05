from __future__ import annotations

from environment import AgentManager
from abc import ABC, abstractmethod


class Agent(ABC):
    _manager: AgentManager
    _unique_id: int
    _name: str
    _registered: list

    def __init__(self, manager: AgentManager, unique_id: int, name: str, registered: list = None):
        self._manager = manager
        self._unique_id = unique_id
        self._name = name
        self._registered = list(registered) if registered else []

    @property
    def unique_id(self) -> int:
        """Returns the unique identifier of the agent."""
        return self._unique_id

    @property
    def name(self) -> str:
        """Returns the agents key."""
        return self._name

    def register(self, unique_id: int) -> None:
        if unique_id not in self._registered:
            self._registered.append(unique_id)

    def deregister(self, unique_id: int) -> None:
        if unique_id in self._registered:
            self._registered.remove(unique_id)

    def on_kill(self) -> None:
        for unique_id in self._registered:
            agent = self._manager.get_agent_by_id(unique_id)
            if agent:
                agent.deregister(self.unique_id)

    @abstractmethod
    def step(self, **kwargs) -> None:
        """Method called by the environment to update the agent."""
        pass


class AgentBuilder(ABC):
    @abstractmethod
    def __call__(self, manager: AgentManager, unique_id: int, **kwargs):
        """Creates and returns an agent object."""
        pass


class AgentFactory:
    def __init__(self):
        self._builders = {}

    def register(self, name: str, builder: AgentBuilder) -> None:
        """Registers an agent type and a corresponding builder function for the agent."""
        if not isinstance(builder, AgentBuilder):
            raise TypeError(f"{builder} must subclass AgentBuilder")
        if name in self._builders:
            raise KeyError(f"Agent type '{name}' already registered")
        self._builders[name] = builder

    def create(self, name: str, **kwargs) -> Agent:
        """Builds an agent based on the key (if the key exists)."""
        builder = self._builders.get(name)
        if not builder:
            raise ValueError(name)
        return builder(**kwargs)
