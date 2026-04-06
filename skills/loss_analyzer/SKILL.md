# get_loss_trend Skill Specification

## Description
Extracts and analyzes loss values from training job logs to determine model training trends.

## Inputs
- **job_id** (string): Unique identifier of the training job to analyze

## Outputs
The skill returns a JSON object with the following structure:

```json
{
  "job_id": "string",
  "losses": [float],
  "status": "string"
}
```

- **losses**: Array of floating-point loss values extracted in chronological order
- **status**: Trend analysis result with possible values:
  - `"decreasing"`: Loss values show a downward trend
  - `"increasing"`: Loss values show an upward trend
  - `"stable"`: Loss values remain relatively constant
  - `"single_value"`: Only one loss value was found
  - `"error"`: Error occurred during processing

## Execution Requirements
- Magnus client must be properly configured
- Job logs must contain loss values in format `loss: <value>`
- Python 3.8+ environment with required dependencies

## Example Usage
```bash
python blueprints/get_loss_trend.py --job_id "training-123"
```

## Example Output
```json
{
  "job_id": "training-123",
  "losses": [0.85, 0.72, 0.61, 0.53],
  "status": "decreasing"
}
```

# Loss Trend Analysis Robustness Report

| Scenario | Status | Details |
|----------|--------|---------|
| Scenario A (Empty Logs) | PASSED | error |
| Scenario B (No Metrics) | PASSED | error |
| Scenario C (NaN/Inf) | PASSED | error |
| Scenario D (Format Variations) | PASSED |  |
| Scenario E (Invalid ID) | PASSED | error |