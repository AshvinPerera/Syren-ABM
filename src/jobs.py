from __future__ import annotations

from dataclasses import dataclass
from skills import Specialisation


@dataclass(slots=True, frozen=True)
class JobReference:
    """Lightweight, hashable reference to a unique vacancy."""
    firm_id: int
    job_id: int


@dataclass(slots=True, frozen=True)
class JobDetails:
    """Stores the details of a job."""
    satisficing_wage: float
    specialisation: Specialisation | None = None


class JobBoard:
    _board: dict[JobReference, JobDetails]
    _popularity: int

    def __init__(self, popularity: int = None):
        self._board = {}
        self._popularity = popularity

    def __getitem__(self, name):
        return self._board[name]

    def __iter__(self):
        return iter(self._board)

    def keys(self):
        return self._board.keys()

    def items(self):
        return self._board.items()

    def values(self):
        return self._board.values()

    @property
    def popularity(self):
        return self._popularity

    @popularity.setter
    def popularity(self, popularity):
        self._popularity = popularity

    def register(self, firm_id: int, job_id: int, wage_offered: float, specialisation: Specialisation) -> None:
        job = JobReference(firm_id, job_id)
        self._board[job] = JobDetails(wage_offered, specialisation)

    def deregister(self, firm_id: int, job_id: int) -> None:
        job = JobReference(firm_id, job_id)
        self._board.pop(job, None)
