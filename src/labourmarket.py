from __future__ import annotations

from environment import Environment, AgentManager, AgentScheduler
from collector import Collector
from agent import AgentBuilder
from workers import SpecialisingWorker
from skills import YEARS_TO_SPECIALISE


class Worker(SpecialisingWorker):
    def step(self, week: bool) -> None:
        """Workers daily and weekly activities."""
        if not self._employed:
            if week:
                self._reservation_wage = max(self._reservation_wage - self._alpha, 0.0)

            if self._is_training:
                if self._time_training < YEARS_TO_SPECIALISE[self._training_specialisation] * 365:
                    self._time_training += 1
                else:
                    self.train(self._training_specialisation)
                    self._is_training = False
                return

            if self._time_unemployed >= self._unemployment_limit:
                self.start_training()
                return

            self.search_for_jobs()
            self.apply_to_jobs()
            self.find_training_opportunities()

            self._time_unemployed += 1


class WorkerBuilder(AgentBuilder):  # TODO: implement
    def __call__(self, manager: AgentManager, unique_id: int, **kwargs):
        """Creates and returns a worker agent."""
        pass


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
