from __future__ import annotations

from environment import Environment, AgentManager, AgentScheduler
from collector import Collector


class DayScheduler(AgentScheduler):
    def __init__(self, manager: AgentManager, order: list[int]):
        super().__init__(manager, order)

    def step(self) -> None:
        pass

    def _reorder(self) -> None:
        pass


class MarketData:
    pass


class MarketCollector(Collector):
    pass


class LabourABM(Environment):
    def __init__(self, configuration, iterations: int):
        manager = AgentManager({}, configuration)
        scheduler = AgentScheduler(manager, [])
        super().__init__(manager, scheduler, iterations)

    def load(self, configuration) -> None:
        pass

    def reset(self) -> None:
        pass

    def collect(self):
        pass

    def render(self):
        pass


def plot_history(market_data: MarketData, **kwargs):
    pass
