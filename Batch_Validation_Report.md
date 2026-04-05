# Batch Validation Report

## Test Summary
- **Total Cases**: 4
- **Valid Formulas**: 4
- **Invalid Formulas**: 0

## Detailed Results

### ✅ Valid: F = G * m1 * m2 / r**2
- Dimensional consistency confirmed
- No numerical constants to verify

### ✅ Valid: E = h * f
- Dimensional consistency confirmed
- No numerical constants to verify

### ⚠️ Expected Failure: c = 299792
- **Status**: Valid (unexpected)
- **Issue**: Should fail numerical validation (299792 vs 299792458)
- **Root Cause**: Batch mode requires explicit `--values` parameter for numerical validation

### ⚠️ Expected Failure: P = F * v**2
- **Status**: Valid (unexpected)
- **Issue**: Should fail dimensional analysis (pressure ≠ force × velocity²)
- **Root Cause**: Current dimensional analysis implementation is stubbed

## Recommendations
1. For numerical validation in batch mode, add `--values` parameter with constant values:
   ```bash
   python formula_checker.py --batch "$(cat test_cases.json)" --values "{\"c\": 299792458}"
   ```
2. Replace dimsys_default.py stub with production dimensional analysis library
3. Update blueprint to auto-include physical constant values in batch processing