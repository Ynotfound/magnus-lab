import sys
import json
import sympy as sp


def check_formula(formula):
    try:
        # Parse formula using SymPy
        expr = sp.sympify(formula)

        # Basic dimensional analysis (simplified example)
        variables = expr.free_symbols
        if not variables:
            return {
                "status": "error",
                "message": "Formula contains no variables",
                "formula": formula
            }

        return {
            "status": "valid",
            "formula": formula,
            "variables": [str(v) for v in variables]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "formula": formula
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "Formula required",
            "reason": "Please provide a formula as argument"
        }))
        sys.exit(1)

    formula = ' '.join(sys.argv[1:])
    result = check_formula(formula)
    print(json.dumps(result, indent=2))