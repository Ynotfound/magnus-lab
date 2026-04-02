from magnus import submit_job, JobType

def blueprint():
    submit_job(
        task_name="Agent-First-Job",
        namespace="HET-AGI",
        repo_name="Magnus-Demo",
        commit_sha="HEAD",
        entry_command="echo 'Success! My Agent is working!'",
        container_image="docker://python:3.11-slim",
        job_type=JobType.B2
    )