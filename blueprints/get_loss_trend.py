from magnus import submit_job

if __name__ == "__main__":
    job_id = submit_job(
        branch="main",
        namespace="Ynotfound",
        repo_name="magnus-lab",
        job_type="B2",
        task_name="get_loss_trend",
        entry_command="python scripts/analyze_logs.py {job_id}"
    )
    print(f"Submitted loss analysis job with ID: {job_id}")