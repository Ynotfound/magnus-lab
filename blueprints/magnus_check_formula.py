"""
Formula Checker Blueprint for Magnus Platform
Validates physics formulas for mathematical correctness and dimensional consistency.
"""
import sys
from sympy import Symbol, Eq, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_equals_signs
from sympy.physics.units import (
    force, mass, acceleration, length, time, energy, velocity,
    momentum, power, pressure, charge, current, voltage
)

# Predefined symbol-to-dimension mapping for common physics quantities
SYMBOL_DIMENSIONS = {
    # Mechanics
    'F': force,       # Force
    'm': mass,        # Mass
    'a': acceleration,# Acceleration
    'v': velocity,    # Velocity
    'p': momentum,    # Momentum
    'E': energy,      # Energy
    'Pwr': power,     # Power
    't': time,        # Time
    'd': length,      # Distance
    'A': length**2,   # Area
    'V': length**3,   # Volume
    'rho': mass/length**3,  # Density
    'P': pressure,    # Pressure

    # Electromagnetism
    'q': charge,      # Charge
    'I': current,     # Current
    'V': voltage,     # Voltage
    'R': voltage/current,  # Resistance
}

def check_formula(formula_str: str) -> dict:
    """
    Validates a physics formula for mathematical correctness and dimensional consistency.

    Args:
        formula_str: Physics formula (e.g., "F = m * a")

    Returns:
        dict: {
            "is_valid": bool,
            "error": str | None
        }
    """
    try:
        # Parse the formula with implicit multiplication support
        transformations = standard_transformations + (implicit_multiplication_application, convert_equals_signs)
        expr = parse_expr(formula_str, transformations=transformations, evaluate=False)

        # Must be an equation
        if not isinstance(expr, Eq):
            return {
                "is_valid": False,
                "error": "Formula must be an equation (contain '=')"
            }

        lhs = expr.lhs
        rhs = expr.rhs

        # Check mathematical validity by simplifying
        try:
            simplify(lhs - rhs)
        except Exception as e:
            return {
                "is_valid": False,
                "error": f"Mathematical error: {str(e)}"
            }

        # Dimensional analysis
        lhs_dims = lhs
        rhs_dims = rhs

        # Replace symbols with their dimensions
        for symbol, dimension in SYMBOL_DIMENSIONS.items():
            sym = Symbol(symbol)
            lhs_dims = lhs_dims.subs(sym, dimension)
            rhs_dims = rhs_dims.subs(sym, dimension)

        # Simplify dimensions
        lhs_dims = lhs_dims.simplify()
        rhs_dims = rhs_dims.simplify()

        # Check dimensional equality
        if lhs_dims != rhs_dims:
            return {
                "is_valid": False,
                "error": f"Dimensional mismatch: {lhs_dims} vs {rhs_dims}"
            }

        return {"is_valid": True, "error": None}

    except Exception as e:
        return {
            "is_valid": False,
            "error": f"Parsing error: {str(e)}"
        }

def formula_check_task(formula: str) -> dict:
    """
    Magnus task entry point for formula validation.

    Args:
        formula: Physics formula to validate

    Returns:
        Validation result
    """
    return check_formula(formula)

if __name__ == "__main__":
    # Validate command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python formula_check_blueprint.py 'formula_string'")
        print("Example: python formula_check_blueprint.py 'F = m * a'")
        sys.exit(1)

    formula = sys.argv[1]

    # Submit job to Magnus platform
    try:
        from magnus import submit_job
        job_id = submit_job(
            task_name="formula_check",
            entry_command=f"pip install sympy && python blueprints/magnus_check_formula.py '{formula}'",
            container_image="docker://python:3.11-slim",
            job_type="N/A",
            branch="main",
            namespace="Ynotfound",
            repo_name="magnus-lab"
        )
        print(f"Submitted job with ID: {job_id}")
    except ImportError:
        # Fallback for local testing
        print(f"Running locally (Magnus not available): validating '{formula}'")
        result = check_formula(formula)
        print(result)
        sys.exit(0 if result["is_valid"] else 1)