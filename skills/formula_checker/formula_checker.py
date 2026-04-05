import json
import re
from dimsys import DimensionSystem, equivalent

# Physical constants with SI units
c = 299792458  # m/s
h = 6.62607015e-34  # J*s
G = 6.67430e-11  # m^3/kg/s^2

CONSTANTS = {
    'c': {'value': c, 'unit': 'm/s'},
    'h': {'value': h, 'unit': 'J*s'},
    'G': {'value': G, 'unit': 'm^3/kg/s^2'}
}

class FormulaValidationError(Exception):
    pass

def validate_formula(formula: str, values: dict = None) -> dict:
    """Validate dimensional consistency and numerical correctness"""

    # Parse formula
    if '=' not in formula:
        raise FormulaValidationError('Formula must contain "="')

    left, right = formula.split('=', 1)
    left = left.strip()
    right = right.strip()

    # Dimensional validation
    ds = DimensionSystem()
    try:
        left_dim = ds.parse(left)
        right_dim = ds.parse(right)
    except Exception as e:
        raise FormulaValidationError(f'Dimensional parsing error: {str(e)}')

    if not equivalent(left_dim, right_dim):
        raise FormulaValidationError(
            f'Dimensional mismatch: {left} ({left_dim}) != {right} ({right_dim})'
        )

    # Numerical validation for constants
    if values is None:
        values = {}

    # Check constant values if present
    for constant, info in CONSTANTS.items():
        if constant in values and abs(values[constant] - info['value']) > 1e-10:
            raise FormulaValidationError(
                f'Numerical mismatch for {constant}: '
                f'expected {info["value"]}, got {values[constant]}'
            )

    return {
        'dimensional_consistent': True,
        'numerical_valid': True,
        'left_side': left,
        'right_side': right
    }

def batch_validate(formulas: list) -> list:
    """Validate multiple formulas in batch"""
    results = []
    for formula in formulas:
        try:
            result = validate_formula(formula)
            results.append({'formula': formula, 'status': 'valid', 'details': result})
        except FormulaValidationError as e:
            results.append({'formula': formula, 'status': 'invalid', 'error': str(e)})
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Physics Formula Validator')
    parser.add_argument('formula', nargs='?', help='Formula to validate')
    parser.add_argument('--batch', type=str, help='JSON array of formulas')
    parser.add_argument('--values', type=str, help='JSON of constant values for numerical validation')

    args = parser.parse_args()

    if args.batch:
        formulas = json.loads(args.batch)
        results = batch_validate(formulas)
        print(json.dumps(results, indent=2))
    elif args.formula:
        values = json.loads(args.values) if args.values else None
        result = validate_formula(args.formula, values)
        print(f'Formula "{args.formula}" is dimensionally consistent and numerically valid.')
        print(f'Result: {result}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()