from magnus import submit_job

if __name__ == "__main__":
    job_id = submit_job(
        branch="main",
        namespace="Ynotfound",
        repo_name="magnus-lab",
        job_type="training"
    )
    print(f"Submitted job with ID: {job_id}")