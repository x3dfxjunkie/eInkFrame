# CI/CD Quick Reference

## Before Pushing Your Code

```bash
# 1. Install dev dependencies (first time)
pip install -r requirements-dev.txt

# 2. Run tests locally
pytest tests/ --cov=. --cov-report=term-missing

# 3. Check coverage meets 80% minimum
python -m coverage report --fail-under=80

# 4. Fix any formatting issues
ruff check . --fix
ruff format .
isort .

# 5. Verify all checks pass
ruff check .
pytest tests/ --cov=. --cov-report=term-missing
```

## What Happens When You Push

### On Pull Request:

```
✓ Python 3.11 - Run tests and check coverage
✓ Python 3.12 - Run tests and check coverage
✓ Python 3.13 - Run tests and check coverage
✓ Python 3.14 - Run tests and check coverage
✓ Code Linting - Check code quality
✓ Code Formatting - Check formatting compliance
✓ PR Comment - Post coverage results
```

**All must pass before merging.**

### What Gets Checked

| Check | Tool | Threshold | Action |
|-------|------|-----------|--------|
| Tests Pass | pytest | 100% | Required |
| Code Coverage | pytest-cov | ≥80% | Required |
| Linting | ruff | 0 errors | Continue on error |
| Formatting | ruff format | 0 diffs | Continue on error |
| Imports | isort | 0 issues | Continue on error |

## Common Commands

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_sd_monitor.py -v

# Run specific test function
pytest tests/test_sd_monitor.py::TestGetRefreshTime::test_get_refresh_time_valid_value -v

# Run with more details
pytest tests/ -vv --tb=short
```

### Coverage

```bash
# Show coverage report in terminal
python -m coverage report

# Show coverage with missing lines
python -m coverage report --skip-covered

# Generate HTML report
python -m coverage html
open htmlcov/index.html  # macOS

# Fail if below 80%
python -m coverage report --fail-under=80
```

### Code Quality

```bash
# Check with ruff
ruff check .

# Auto-fix with ruff
ruff check . --fix

# Format code
ruff format .

# Check formatting
ruff format . --check

# Check imports with isort
isort . --check-only

# Fix import order
isort .
```

## When Tests Fail

### Coverage below 80%:

1. Generate HTML report:
   ```bash
   pytest tests/ --cov=. --cov-report=html
   open htmlcov/index.html
   ```

2. Find red lines (uncovered code)
3. Add tests for those lines
4. Re-run: `pytest tests/ --cov=. --cov-report=term-missing`

### Tests failing:

```bash
# Run with more details
pytest tests/ -vv --tb=long

# Run just failed tests
pytest --lf

# Run with print statements visible
pytest -s

# Run specific test
pytest tests/test_file.py::TestClass::test_method -v
```

### Linting/Formatting issues:

```bash
# Auto-fix everything
ruff check . --fix
ruff format .
isort .

# Review changes
git diff

# Commit and push
git add .
git commit -m "chore: fix formatting and linting"
git push
```

## PR Workflow

1. **Create PR** - from feature branch to main
2. **Wait for checks** - workflows run automatically
3. **Review results** - in PR checks section
4. **Fix issues** - if any checks fail
5. **Get approval** - from code reviewer
6. **Merge** - when all checks pass

## Viewing Coverage in GitHub

1. Go to your PR
2. Click "Checks" tab
3. Click "Python Tests & Coverage"
4. Scroll to "Artifacts" section
5. Download `coverage-report-py3.13`
6. Extract and open `htmlcov/index.html`

## Quick Troubleshooting

| Problem | Command | Solution |
|---------|---------|----------|
| Imports wrong order | `isort . --check-only` | `isort .` |
| Code formatting | `ruff format . --check` | `ruff format .` |
| Linting errors | `ruff check .` | `ruff check . --fix` |
| Coverage below 80% | `python -m coverage report` | Add tests |
| Test failures | `pytest -vv --tb=long` | Fix code/test |
| All at once | See "Before Pushing" above | Run the script |

## Environment Variables

Not needed for basic usage. These are set automatically in CI:

- `GITHUB_ACTIONS=true` - Set by GitHub
- `CI=true` - Common CI flag
- `PYTHONDONTWRITEBYTECODE=1` - Prevent `.pyc` files (in CI)

## Python Versions

### Currently tested:
- ✅ Python 3.11
- ✅ Python 3.12
- ✅ Python 3.13 (recommended)
- ✅ Python 3.14

### Add/remove versions:

Edit `.github/workflows/pytest-coverage.yml`:
```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13', '3.14']
```

## Coverage Targets

### Current Status:
- **Actual:** 99% (sd_monitor.py)
- **Required:** 80%
- **Gap:** Safe, well above threshold

### History:
Track coverage trends over time. Aim for consistency or improvement.

## Project Standards

✅ **Must have:**
- ≥80% code coverage
- All tests passing
- Clean linting
- Proper formatting

✅ **Should have:**
- ≥90% code coverage
- Well-organized tests
- Comprehensive docstrings
- Type hints

✅ **Nice to have:**
- ≥95% code coverage
- Integration tests
- Performance benchmarks
- Security scanning

## Getting Help

### Check the docs:
1. `.github/GITHUB_ACTIONS_SETUP.md` - Full setup guide
2. `.github/WORKFLOWS.md` - Workflow details
3. This file - Quick reference

### Run locally:
```bash
# Same as CI does
pytest tests/ --cov=. --cov-report=term-missing
ruff check .
ruff format . --check
isort . --check-only
```

### Check workflow logs:
1. Go to PR
2. Click "Checks"
3. Click workflow name
4. View detailed logs

### Common questions:

**Q: Do I need to install anything?**
A: Yes, first time: `pip install -r requirements-dev.txt`

**Q: Will the workflow auto-fix issues?**
A: No, but `ruff check . --fix` and `ruff format .` will locally.

**Q: What if coverage drops?**
A: Workflow fails. Add tests for uncovered code.

**Q: Can I merge without passing checks?**
A: No (if branch protection is enabled). Fix issues first.

**Q: How long do tests take?**
A: ~10 seconds total (3 Python versions × ~3 seconds each)

---

**Last Updated:** 2025-10-26
**For full documentation:** See `.github/GITHUB_ACTIONS_SETUP.md`
