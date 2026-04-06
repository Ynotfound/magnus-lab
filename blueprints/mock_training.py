from magnus import submit_job

if __name__ == "__main__":
    job_id = submit_job(
        branch="main",
        namespace="Ynotfound",
        repo_name="magnus-lab",
        task_name="mock_training",
        entry_command="python blueprints/mock_training_executor.py"
    )
    print(f"Submitted job with ID: {job_id}")