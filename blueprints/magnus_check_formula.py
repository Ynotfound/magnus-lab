from magnus import submit_job
from typing import Literal
from typing_extensions import Annotated

Formula = Annotated[str, {
    "label": "Physics Formula",
    "placeholder": "e.g. F = m * a"
}]

Priority = Annotated[Literal["A1", "A2", "B1", "B2"], {
    "label": "Priority",
    "description": "A1/A2: high priority (non-preemptible), B1/B2: low priority (preemptible by A)",
    "options": {
        "A1": {"label": "A1", "description": "Highest priority"},
        "A2": {"label": "A2", "description": "High priority"},
        "B1": {"label": "B1", "description": "Low priority"},
        "B2": {"label": "B2", "description": "Lowest priority"},
    }
}]

def blueprint(formula: Formula, priority: Priority = "B2"):
    submit_job(
        branch="main",
        namespace="Rise-AGI",
        repo_name="Agentification-of-AI-Infra",
        job_type=priority,
        task_name="formula_check",
        entry_command=f"python magnus_check_formula/scripts/run_formula_checker.py '{formula}'"
    )