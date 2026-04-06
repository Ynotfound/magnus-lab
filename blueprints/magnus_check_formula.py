from magnus import submit_job

if __name__ == "__main__":
    job_id = submit_job(
        branch="main",
        namespace="Ynotfound",
        repo_name="magnus-lab",
        job_type="B2",
        task_name="formula_check",
        entry_command="python scripts/run_formula_checker.py '{formula}'"
    )
    print(f"Submitted formula check job with ID: {job_id}")