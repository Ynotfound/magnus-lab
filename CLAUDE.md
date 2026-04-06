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

## Project-Specific Best Practices
- **Encoding Requirement** (Critical for Windows):
  ```yaml
  environment:
    PYTHONUTF8: "1"
    PYTHONIOENCODING: "utf-8"
  ```
- **Deployment Workflow**:
  Always `git push` BEFORE submitting jobs - cluster uses remote code, not local files
- **Execution Context Separation**:
  Use LOCAL IMPORTS for Magnus client (`from magnus import...` inside blueprint function) to prevent container recursion
- **Directory Structure**:
  - `blueprints/`: Contains job submission blueprints
  - `scripts/`: Contains executable logic decoupled from Magnus infrastructure

- **get_loss_trend Skill**:
  V2.1 版本已通过混沌测试，强制开启 errors=replace 编码保护，具备生产级异常捕获逻辑。

- **Parameter Specification**:
  Use STRING values for job parameters (e.g., `job_type="B2"` not enum types)

**Last Verified**: 2026-04-03