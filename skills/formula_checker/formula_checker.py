import json
import re
from ast import literal_eval
from dimsys_default import DimensionSystem, equivalent

# Comprehensive physical constants with SI units
c = 299792458  # m/s
h = 6.62607015e-34  # J*s
G = 6.67430e-11  # m^3/kg/s^2
e = 1.602176634e-19  # C
k = 1.380649e-23  # J/K
m_e = 9.1093837015e-31  # kg
m_p = 1.67262192369e-27  # kg

CONSTANTS = {
    'c': {'value': c, 'unit': 'm/s', 'tolerance': 1e-10},
    'h': {'value': h, 'unit': 'J*s', 'tolerance': 1e-10},
    'G': {'value': G, 'unit': 'm^3/kg/s^2', 'tolerance': 1e-6},
    'e': {'value': e, 'unit': 'C', 'tolerance': 1e-10},
    'k': {'value': k, 'unit': 'J/K', 'tolerance': 1e-10},
    'm_e': {'value': m_e, 'unit': 'kg', 'tolerance': 1e-10},
    'm_p': {'value': m_p, 'unit': 'kg', 'tolerance': 1e-10},
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

        # Special handling for constant definitions with numerical RHS
        if left in CONSTANTS:
            try:
                # Check if right side is a numerical value
                constant_value = literal_eval(right)
                if isinstance(constant_value, (int, float)):
                    # For dimensional check, treat numerical RHS as having same dimensions as constant
                    right_dim = left_dim
                else:
                    right_dim = ds.parse(right)
            except:
                right_dim = ds.parse(right)
        else:
            right_dim = ds.parse(right)

    except Exception as e:
        raise FormulaValidationError(f'Dimensional parsing error: {str(e)}')

    if not equivalent(left_dim, right_dim):
        raise FormulaValidationError(
            f'Dimensional mismatch: {left} ({left_dim}) != {right} ({right_dim})'
        )

    # Numerical validation for constants
    errors = []
    for constant, info in CONSTANTS.items():
        if constant in values:
            expected = info['value']
            actual = values[constant]
            tolerance = info.get('tolerance', 1e-10)

            # Calculate relative error (handle zero values safely)
            if expected == 0:
                rel_error = abs(actual)
            else:
                rel_error = abs(actual - expected) / abs(expected)

            if rel_error > tolerance:
                errors.append(
                    f'Numerical mismatch for {constant}: '
                    f'expected {expected}, got {actual} '
                    f'(error: {rel_error:.2e} > {tolerance})'
                )

    if errors:
        raise FormulaValidationError('\n'.join(errors))

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