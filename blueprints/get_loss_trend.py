import sys
import re
import json


def main(job_id):
    try:
        import magnus.client
        client = magnus.client.get_client()
        logs = client.get_job_logs(job_id)
    except Exception as e:
        return {
            "job_id": job_id,
            "error": f"Failed to retrieve job logs: {str(e)}",
            "status": "error"
        }

    # Extract loss values using regex
    loss_pattern = r'loss:\s*([\d.]+)'
    losses = [float(match) for match in re.findall(loss_pattern, logs)]

    if not losses:
        return {
            "job_id": job_id,
            "error": "No loss values found in logs",
            "status": "error"
        }

    # Determine trend status
    if len(losses) > 1:
        if losses[-1] < losses[0]:
            status = "decreasing"
        elif losses[-1] > losses[0]:
            status = "increasing"
        else:
            status = "stable"
    else:
        status = "single_value"

    return {
        "job_id": job_id,
        "losses": losses,
        "status": status
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({
            "error": "Usage: python get_loss_trend.py <job_id>",
            "status": "error"
        }))
        sys.exit(1)

    job_id = sys.argv[1]
    result = main(job_id)
    print(json.dumps(result, indent=2))