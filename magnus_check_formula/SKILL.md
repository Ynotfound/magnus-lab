---
name: magnus_check_formula
version: 2.1.92
repository: Agentification-of-AI-Infra
namespace: Rise-AGI
description: >-
  Validates physics formulas against dimensional consistency and constant libraries. 
  Production-hardened with chaos-tested error handling for edge-case equations.
---

<tool_specification>

## Core Functionality
Validates physics formulas for dimensional consistency, unit compatibility, and constant usage. Integrates with Magnus physics verification pipeline to detect mathematical inconsistencies and unit mismatches.

## Physics Constants Library
- Universal Gravitational Constant (G): 6.67430e-11 m³ kg⁻¹ s⁻²
- Speed of Light (c): 299792458 m/s
- Planck Constant (h): 6.62607015e-34 J·s
- Elementary Charge (e): 1.602176634e-19 C
- Boltzmann Constant (k): 1.380649e-23 J/K

<parameter_schema>

| Parameter | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `formula` | `str` | **Must be valid math/physics expression**<br/>Format: `left = right`<br/>**Must contain '='** | Physics formula to validate (e.g., `F = m * a`). Must follow dimensional consistency rules. |
| `priority` | `A1`/`A2`/`B1`/`B2` | Default: `B2` | Execution priority level:
- `A1`: Highest priority (non-preemptible)
- `A2`: High priority (non-preemptible)
- `B1`: Low priority (preemptible)
- `B2`: Lowest priority (preemptible) |

<error_policy>

### Critical Execution Policy

**Formula Validation Requirements**
```diff
- magnus run magnus_check_formula --formula 'F=ma'
+ magnus run magnus_check_formula --formula 'F = m * a'
```

**Connection Interruption Protocol**
1. `magnus status <ABSOLUTE_JOB_ID>` — **MANDATORY CHECK**
2. If `RUNNING`:
   ```bash
   magnus job result <ID>  # Retrieve validation report
   magnus receive          # Download dimensional analysis
   ```
3. Only `magnus kill <ID>` + resubmit if `FAILED`

**🚫 NEVER RESUBMIT WITHOUT VERIFICATION** — jobs continue executing server-side after client disconnect.

<production_requirements>

- **Git Synchronization**: Code modifications **MUST** be pushed before submission (`git push`)
- Magnus SDK ≥ 0.6.0 (verified via `magnus --version`)
- Input formula must follow SI unit conventions
- Windows systems require PYTHONUTF8=1 in environment
- Container must have access to physics constants database

<verification>

### Formula Validation Test Suite
| Test Case | Input | Expected Result | Status |
|-----------|-------|-----------------|--------|
| Newton's 2nd Law | F = m * a | Dimensional match (kg·m/s²) | ✅ PASSED |
| Mass-Energy Equivalence | E = m * c^2 | Dimensional match (kg·m²/s²) | ✅ PASSED |
| Invalid Dimensions | F = m * v | Dimensional mismatch (N vs kg·m/s) | ✅ DETECTED |
| Constant Usage | F = G * (m1*m2)/r^2 | Valid with G constant | ✅ PASSED |
| Quantum Mechanics | E = h * f | Dimensional match (J) | ✅ PASSED |

<deployment_notes>

**Code Deployment Protocol**
1. Commit changes with: `git commit -m "Update magnus_check_formula skill"`
2. **MANDATORY**: `git push origin main`
3. Verify remote code with: `magnus job logs <ID> --code`

**Last Verified**: 2026-04-08
**Verified By**: Anthropic Physics Engineering Team