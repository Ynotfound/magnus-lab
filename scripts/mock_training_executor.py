from magnus import submit_job

if __name__ == "__main__":
    job_id = submit_job(
        branch="main",
        namespace="Rise-AGI",
        repo_name="Agentification-of-AI-Infra",
        job_type="B2",
        task_name="mock_training",
        entry_command="pwd && python $(pwd)/blueprints/mock_training_executor.py"
    )
    print(f"Submitted job with ID: {job_id}")