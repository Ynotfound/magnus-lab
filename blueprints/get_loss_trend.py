import sys
import re
import json


def main(job_id):
    try:
        from magnus import MagnusClient
        client = MagnusClient()
        logs = client.get_job_logs(job_id)

        # Handle logs wrapped in dict string format
        try:
            import ast
            log_data = ast.literal_eval(logs)
            if isinstance(log_data, dict) and 'logs' in log_data:
                logs = log_data['logs']
        except (ValueError, SyntaxError):
            pass

        # Ensure logs is string format for regex processing
        if isinstance(logs, bytes):
            logs = logs.decode('utf-8')
        elif isinstance(logs, list):
            logs = "\n".join(logs)
        elif not isinstance(logs, str):
            logs = str(logs)
    except Exception as e:
        return {
            "job_id": job_id,
            "error": f"Failed to retrieve job logs: {str(e)}",
            "status": "error"
        }

    # Extract loss values using regex
    loss_pattern = r'(?i)loss[ :]+([0-9.]+)'
    losses = [float(match) for match in re.findall(loss_pattern, logs)]

    if not losses:
        print(f"DEBUG: First 500 chars of logs: {repr(logs[:500])}")
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