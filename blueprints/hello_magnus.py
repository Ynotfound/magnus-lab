from magnus import submit_job, JobType
import subprocess

def get_current_commit():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()

def get_current_branch():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

def blueprint():
    return submit_job(
        task_name="Agent-First-Job",
        namespace="Ynotfound",
        repo_name="magnus-lab",
        default_branch="main",
        commit_sha=get_current_commit(),
        entry_command="echo 'Success! My Agent is working!'",
        container_image="docker://python:3.11-slim",
        job_type=JobType.B2
    )
if __name__ == "__main__":
    job_id = blueprint()
    print(f"Job ID: {job_id}")