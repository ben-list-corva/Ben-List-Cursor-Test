"""In-memory job tracking for background pipeline runs."""

import uuid
from typing import Optional


_jobs: dict[str, dict] = {}


def create_job() -> str:
    job_id = uuid.uuid4().hex[:12]
    _jobs[job_id] = {
        "status": "pending",
        "progress": "Queued",
        "step": 0,
        "total_steps": 8,
        "error": None,
        "section_name": None,
    }
    return job_id


def get_job(job_id: str) -> Optional[dict]:
    return _jobs.get(job_id)


def update_job(job_id: str, **kwargs):
    if job_id in _jobs:
        _jobs[job_id].update(kwargs)


def list_jobs() -> dict[str, dict]:
    return dict(_jobs)
