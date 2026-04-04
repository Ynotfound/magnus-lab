# magnus_check_formula()

**Layer**: L0.5 (Hallucination Detection)  
**Safety Level**: L1  
**Author**: Phy-LLM AI Infrastructure Team  
**Last Updated**: 2026-04-04

## Description
Validates the mathematical correctness and dimensional consistency of physics formulas to detect hallucinations in AI-generated scientific content.

## Input Parameters
| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| formula | string | Physics formula to validate (e.g., "F = m * a") | Yes |

## Output
```json
{
  "is_valid": bool,
  "error": string | null
}
```

## Dependencies
- Python 3.10+
- sympy >= 1.12 (`pip install sympy`)

## Workflow
1. Parse formula for mathematical validity
2. Check dimensional consistency using physics unit system
3. Return validation result

## Example Usage
```python
result = formula_check_task("F = m * a")
# Returns: {"is_valid": true, "error": null}

result = magnus_check_formula("E = m * c")
# Returns: {"is_valid": false, "error": "Dimensional mismatch: energy vs mass*velocity"}
```

## Implementation Notes
- Only validates equations (must contain '=')
- Uses predefined mapping of common physics symbols to dimensions
- Returns detailed error messages for debugging