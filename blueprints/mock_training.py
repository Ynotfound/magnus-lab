from magnus import submit_job

if __name__ == "__main__":
    submit_job(
        branch="main",
        namespace="Ynotfound",
        repo_name="magnus-lab",
        command="python blueprints/mock_training_executor.py"
    )