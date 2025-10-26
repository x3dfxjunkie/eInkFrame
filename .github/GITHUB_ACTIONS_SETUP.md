# GitHub Actions CI/CD Setup Guide

## Overview

This project uses GitHub Actions for automated testing and code quality checks. Two main workflows have been configured:

1. **pytest-coverage.yml** - Test execution and coverage validation (80% minimum)
2. **code-quality.yml** - Linting and code formatting checks

## Quick Start

### For Developers

No setup required! Just push to a PR or push to `main`/`develop` branches with Python file changes.

**What happens automatically:**
1. Tests run on Python 3.9, 3.11, and 3.13
2. Coverage is calculated and checked against 80% threshold
3. Code is linted with Ruff
4. Formatting is validated
5. PR gets automatic comments with results

### For Project Maintainers

**CI Status:**
- Check PRs for automated test results
- Coverage reports available in Actions artifacts
- Merge only when all checks pass (branch protection recommended)

## Workflow Details

### 1. pytest-coverage.yml

**File:** `.github/workflows/pytest-coverage.yml`

**Triggers:**
- Pull requests with Python file changes
- Pushes to `main` or `develop` with Python file changes

**What it does:**

```
1. Checkout code
   ↓
2. Set up Python (3.9, 3.11, 3.13)
   ↓
3. Install dev dependencies
   ↓
4. Run pytest with coverage reporting
   ↓
5. Check coverage >= 80%
   ↓
6. Comment on PR with results
   ↓
7. Upload HTML coverage report
   ↓
8. Fail if below threshold
```

**Key Configuration:**
- **Coverage threshold:** 80% (enforced)
- **Tested Python versions:** 3.9, 3.11, 3.13
- **Test location:** `tests/` directory
- **Timeout:** 10 minutes

**Coverage Reports Generated:**
- Terminal summary (in logs)
- XML format (`coverage.xml` - machine readable)
- HTML format (`htmlcov/` - human readable)
- Artifact retention: 30 days

**Example PR Comment:**
```
## Test Results

- **Coverage:** 99%
- **Threshold:** 80%
- **Status:** ✅ All checks passed
```

### 2. code-quality.yml

**File:** `.github/workflows/code-quality.yml`

**Triggers:**
- Pull requests with Python file changes
- Pushes to `main` or `develop` with Python file changes

**What it does:**

```
1. Checkout code
   ↓
2. Set up Python 3.13
   ↓
3. Install linting tools (ruff, isort)
   ↓
4. Run Ruff linter
   ↓
5. Run Ruff formatter check
   ↓
6. Run isort import checker
   ↓
7. Comment on PR if issues found
```

**Linting Rules (from pyproject.toml):**
- Error codes: E4, E7, E9, F (Pyflakes and pycodestyle basics)
- Line length: 120 characters
- Quote style: Double quotes
- Indent: 4 spaces
- Python target: 3.13

**Continues on error:** Issues are reported but don't block merge

## Coverage Threshold: 80%

### Why 80%?

- **High enough** to catch untested code
- **Realistic** for production code
- **Achievable** without excessive test bloat
- **Your project** currently at 99% ✨

### Current Status

**sd_monitor.py:** 99% coverage
- 81 statements
- 1 missed line (if __name__ == "__main__")
- 82 passing tests

### Viewing Coverage Reports

**In GitHub:**
1. Go to completed workflow run
2. Click "Artifacts" section
3. Download `coverage-report-py3.13`
4. Extract and open `htmlcov/index.html`

**Locally:**
```bash
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html  # macOS
```

## Local Development Workflow

### Before committing:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest tests/ --cov=. --cov-report=term-missing

# Check coverage
python -m coverage report --fail-under=80
```

### If coverage is below 80%:

```bash
# Find uncovered lines
python -m coverage report --skip-covered
python -m coverage html  # Generate HTML report
open htmlcov/index.html  # View in browser

# Add tests for uncovered code
# Then re-run pytest
```

### Code quality checks:

```bash
# Run linting
ruff check .

# Check formatting
ruff format . --check

# Check imports
isort . --check-only

