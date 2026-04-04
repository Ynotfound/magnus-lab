import sys
from sympy import Symbol, Eq, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_equals_signs
from sympy.physics.units import *
from sympy.physics.units.systems.si import dimsys_default

# 定义符号量纲映射
SYMBOL_DIMENSIONS = {
    'F': force, 'm': mass, 'a': acceleration, 'v': velocity,
    'E': energy, 'c': velocity, 't': time, 'd': length
}

def check_formula(formula_str):
    try:
        transformations = standard_transformations + (implicit_multiplication_application, convert_equals_signs)
        expr = parse_expr(formula_str, transformations=transformations, evaluate=False)

        if isinstance(expr, Eq):
            lhs_deps = dimsys_default.get_dimensional_dependencies(expr.lhs.subs(SYMBOL_DIMENSIONS))
            rhs_deps = dimsys_default.get_dimensional_dependencies(expr.rhs.subs(SYMBOL_DIMENSIONS))
            is_valid = lhs_deps == rhs_deps
            return {"is_valid": is_valid, "error": None if is_valid else f"Mismatch: {lhs_deps} vs {rhs_deps}"}
        return {"is_valid": False, "error": "Not an equation"}
    except Exception as e:
        return {"is_valid": False, "error": str(e)}

def blueprint(formula="F = m * a"):
    from magnus import submit_job, JobType
    res = submit_job(
        task_name="formula_check_v2",
        entry_command=f"pip install sympy && python blueprints/magnus_check_formula.py '{formula}'",
        container_image="docker://python:3.11-slim",
        repo_name="magnus-lab",
        branch="main",
        job_type="B2"
    )
    print(f"SUCCESS: Job ID {res}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(check_formula(sys.argv[1]))
    else:
        blueprint()