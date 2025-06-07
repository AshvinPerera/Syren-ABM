from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum
import random

from agent import Agent
from environment import AgentManager
from households import Household
from jobs import JobReference, JobDetails, JobBoard
from skills import Skill, Specialisation, SPECIALISATION_TO_SKILL


@dataclass(slots=True, frozen=True)
class CV:
    skill: Skill
    specialisations: list[Specialisation]


class AccessMethod(Enum):
    Random = 1
    Ordered = 2


class BaseWorker(Agent, ABC):
    _household: Household
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
            reservation_wage
    ):
        super().__init__(manager, unique_id, 'Worker')
        self._household = household
        self._reservation_wage = reservation_wage

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


class JobSearchingWorker(BaseWorker, ABC):
    _job_boards: list[JobBoard]
    _jobs: dict[JobReference, JobDetails]
    _seen_jobs: set[JobReference]
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

    def __init__(self, manager, unique_id, household,
                 search_method,
                 application_method,
                 reservation_wage,
                 alpha: float,
                 search_rate: float,
                 pi: float,
                 search_max: int,
                 application_rate: float,
                 application_max: int):

        super().__init__(manager, unique_id, household, reservation_wage)
        self._job_boards = []
        self._jobs = {}
        self._seen_jobs = set()
        self._cached_weights = []
        self._search_method = search_method
        self._search_count = 0
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

    def search_for_jobs(self) -> None:
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

    def apply_to_jobs(self) -> None:
        """Apply for jobs if any jobs are available."""
        if random.random() >= self._application_rate:
            return

        if list(self._jobs.keys()):
            self._apply_to_job()

    def _add_job(self, job_reference: JobReference, job_details: JobDetails) -> None:
        """Add a job to the application list."""
        if job_reference not in self._seen_jobs:
            self._jobs[job_reference] = job_details
            self._seen_jobs.add(job_reference)

    def _clear_applied(self, refs: list[JobReference]) -> None:
        """Remove all jobs the worker has applied to."""
        for ref in refs:
            self._seen_jobs.discard(ref)
            self._jobs.pop(ref, None)

    def _search_board(self, job_board: JobBoard) -> None:
        """Search for jobs on a job board."""
        self._search_count = 0
        job_references = list(job_board.keys())
        job_details = list(job_board.values())
        wages = [value.satisficing_wage for value in job_details]

        perm = self._order(job_references, wages)
        self._search(perm, job_references, job_details)

    def _search_network(self) -> None:
        """Search for jobs on the household social network."""
        self._search_count = 0
        for friend_id in self._household.friends:
            friend_household = self._manager.get_agent_by_id(friend_id)
            for worker in friend_household.workers:
                job_references = list(worker.jobs.keys())
                job_details = list(worker.jobs.values())
                wages = [value.satisficing_wage for value in job_details]

                perm = self._order(job_references, wages)
                self._search(perm, job_references, job_details)

    def _search(self, perm: list[int], job_references: list[JobReference], job_details: list[JobDetails]):
        for index in perm:
            if self._search_count < self._search_max:
                job_reference = job_references[index]
                job_information = job_details[index]
                wage = job_information.satisficing_wage
                if wage >= self._reservation_wage:
                    self._add_job(job_reference, job_information)
                self._search_count += 1
            else:
                break

    def _apply_to_job(self):
        """Apply for jobs saved to the application list."""
        applications = 0
        jobs_to_delete = []

        job_references = list(self._jobs.keys())
        job_details = list(self._jobs.values())
        wages = [value.satisficing_wage for value in job_details]

        selection = self._select(job_references, job_details)
        selected_job_references = [job_references[i] for i in selection]
        selected_wages = [wages[i] for i in selection]

        perm = self._order(selected_job_references, selected_wages)

        for index in perm:
            if applications < self._application_max:
                self._apply(selected_job_references[index], self.unique_id)
                jobs_to_delete.append(selected_job_references[index])
                applications += 1
            else:
                break

        self._clear_applied(jobs_to_delete)

    def _apply(self, job_reference: JobReference, worker_id: int):
        firm = self._manager.get_agent_by_id(job_reference.firm_id)
        firm.apply(job_reference.job_id, worker_id)

    @staticmethod
    def _select(job_references: list[JobReference], job_details: list[JobDetails]) -> list[int]:
        return list(range(len(job_references)))

    def _order(self, job_references: list[JobReference], wages: list[float]) -> list[int]:
        if self._search_method is AccessMethod.Random:
            perm = random.sample(range(len(job_references)), k=len(job_references))
        elif self._search_method is AccessMethod.Ordered:
            perm = sorted(range(len(wages)), key=lambda k: wages[k], reverse=True)
        else:
            perm = list(range(len(job_references)))
        return perm


class SpecialisingWorker(JobSearchingWorker, ABC):
    _time_unemployed: int
    _unemployment_limit: int
    _is_training: bool
    _training_rate: float
    _time_training: int
    _training_specialisation: Specialisation | None
    _max_general_skill: Skill
    _skill_level: Skill
    _specialisations: set[Specialisation]
    _search_history: dict[Specialisation: int]

    def __init__(self, manager, unique_id, household, reservation_wage,
                 training_rate,
                 max_general_skill,
                 unemployment_limit,
                 skill: Skill,
                 specialisation: Specialisation):
        super().__init__(manager, unique_id, household, skill, reservation_wage)
        self._time_unemployed = 0
        self._unemployment_limit = unemployment_limit
        self._is_training = False
        self._training_rate: training_rate
        self._time_training = 0
        self._training_specialisation = None
        self._max_general_skill = max_general_skill
        self._skill_level = skill
        self._specialisations = {specialisation}
        self._search_history = {}

    @property
    def skill(self):
        return self._skill_level

    @property
    def specialisations(self):
        return self._specialisations

    def train(self, specialisation: Specialisation):
        self._specialisations.add(specialisation)
        self._skill_level = max(self._skill_level, SPECIALISATION_TO_SKILL(specialisation))

    def start_training(self):
        if self._search_history and random.random() < self._training_rate:
            specialisations = list(self._search_history.keys())
            weights = list(self._search_history.values())
            self._training_specialisation = random.choices(specialisations, weights=weights, k=1)[0]

            self._search_history = {}
            self._is_training = True
            self._time_training = 0
            self._time_unemployed = 0

    def stop_training(self):
        self._is_training = False

    def find_training_opportunities(self):
        if self._jobs:
            job_references = list(self._jobs.keys())
            job_details = list(self._jobs.values())

            selected_job_references = [
                job_references[index] for index in range(len(job_references))
                if job_details[index].specialisation not in self.specialisations
                and SPECIALISATION_TO_SKILL[job_details[index].specialisation] > self._max_general_skill
            ]

            selected_job_details = [
                job_details[index] for index in range(len(job_details))
                if job_details[index].specialisation not in self.specialisations
                and SPECIALISATION_TO_SKILL[job_details[index].specialisation] > self._max_general_skill
            ]

            for job_detail in selected_job_details:
                if job_detail.specialisation in self._search_history.keys():
                    self._search_history[job_detail.specialisation] += 1
                else:
                    self._search_history[job_detail.specialisation] = 1

            self._clear_applied(selected_job_references)

    def _select(self, job_references: list[JobReference], job_details: list[JobDetails]) -> list[int]:
        return [index for index in range(len(job_references))
                if job_details[index].specialisation in self.specialisations
                or SPECIALISATION_TO_SKILL[job_details[index].specialisation] <= self._max_general_skill]
