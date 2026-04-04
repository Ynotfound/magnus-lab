# Week 1 Progress Report: magnus_check_formula Implementation

## Troubleshooting Journey Summary

### 1. Initial Symbol Conflict (Physics Dimension Mapping)
- **Issue**: Symbol `'P'` used for both power and pressure in `SYMBOL_DIMENSIONS`
- **Error**: Silent override causing incorrect dimensional analysis
- **Resolution**: 
  - Renamed power to `'Pwr'`
  - Added explicit documentation for symbol mappings
  - Verified against physics standards (NIST, SI units)
- **Significance**: Critical for detecting formula hallucinations (section 3.4 of Action Plan)

### 2. Dependency Management (Windows Environment)
- **Issue**: `ModuleNotFoundError: No module named 'sympy'`
- **Root Cause**: Missing physics validation library in Windows Python environment
- **Resolution**:
  - Installed `sympy==1.14.0` with `pip install sympy`
  - Validated compatibility with Windows Python 3.10
- **Prevention**: Added to `requirements.txt` per CLAUDE.md Windows setup guidelines

### 3. Magnus API Integration Challenges
- **Issue 1**: `TypeError: submit_job() got unexpected keyword argument 'task'`
  - **Debugging**: Referenced CLAUDE.md branch mapping requirements
  - **Resolution**: Removed positional arguments, switched to keyword parameters

- **Issue 2**: `job_type="blueprint"` validation failure
  - **Error**: `Input should be 'A1', 'A2', 'B1', 'B2' or 'N/A'`
  - **Root Cause**: Misinterpreted job_type enum in Magnus API docs
  - **Resolution**: Set `job_type="N/A"` for blueprint workflows

- **Issue 3**: Windows path handling in container commands
  - **Debugging**: Verified `core.autocrlf=input` setting from CLAUDE.md
  - **Resolution**: Used forward slashes in entry_command (`blueprints/...`)

### 4. SSH & Environment Setup (Proactive Prevention)
- **Actions Taken**:
  - Configured SSH key per CLAUDE.md (ed25519, GitHub integration)
  - Set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` in `magnus_config.yaml`
  - Verified `core.autocrlf=input` globally to prevent CRLF issues
- **Outcome**: No SSH/auth failures or encoding errors during testing

### 5. Final Validation Success
- **Test Case 1**: `F = m * a`
  ```json
  {"is_valid": true, "error": null}
  ```
  
- **Test Case 2**: `E = m * c`
  ```json
  {"is_valid": false, "error": "Dimensional mismatch: energy vs mass*velocity"}
  ```
  - **Significance**: Correctly identified missing `c²` term (section 3.4 formula hallucination)

## Key Achievements
✅ Implemented full L0.5 hallucination detection workflow
✅ Validated against physics standards with dimensional analysis
✅ Resolved Windows-specific environment challenges
✅ Established CI/CD-ready blueprint structure
✅ Generated actionable error messages for hallucination diagnosis

## Week 2 Next Steps (Per Action Plan v2.0)

### Priority Tasks
1. **Bulk Data Filtering Pipeline**
   - Implement `magnus_step_verify()` for multi-step CoT validation
   - Build regex-based formula extractor from raw CoT outputs
   - Integrate Wolfram Alpha API for intermediate step verification

2. **Knowledge Distillation Integration**
   ```python
   # Pseudocode for Week 2 integration
   def filter_distillation_data(raw_cots):
       valid_cots = []
       for cot in raw_cots:
           if magnus_check_formula(cot['formula']).is_valid:
               if magnus_verify_constants(cot['constants']).is_valid:
                   valid_cots.append(cot)
       return valid_cots
   ```

3. **Physical Constant Validation**
   - Develop `magnus_verify_constants()` using NIST CODATA 2025
   - Implement tolerance thresholds for measurement uncertainty
   - Create error catalog for common constant hallucinations (section 3.4)

4. **Quantitative Metrics**
   | Metric | Target | Measurement |
   |--------|--------|-------------|
   | Formula validation rate | ≥95% | Pre/post-filter comparison |
   | False positive rate | ≤5% | Expert-reviewed sample |
   | Processing speed | 500 formulas/sec | Benchmark test |

### Risk Mitigation
- **Risk**: Overly strict filtering reduces dataset size
  **Action**: Implement confidence scoring (section 3.5 memory compression loss)
- **Risk**: API rate limits for Wolfram verification
  **Action**: Build local fallback validator for common formulas

### Deliverables Timeline
| Date | Deliverable |
|------|-------------|
| Apr 7 | `magnus_check_formula` integration test suite |
| Apr 9 | Constant validation prototype |
| Apr 11 | Bulk CoT filtering pipeline |
| Apr 12 | Week 2 progress report & credit documentation |

---
*Report generated automatically on 2026-04-04 per Action Plan v2.0 §6 (Week 1-3 Plan)*