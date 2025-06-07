from __future__ import annotations

from abc import ABC
from enum import Enum
import random

from agent import Agent, AgentBuilder
from environment import AgentManager
from households import Household
from jobs import JobRef, JobBoard
from skills import Skill, Specialisation, YEARS_TO_SPECIALISE


class AccessMethod(Enum):
    Random = 1
    Ordered = 2


class BaseWorker(Agent, ABC):
    _household: Household
    _skill_level: Skill
    _employed: bool = False
    _firm_id: int | None = None
    _job_id: int | None = None
    _wage: float | None = None

    # Hyperparameter
    _reservation_wage: float

    def __init__(
            self,
            manager: AgentManager,
            unique_id: int,
            household: Household,
            skill: Skill,
            reservation_wage
    ):
        super().__init__(manager, unique_id, 'Worker')
        self._household = household
        self._skill_level = skill
        self._reservation_wage = reservation_wage

    @property
    def skill(self):
        return self._skill_level

    @property
    def employed(self):
        return self._employed

    def employ(self, firm_id: int, job_id: int, wage: float) -> None:
        """Employs the worker in the firm if they are currently unemployed."""
        if not self._employed:
            self._employed = True
            self._firm_id = firm_id
            self._job_id = job_id
            self._wage = wage

    def unemploy(self) -> None:
        """Unemploys the worker, setting their reservation wage to the last earned wage."""
        if self._employed:
            self._employed = False
            self._reservation_wage = self._wage

    def train(self, skill: Skill) -> None:
        """Increase the worker's skill level from training received."""
        if skill > self._skill_level:
            self._skill_level = skill


class JobSearchingWorker(BaseWorker, ABC):
    _job_boards: list[JobBoard]
    _jobs: dict[JobRef, float]
    _seen_jobs: set[JobRef]
    _cached_weights: list[float]
    _search_method: AccessMethod
    _application_method: AccessMethod

    # Hyperparameters
    _alpha: float
    _search_rate: float
    _pi: float
    _search_max: int
    _application_rate: float
    _application_max: int

    def __init__(self, manager, unique_id, household, skill,
                 search_method,
                 application_method,
                 reservation_wage,
                 alpha: float,
                 search_rate: float,
                 pi: float,
                 search_max: int,
                 application_rate: float,
                 application_max: int):

        super().__init__(manager, unique_id, household, skill, reservation_wage)
        self._job_boards = []
        self._jobs = {}
        self._seen_jobs = set()
        self._cached_weights = []
        self._search_method = search_method
        self._application_method = application_method

        self._alpha = alpha
        self._search_rate = search_rate
        self._pi = pi
        self._search_max = search_max
        self._application_rate = application_rate
        self._application_max = application_max

    @property
    def jobs(self):
        return self._jobs

    def add_job_board(self, board: JobBoard):
        """Adds a job board to the worker's list of registered boards."""
        if board not in self._job_boards:
            self._job_boards.append(board)
            self.update_board_weights()

    def update_board_weights(self) -> None:
        """Adjust board weights based on their popularity."""
        pops = [jb.popularity for jb in self._job_boards]
        pops = [p or 0 for p in pops]
        total = sum(pops)
        if total <= 0:
            weights = None
        else:
            weights = [p/total for p in pops]
        self._cached_weights = weights

    def job_search(self) -> None:
        """Search for a job if any search mechanisms are available."""
        has_boards = bool(self._job_boards)
        has_friends = bool(self._household.friends)
        if not (has_boards or has_friends):
            return

        if random.random() >= self._search_rate:
            return

        self.update_board_weights()

        if has_boards and has_friends:
            if random.random() < self._pi:
                board, weights = self._job_boards, self._cached_weights
                chosen_board = random.choices(board, weights=weights, k=1)[0]
                self._search_board(chosen_board)
            else:
                self._search_network()
        elif has_boards:
            board, weights = self._job_boards, self._cached_weights
            chosen_board = random.choices(board, weights=weights, k=1)[0]
            self._search_board(chosen_board)
        else:
            self._search_network()

    def job_application(self) -> None:
        """Apply for jobs if any jobs are available."""
        if random.random() >= self._application_rate:
            return

        if list(self._jobs.keys()):
            self._apply()

    def _add_job(self, firm_id: int, job_id: int, wage_offered: float) -> None:
        """Add a job to the application list."""
        ref = JobRef(firm_id, job_id)
        if ref not in self._seen_jobs:
            self._jobs[ref] = wage_offered
            self._seen_jobs.add(ref)

    def _clear_applied(self, refs: list[JobRef]) -> None:
        """Remove all jobs the worker has applied to."""
        for ref in refs:
            self._seen_jobs.discard(ref)
            self._jobs.pop(ref, None)

    def _search_board(self, job_board: JobBoard) -> None:
        """Search for jobs on a job board."""
        search_count = 0
        jobs = list(job_board.keys())
        wages = list(job_board.values())

        if self._search_method is AccessMethod.Random:
            perm = random.sample(range(len(jobs)), k=len(jobs))
        elif self._search_method is AccessMethod.Ordered:
            perm = sorted(range(len(wages)), key=lambda k: wages[k], reverse=True)
        else:
            perm = list(range(len(jobs)))

        for index in perm:
            if search_count < self._search_max:
                firm_id = jobs[index].firm_id
                job_id = jobs[index].job_id
                wage = wages[index]
                if wages[index] >= self._reservation_wage:
                    self._add_job(firm_id, job_id, wage)
                search_count += 1
            else:
                break

    def _search_network(self) -> None:
        """Search for jobs on the household social network."""
        search_count = 0

        for friend_id in self._household.friends:
            friend_household = self._manager.get_agent_by_id(friend_id)
            for worker in friend_household.workers:
                jobs = worker.jobs.keys()
                wages = worker.jobs.values()

                if self._search_method is AccessMethod.Random:
                    perm = random.sample(range(len(jobs)), k=len(jobs))
                elif self._search_method is AccessMethod.Ordered:
                    perm = sorted(range(len(wages)), key=lambda k: wages[k], reverse=True)
                else:
                    perm = list(range(len(jobs)))

                for index in perm:
                    if search_count < self._search_max:
                        firm_id = jobs[index].firm_id
                        job_id = jobs[index].job_id
                        wage = wages[index]
                        if wages[index] >= self._reservation_wage:
                            self._add_job(firm_id, job_id, wage)
                        search_count += 1
                    else:
                        break

    def _apply(self):
        """Apply for jobs saved to the application list."""
        applications = 0
        jobs_to_delete = []
        jobs = list(self._jobs.keys())

        if self._application_method is AccessMethod.Random:
            perm = random.sample(range(len(self._jobs)), k=len(self._jobs))
        elif self._application_method is AccessMethod.Ordered:
            wages = list(self._jobs.values())
            perm = sorted(range(len(wages)), key=lambda k: wages[k], reverse=True)
        else:
            perm = list(range(len(self._jobs)))

        for index in perm:
            if applications < self._application_max:
                firm = self._manager.get_agent_by_id(jobs[index].firm_id)
                firm.apply(jobs[index].job_id, self.unique_id)
                jobs_to_delete.append(jobs[index])
                applications += 1
            else:
                break

        self._clear_applied(jobs_to_delete)


class SpecialisingWorker(BaseWorker, ABC):  # TODO: implement
    _specialisations: list[Specialisation]
    _application_history: list

    def __init__(self, manager, unique_id, household, skill, reservation_wage):
        super().__init__(manager, unique_id, household, skill, reservation_wage)
