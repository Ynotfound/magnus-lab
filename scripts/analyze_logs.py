import os
import sys
import re
import json


def main(job_id):
    # Attempt to get logs from Magnus
    try:
        from magnus import MagnusClient
        client = MagnusClient()
        logs = client.get_job_logs(job_id)
    except Exception:
        # Fallback to local logs for testing/development
        log_path = os.path.join('logs', job_id, 'stdout.log')
        try:
            with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
                logs = f.read()
        except Exception as e:
            print(json.dumps({
                "job_id": job_id,
                "status": "error",
                "message": "Job logs not found",
                "reason": str(e)
            }))
            return

    # Wrap all processing in try-except to prevent crashes
    try:
        # Handle JSON-wrapped logs
        if isinstance(logs, str):
            try:
                log_data = json.loads(logs)
                if isinstance(log_data, dict) and 'logs' in log_data:
                    logs = log_data['logs']
            except (json.JSONDecodeError, TypeError):
                try:
                    import ast
                    log_data = ast.literal_eval(logs)
                    if isinstance(log_data, dict) and 'logs' in log_data:
                        logs = log_data['logs']
                except (ValueError, SyntaxError):
                    pass

        # Normalize logs to string
        if isinstance(logs, bytes):
            logs = logs.decode('utf-8', errors='replace')
        elif isinstance(logs, list):
            logs = "\n".join(logs)
        elif not isinstance(logs, str):
            logs = str(logs)

        # Check for empty logs
        if not logs.strip():
            print(json.dumps({
                "job_id": job_id,
                "status": "error",
                "message": "Empty log file",
                "reason": "No content to analyze"
            }))
            return

        # Comprehensive pattern matching for loss metrics (fixed regex patterns)
        patterns = [
            r'(?i)loss[ :]+([\\d.]+|nan|inf)',
            r'(?i)current loss[ =]+([\\d.]+|nan|inf)',
            r'(?i)training loss[ :]+([\\d.]+|nan|inf)',
            r'(?i)val_loss[ :]+([\\d.]+|nan|inf)'
        ]

        losses = []
        nan_inf_count = 0

        for pattern in patterns:
            for match in re.findall(pattern, logs, re.IGNORECASE):
                match_lower = match.lower()
                if match_lower in ['nan', 'inf']:
                    nan_inf_count += 1
                else:
                    try:
                        losses.append(float(match))
                    except (ValueError, TypeError):
                        continue

        # Handle invalid values
        if nan_inf_count > 0:
            print(json.dumps({
                "job_id": job_id,
                "status": "error",
                "message": "Invalid loss values detected",
                "reason": f"Found {nan_inf_count} NaN/Inf values"
            }))
            return

        # Handle missing metrics
        if not losses:
            print(json.dumps({
                "job_id": job_id,
                "status": "error",
                "message": "No valid loss metrics found",
                "reason": "Log format doesn't match expected patterns"
            }))
            return

        # Determine trend
        trend = "decreasing" if losses and losses[-1] < losses[0] else "increasing"
        print(json.dumps({
            "job_id": job_id,
            "losses": losses,
            "status": trend
        }, indent=2))

    except Exception as e:
        print(json.dumps({
            "job_id": job_id,
            "status": "error",
            "message": "Internal processing error",
            "reason": str(e)
        }))



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({
            "status": "error",
            "message": "Job ID required",
            "reason": "Please provide exactly one job ID"
        }))
        sys.exit(1)

    main(sys.argv[1])