# Auto-fix everything
ruff check . --fix
ruff format .
isort .
```

## Branch Protection Rules (Recommended)

For maximum CI/CD benefit, configure GitHub branch protection:

**Settings → Branches → Branch protection rule → main**

Enable:
- ✅ Require status checks to pass before merging
  - Select `test` from pytest-coverage workflow
  - Select `lint` from code-quality workflow
- ✅ Require branches to be up to date before merging
- ✅ Dismiss stale pull request approvals when new commits are pushed

This ensures:
- All tests pass before merge
- Coverage doesn't drop
- Code meets quality standards
- No outdated PRs merged

## Artifact Management

**Auto-cleanup:** 30 days retention

If you need longer retention:
1. Go to workflow file
2. Change `retention-days: 30` to desired value

**Storage considerations:**
- HTML reports: ~1-2 MB each
- With 3 Python versions: ~3-6 MB per run
- 30 days = ~180 MB maximum

## Debugging Workflow Failures

### If tests fail:

1. **Check workflow logs:**
   - PR → Checks → Click workflow name
   - View test output in "Run pytest" step

2. **Key failure indicators:**
   - `FAILED test_name` - Test assertion failed
   - `ERROR collecting` - Syntax error in code
   - `ImportError` - Missing dependency

3. **Run locally to replicate:**
   ```bash
   pytest tests/ -v --tb=short
   ```

### If coverage is below 80%:

1. **View HTML report** (from artifacts)
2. **Find red lines** (uncovered code)
3. **Add tests** for those lines
4. **Re-run locally:**
   ```bash
   pytest tests/ --cov=. --cov-report=term-missing
   ```

### If linting fails:

1. **Check code-quality logs**
2. **Run auto-fix locally:**
   ```bash
   ruff check . --fix
   ruff format .
   isort .
   ```
3. **Commit and push**

## Environment Details

### Python Versions Tested

- **3.9** - Older, wider compatibility
- **3.11** - Current stable
- **3.13** - Latest (recommended)

Set `target-version` in pyproject.toml to match your requirements.

### Dependencies (from requirements-dev.txt)

- **pytest** - Test runner
- **pytest-cov** - Coverage plugin
- **ruff** - Fast Python linter
- **isort** - Import formatter

## Integration with IDEs

### VS Code

Install extensions:
- Python
- Pylance
- Ruff

Add to `.vscode/settings.json`:
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit"
    }
  },
  "ruff.line-length": 120
}
```

### PyCharm

- Settings → Tools → Python Integrated Tools → Package requirements file: `requirements-dev.txt`
- Enable Ruff inspections
- Settings → Languages & Frameworks → Python → Ruff

## CI/CD Metrics

### Current Performance

| Metric | Value |
|--------|-------|
| Total Tests | 82 |
| Passing | 100% |
| Coverage | 99% |
| Threshold | 80% |
| Execution Time | ~0.1s |
| Python Versions | 3 |

### Historical Tracking

Monitor these over time:
- Test count (growing?)
- Coverage percentage (improving?)
- Execution time (degrading?)
- Failure rate (stable?)

## Troubleshooting Guide

### Problem: "Coverage below 80%"

**Solution:**
```bash
# See what's uncovered
pytest tests/ --cov=. --cov-report=term-missing

# Generate HTML report
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

### Problem: "tests not found"

**Solution:**
- Ensure `pyproject.toml` has: `pythonpath = ["."]*
- Ensure test files are in `tests/` directory
- Ensure test files are named `test_*.py`

### Problem: "ImportError in workflow"

**Solution:**
```bash
# Verify dependencies
pip install -r requirements-dev.txt

# Try locally
pytest tests/ -v
```

### Problem: "Linting passes locally but fails in CI"

**Solution:**
- Ruff versions may differ
- Force same version:
  ```bash
  pip install ruff==0.14.2  # Update to version in requirements-dev.txt
  ruff check .
  ```

### Problem: "Artifact not available"

**Solution:**
- Check retention days (default 30)
- Workflow must complete successfully to upload
- Check "Upload coverage artifacts" step in logs

## Advanced Configuration

### Running specific Python versions only:

Edit `pytest-coverage.yml`:
```yaml
matrix:
  python-version: ['3.13']  # Just Python 3.13
```

### Excluding directories from coverage:

Edit `.github/workflows/pytest-coverage.yml`:
```bash
pytest tests/ \
  --cov=. \
  --cov-report=term-missing \
  --cov-config=.coveragerc  # Use config file
```

Create `.coveragerc`:
```ini
[run]
omit =
    */tests/*
    */venv/*
```

### Sending coverage to Codecov:

Add step to pytest-coverage.yml:
```yaml
- name: Upload to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
    fail_ci_if_error: true
```

## Support & Resources

### GitHub Actions Docs
- https://docs.github.com/en/actions
- https://docs.github.com/en/actions/using-workflows

### Tool Documentation
- pytest: https://docs.pytest.org
- pytest-cov: https://pytest-cov.readthedocs.io
- Ruff: https://docs.astral.sh/ruff
- isort: https://pycqa.github.io/isort

### Coverage.py
- https://coverage.readthedocs.io

## Summary

✅ **What's automated:**
- Test execution (3 Python versions)
- Coverage validation (80% minimum)
- Code linting
- Import sorting
- PR commenting with results
- Artifact storage

✅ **What's enforced:**
- 80% minimum code coverage
- Code quality standards
- Consistent formatting

🎯 **Next steps:**
1. Push a PR with Python changes
2. Watch the workflows run
3. Review coverage reports in artifacts
4. Merge when all checks pass

---

**Workflow Status:** ✅ Configured and Ready
**Last Updated:** 2024-10-26
**Maintained by:** QA Engineering
