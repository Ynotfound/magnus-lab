import json
import re
from ast import literal_eval

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

DIMENSION_MAP = {
    'm': {'L': 1},
    'kg': {'M': 1},
    's': {'T': 1},
    'c': {'L': 1, 'T': -1},
    'h': {'M': 1, 'L': 2, 'T': -1},
    'G': {'M': -1, 'L': 3, 'T': -2},
    'e': {'I': 1, 'T': 1},
    'k': {'M': 1, 'L': 2, 'T': -2, 'Theta': -1},
    'm_e': {'M': 1},
    'm_p': {'M': 1},
    # Physics variables
    'F': {'M': 1, 'L': 1, 'T': -2},  # Force
    'E': {'M': 1, 'L': 2, 'T': -2},  # Energy
    'P': {'M': 1, 'L': 2, 'T': -3},  # Power
    'm1': {'M': 1},  # Mass 1
    'm2': {'M': 1},  # Mass 2
    'r': {'L': 1},   # Radius
    'v': {'L': 1, 'T': -1},  # Velocity
    'f': {'T': -1},  # Frequency
}

class FormulaValidationError(Exception):
    pass

def parse_dimension(expr):
    """Parse a dimension expression like 'm/s' or 'c^2' into a dimension dict."""
    expr = expr.replace('**', '^').replace(' ', '')
    terms = re.split(r'([*/])', expr)
    current_sign = 1
    result = {}

    for term in terms:
        if term == '*':
            current_sign = 1
        elif term == '/':
            current_sign = -1
        else:
            base, *exponent = re.split(r'\^', term)
            exp = int(exponent[0]) if exponent else 1
            exp *= current_sign

            if base in DIMENSION_MAP:
                dim = DIMENSION_MAP[base]
                for key, value in dim.items():
                    result[key] = result.get(key, 0) + value * exp
            # Else: ignore unknown symbols (treated as dimensionless)

    return result

def dimensions_equal(d1, d2):
    """Check if two dimension dictionaries are equal."""
    all_keys = set(d1.keys()) | set(d2.keys())
    for key in all_keys:
        if d1.get(key, 0) != d2.get(key, 0):
            return False
    return True

def validate_formula(formula: str, values: dict = None) -> dict:
    """Validate dimensional consistency and numerical correctness"""

    # Parse formula
    if '=' not in formula:
        raise FormulaValidationError('Formula must contain "="')

    left, right = formula.split('=', 1)
    left = left.strip()
    right = right.strip()

    # Initialize values if None
    if values is None:
        values = {}

    # Dimensional validation
    try:
        left_dim = parse_dimension(left)

        # Special handling for constant definitions with numerical RHS
        if left in CONSTANTS:
            try:
                constant_value = literal_eval(right)
                if isinstance(constant_value, (int, float)):
                    if values is None:
                        values = {}
                    values[left] = constant_value
                    right_dim = parse_dimension(left)
                else:
                    right_dim = parse_dimension(right)
            except:
                right_dim = parse_dimension(right)
        else:
            right_dim = parse_dimension(right)

    except Exception as e:
        raise FormulaValidationError(f'Dimensional parsing error: {str(e)}')

    if not dimensions_equal(left_dim, right_dim):
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