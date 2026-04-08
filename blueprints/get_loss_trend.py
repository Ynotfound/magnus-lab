from magnus import submit_job
from typing import Literal
from typing_extensions import Annotated

TargetJobId = Annotated[str, {
    "label": "Target Job ID",
    "placeholder": "ID of the training job"
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

def blueprint(target_job_id: TargetJobId, priority: Priority = "B2"):
    submit_job(
        branch="main",
        namespace="Rise-AGI",
        repo_name="Agentification-of-AI-Infra",
        job_type=priority,
        task_name="get_loss_trend",
        entry_command=f"python scripts/analyze_logs.py '{target_job_id}'"
    )