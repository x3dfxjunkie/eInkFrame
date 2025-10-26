# GitHub Actions Workflows

This document describes the automated testing and code quality workflows for the eInkFrame project.

## Workflow Overview

### 1. pytest-coverage.yml - Python Tests & Coverage

**Trigger:** Pull requests and pushes affecting Python files

**What it does:**
- Runs pytest test suite on Python 3.9, 3.11, and 3.13
- Generates code coverage reports
- Enforces 80% minimum code coverage
- Comments on PRs with coverage results
- Uploads coverage artifacts (HTML reports)

**Key Features:**
- ✅ Multi-version Python testing for compatibility
- ✅ Automatic PR comments with coverage metrics
- ✅ Fails PR if coverage drops below 80%
- ✅ Generates HTML coverage reports for review
- ✅ Caches pip dependencies for faster runs

**Coverage Requirements:**
- **Minimum:** 80% line coverage
- **Target:** 99%+ (current: 99% on sd_monitor.py)
- **Enforcement:** Automatic failure if below minimum

**Artifacts Generated:**
- Coverage HTML report (`htmlcov/`)
- Coverage XML file (`coverage.xml`)
- Retained for 30 days

### 2. code-quality.yml - Code Quality Checks

**Trigger:** Pull requests and pushes affecting Python files

**What it does:**
- Runs Ruff linter for code style issues
- Checks code formatting compliance
- Validates import sorting with isort
- Comments on PRs with issues found

**Linting Rules:**
- Ruff error codes: E4, E7, E9, F (via pyproject.toml)
- Line length: 120 characters
- Quote style: Double quotes
- Indent width: 4 spaces
- Target: Python 3.13

**Auto-Fix Available:**
```bash
ruff check . --fix       # Fix Ruff issues
ruff format .            # Auto-format code
isort .                  # Sort imports
```

## Paths that Trigger Workflows

### pytest-coverage.yml triggers on:
- `**.py` - Any Python file
- `requirements*.txt` - Dependency files
- `pyproject.toml` - Project configuration
- `.github/workflows/pytest-coverage.yml` - This workflow

### code-quality.yml triggers on:
- `**.py` - Any Python file
- `.github/workflows/code-quality.yml` - This workflow

## Running Tests Locally

### Before pushing changes:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest tests/ --cov=. --cov-report=term-missing

# Check coverage percentage
python -m coverage report --fail-under=80

# Run linting
ruff check .
ruff format . --check
isort . --check-only

# Auto-fix formatting issues
ruff check . --fix
ruff format .
isort .
```

## Coverage Report Viewing

After tests run, coverage reports are available:

**In GitHub Actions:**
1. Go to the PR checks
2. Click "Details" on the test job
3. Go to "Artifacts" tab
4. Download `coverage-report-py3.13`
5. Extract and open `htmlcov/index.html` in browser

**Locally:**
```bash
# Generate and view
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov\index.html  # Windows
```

## PR Workflow Expectations

When you submit a PR with Python changes:

1. **Coverage Check** - Runs pytest on 3 Python versions
2. **Code Quality** - Runs linters and formatters
3. **PR Comments** - Coverage results automatically posted
4. **Artifacts** - Coverage reports available for download

**All checks must pass before merge.**

## Configuration Files

### pyproject.toml
- Pytest configuration
- Ruff linter/formatter settings
- Python version targeting (3.13)

### requirements-dev.txt
Dependencies for development:
- pytest (8.4.2)
- pytest-cov (7.0.0)
- ruff (0.14.2)
- isort (7.0.0)

## Troubleshooting

### Coverage below 80%?
1. Check the HTML coverage report in artifacts
2. Focus on lines marked as "not covered"
3. Add tests for untested code paths

### Lint failures?
```bash
# Auto-fix most issues
ruff check . --fix
ruff format .
isort .
```

### Import ordering issues?
```bash
# Fix with isort
isort .

# Or specify a profile
isort . --profile black
```

### Tests fail on specific Python version?
- Check the test output for version-specific issues
- Consider Python version compatibility in code
- Use version guards if needed

## Best Practices

✅ **Do:**
- Run `pytest` locally before pushing
- Keep coverage above 80%
- Fix linting issues with auto-fix tools
- Write descriptive commit messages

❌ **Don't:**
- Push code without running local tests
- Ignore coverage warnings
- Disable checks without justification
- Commit code with formatting issues

## Future Enhancements

Potential additions:
- Type checking with mypy
- Security scanning with Bandit
- Dependency auditing
- Performance benchmarking
- Integration tests for GPIO/display operations (on RPi hardware)

## Support

For workflow issues:
1. Check the GitHub Actions logs
2. Review this documentation
3. Check pytest/ruff documentation
4. Open an issue with workflow logs

---

**Last Updated:** 2024
**Maintained by:** QA Engineering
