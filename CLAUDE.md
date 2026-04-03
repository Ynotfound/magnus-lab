# Magnus Production Environment Configuration Guide

## Windows Environment Setup
- **Critical Environment Variables** (add to `magnus_config.yaml`):
  ```yaml
  environment:
    PYTHONUTF8: "1"
    PYTHONIOENCODING: "utf-8"
  ```
- **Git Line Ending Configuration** (prevents CRLF/LF conflicts):
  ```bash
  git config --global core.autocrlf input
  ```

## SSH Key Configuration
1. **Generate SSH Key** (if missing):
   ```bash
   ssh-keygen -t ed25519 -C "claude@claude.ai" -N "" -f ~/.ssh/id_ed25519
   ```
2. **Add to GitHub**:
   - Copy public key: `cat ~/.ssh/id_ed25519.pub`
   - Paste in GitHub → Settings → SSH and GPG keys
3. **Configure Repository**:
   ```bash
   git remote set-url origin git@github.com:Ynotfound/magnus-lab.git
   ```

## Magnus Blueprint Requirements
- **Required Parameters** (use `branch` NOT `default_branch`):
  ```python
  submit_job(
      branch="main",  # Must match remote branch name
      namespace="Ynotfound",
      repo_name="magnus-lab",
      # ... other parameters
  )
  ```
- **Direct Execution** (bypass `magnus run`):
  ```bash
  python blueprints/your_script.py
  ```

## Git Branch Mapping
- **Local to Remote Branch Setup**:
  ```bash
  git push -u origin master:main  # Maps local master → remote main
  ```
- **Recover from Branch Mismatch**:
  ```bash
  git pull origin main --allow-unrelated-histories
  ```

## Common Errors & Fixes
| Error | Solution |
|-------|----------|
| `Remote branch master not found` | Change `branch="master"` → `branch="main"` |
| `Permission denied (publickey)` | Verify SSH key added to GitHub and correct remote URL |
| `Failed to determine default branch` | Use `branch` parameter instead of `default_branch` |
| `LF will be replaced by CRLF` | Set `core.autocrlf input` globally |

**Last Verified**: 2026-04-03