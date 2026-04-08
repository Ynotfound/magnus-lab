---
name: get_loss_trend
version: 2.1.92
repository: Agentification-of-AI-Infra
namespace: Rise-AGI
description: >-
  Production-grade loss trend analyzer with chaos-tested error handling. 
  Validates job logs, generates convergence metrics, and detects training anomalies.
---

<tool_specification>

## Core Functionality
Analyzes training job logs to visualize loss trends across training iterations. Integrates with Magnus monitoring pipeline for real-time convergence analysis.

## Setup Requirements
```bash
magnus config  # Verify connection to Rise-AGI platform
```

<parameter_schema>

| Parameter | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `target_job_id` | `str` | **🚫 16-character absolute ID**<br/>Format: `[a-f0-9]{16}`<br/>**NEVER USE RELATIVE INDICES** | Absolute job ID of training job (e.g., `a1b2c3d4e5f67890`). Must be captured from `magnus run` output. |
| `priority` | `A1`/`A2`/`B1`/`B2` | Default: `B2` | Execution priority level:
- `A1`: Highest priority (non-preemptible)
- `A2`: High priority (non-preemptible)
- `B1`: Low priority (preemptible)
- `B2`: Lowest priority (preemptible) |

<error_policy>

### Critical Execution Policy

**Absolute ID Enforcement**
```diff
- magnus run get_loss_trend --target_job_id -1
+ JOB_ID=$(magnus run training-job ... | awk '/job_id:/ {print $2}')
+ magnus run get_loss_trend --target_job_id $JOB_ID
```

**Connection Interruption Protocol**
1. `magnus status <ABSOLUTE_JOB_ID>` — **MANDATORY CHECK**
2. If `RUNNING`:
   ```bash
   magnus job result <ID>  # Retrieve structured output
   magnus receive          # Download artifacts
   ```
3. Only `magnus kill <ID>` + resubmit if `FAILED`

**🚫 NEVER RESUBMIT WITHOUT VERIFICATION** — jobs continue executing server-side after client disconnect.

<production_requirements>

- **Git Synchronization**: Code modifications **MUST** be pushed before submission (`git push`)
- Magnus SDK ≥ 0.6.0 (verified via `magnus --version`)
- Input job **MUST** complete successfully
- Log format must contain structured loss metrics (`step`, `train_loss`, `val_loss`)
- Windows systems require PYTHONUTF8=1 in environment

<verification>

### Chaos Test Report (V2.1.92)
| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Log Truncation | 50% incomplete logs | Graceful partial analysis | ✅ PASSED |
| Encoding Failures | UTF-8 invalid sequences | `errors=replace` applied | ✅ PASSED |
| Job Termination | SIGKILL during execution | Resource cleanup verified | ✅ PASSED |
| Priority Override | A1 requested on B-tier quota | Rejection with quota error | ✅ PASSED |
| 16h Execution | Long-running job | Proper timeout handling | ✅ PASSED |

<deployment_notes>

**Code Deployment Protocol**
1. Commit changes with: `git commit -m "Update get_loss_trend skill"`
2. **MANDATORY**: `git push origin main`
3. Verify remote code with: `magnus job logs <ID> --code`

**Last Verified**: 2026-04-08
**Verified By**: Anthropic Infrastructure Team