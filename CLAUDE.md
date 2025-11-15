# CLAUDE.md - AI Assistant Guide for Claude_Code Repository

> **Last Updated:** 2025-11-15
> **Repository:** vitoiitmBSc/Claude_Code
> **Primary Language:** Python

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Codebase Structure](#codebase-structure)
3. [Development Workflows](#development-workflows)
4. [Git Conventions](#git-conventions)
5. [Code Conventions](#code-conventions)
6. [Testing Guidelines](#testing-guidelines)
7. [AI Assistant Guidelines](#ai-assistant-guidelines)
8. [Future Development](#future-development)

---

## Repository Overview

### Current State

This is a **minimal Python repository** currently in its early stages of development. The repository contains:

- **Language:** Python 3.11.14
- **Total Files:** 1 Python script
- **Dependencies:** None
- **Build System:** None configured
- **Testing Framework:** None configured
- **Documentation:** This CLAUDE.md file

### Purpose

The repository appears to be a demonstration or starter project, currently containing a simple Python script.

### Project Statistics

- **Lines of Code:** ~1
- **Commits:** 1
- **Branches:** 1 (Claude working branch)
- **Contributors:** Claude AI Assistant

---

## Codebase Structure

### Directory Layout

```
Claude_Code/
├── .git/                 # Git repository metadata
├── hello_ganesh.py       # Main Python script
└── CLAUDE.md            # This file - AI assistant documentation
```

### File Descriptions

#### `hello_ganesh.py`

- **Location:** `/home/user/Claude_Code/hello_ganesh.py`
- **Purpose:** Simple demonstration script
- **Functionality:** Prints "hello ganesh" to console
- **Lines:** 1

### Future Structure Recommendations

As the project grows, consider organizing it as follows:

```
Claude_Code/
├── .git/
├── .gitignore           # Git ignore patterns
├── README.md            # Project documentation
├── CLAUDE.md            # This file
├── requirements.txt     # Python dependencies
├── setup.py             # Package configuration (if building a package)
├── pyproject.toml       # Modern Python project config
├── src/                 # Source code directory
│   └── __init__.py
├── tests/               # Test files
│   └── test_*.py
├── docs/                # Additional documentation
├── scripts/             # Utility scripts
└── .github/             # GitHub workflows and templates
    └── workflows/
        └── ci.yml       # Continuous integration
```

---

## Development Workflows

### Setting Up Development Environment

#### 1. Clone the Repository

```bash
git clone http://local_proxy@127.0.0.1:47198/git/vitoiitmBSc/Claude_Code
cd Claude_Code
```

#### 2. Python Environment Setup (Recommended for Future)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt
```

#### 3. Running the Current Script

```bash
python hello_ganesh.py
```

**Expected Output:** `hello ganesh`

### Development Cycle

1. **Create/Switch to Feature Branch**
   - AI assistants should work on branches prefixed with `claude/`
   - Format: `claude/claude-md-{identifier}-{session-id}`

2. **Make Changes**
   - Follow code conventions (see below)
   - Add tests for new functionality
   - Update documentation

3. **Test Changes**
   - Run existing tests
   - Verify functionality manually

4. **Commit and Push**
   - Write clear, descriptive commit messages
   - Push to the feature branch

5. **Create Pull Request**
   - Document changes clearly
   - Link to relevant issues

---

## Git Conventions

### Branch Naming

- **Claude AI Branches:** `claude/claude-md-{identifier}-{session-id}`
- **Feature Branches:** `feature/{feature-name}`
- **Bug Fixes:** `bugfix/{bug-description}`
- **Hotfixes:** `hotfix/{issue-description}`
- **Main Branch:** `main` or `master` (to be established)

### Current Git Configuration

- **Remote URL:** `http://local_proxy@127.0.0.1:47198/git/vitoiitmBSc/Claude_Code`
- **Current Branch:** `claude/claude-md-mi043mjzbu6ym3ao-01REdMfEePNeADrAdRgwhXKn`
- **Owner:** vitoiitmBSc

### Commit Message Guidelines

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(core): add user authentication module

Implements basic user authentication with JWT tokens.
Includes login, logout, and token refresh functionality.

Related to #123

---

fix(hello): correct output message typo

Changed "hello ganesh" to proper capitalization.

---

docs: create CLAUDE.md for AI assistant guidance

Comprehensive documentation for AI assistants working on this repo.
```

### Git Push Requirements

**CRITICAL:** When pushing changes:

```bash
# Always use -u flag for new branches
git push -u origin <branch-name>

# Branch MUST start with 'claude/' and end with matching session ID
# Otherwise push will fail with 403 error
```

**Network Retry Policy:**
- If push/fetch fails due to network errors, retry up to 4 times
- Use exponential backoff: 2s, 4s, 8s, 16s

---

## Code Conventions

### Python Style Guide

Follow **PEP 8** - Python's official style guide.

#### Key Points

1. **Indentation:** 4 spaces (no tabs)
2. **Line Length:** Maximum 79 characters for code, 72 for docstrings
3. **Imports:**
   - Standard library first
   - Third-party packages second
   - Local modules third
   - Separated by blank lines

4. **Naming Conventions:**
   - `snake_case` for functions and variables
   - `PascalCase` for classes
   - `UPPER_CASE` for constants
   - `_leading_underscore` for private/internal

5. **Docstrings:** Use for all public modules, functions, classes, and methods

#### Example

```python
"""
Module for greeting functionality.

This module provides functions to greet users.
"""

# Standard library imports
import sys
from typing import Optional

# Third-party imports
# (none yet)

# Local imports
# (none yet)

# Constants
DEFAULT_GREETING = "Hello"


def greet_user(name: str, greeting: Optional[str] = None) -> str:
    """
    Generate a greeting message for a user.

    Args:
        name: The name of the person to greet
        greeting: Optional custom greeting (default: "Hello")

    Returns:
        A formatted greeting string

    Examples:
        >>> greet_user("Ganesh")
        'Hello Ganesh'
        >>> greet_user("Ganesh", "Hi")
        'Hi Ganesh'
    """
    if greeting is None:
        greeting = DEFAULT_GREETING

    return f"{greeting} {name}"


class Greeter:
    """A class for managing greetings."""

    def __init__(self, default_greeting: str = "Hello"):
        """
        Initialize the Greeter.

        Args:
            default_greeting: The default greeting to use
        """
        self._greeting = default_greeting

    def greet(self, name: str) -> str:
        """Generate a greeting for the given name."""
        return f"{self._greeting} {name}"
```

### Code Quality Tools (Recommended)

When the project grows, consider adding:

- **Black:** Code formatter
- **isort:** Import sorting
- **pylint/flake8:** Linting
- **mypy:** Type checking
- **pre-commit:** Git hooks for code quality

---

## Testing Guidelines

### Testing Framework (To Be Implemented)

**Recommended:** pytest

#### Installation

```bash
pip install pytest pytest-cov
```

#### Directory Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_hello.py        # Tests for hello functionality
└── integration/         # Integration tests
    └── test_*.py
```

#### Writing Tests

```python
"""Tests for hello_ganesh module."""

import pytest
from hello_ganesh import greet_user


def test_greet_user_default():
    """Test greeting with default message."""
    result = greet_user("Ganesh")
    assert result == "Hello Ganesh"


def test_greet_user_custom():
    """Test greeting with custom message."""
    result = greet_user("Ganesh", "Hi")
    assert result == "Hi Ganesh"


@pytest.mark.parametrize("name,expected", [
    ("Ganesh", "Hello Ganesh"),
    ("Alice", "Hello Alice"),
    ("Bob", "Hello Bob"),
])
def test_greet_user_multiple(name, expected):
    """Test greeting with multiple names."""
    assert greet_user(name) == expected
```

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_hello.py

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

### Test Coverage Requirements

- **Target:** 80% minimum coverage
- **Critical Paths:** 100% coverage
- **New Features:** Must include tests

---

## AI Assistant Guidelines

### General Principles

1. **Always Read Before Writing**
   - Use `Read` tool before editing any file
   - Understand context before making changes

2. **Use Specialized Tools**
   - Prefer `Edit` over `Write` for existing files
   - Use `Glob` and `Grep` for searching
   - Use `Task` agent for complex exploration

3. **Communication**
   - Output text directly to users (don't use echo/print in bash)
   - Be concise and clear
   - Avoid unnecessary emojis unless requested

4. **Code Quality**
   - Follow PEP 8 for Python
   - Add type hints where appropriate
   - Write docstrings for public APIs
   - Include tests for new functionality

### Security Considerations

**CRITICAL:** Always check for security vulnerabilities:

- **Command Injection:** Sanitize user inputs
- **Path Traversal:** Validate file paths
- **SQL Injection:** Use parameterized queries (when DB is added)
- **XSS:** Sanitize outputs (if web interface is added)
- **Secrets Management:** Never commit credentials
- **Dependency Security:** Use `pip-audit` or similar tools

### Task Management

1. **Use TodoWrite Tool:**
   - Create todos for multi-step tasks
   - Mark tasks as in_progress before starting
   - Mark completed immediately after finishing
   - Only ONE task in_progress at a time

2. **Task Planning:**
   - Break complex tasks into smaller steps
   - Provide clear, actionable task descriptions
   - Use imperative form for todo content
   - Use present continuous for activeForm

### File Operations

**DO:**
- Use `Read` for reading files
- Use `Edit` for modifying existing files
- Use `Write` only for new files
- Use `Glob` for finding files by pattern
- Use `Grep` for searching file contents

**DON'T:**
- Use `cat`, `head`, `tail` in bash
- Use `echo` or `sed` for file operations
- Create files unnecessarily
- Edit files without reading them first

### Git Operations

**Critical Rules:**

1. **Branch Names:**
   - MUST start with `claude/`
   - MUST end with matching session ID
   - Format: `claude/claude-md-{identifier}-{session-id}`

2. **Pushing Changes:**
   - Always use `git push -u origin <branch-name>`
   - Retry on network failures (up to 4 times, exponential backoff)
   - Never push to wrong branch without permission

3. **Commit Messages:**
   - Use conventional commit format
   - Be descriptive and clear
   - Focus on "why" not just "what"

4. **Hooks:**
   - Respect pre-commit hooks
   - Never skip with `--no-verify` unless explicitly requested

### Code Review Checklist

Before committing, verify:

- [ ] Code follows PEP 8 style guide
- [ ] Type hints added where appropriate
- [ ] Docstrings written for public APIs
- [ ] Tests added for new functionality
- [ ] Tests pass successfully
- [ ] No security vulnerabilities introduced
- [ ] No hardcoded secrets or credentials
- [ ] Imports properly organized
- [ ] No unnecessary files created
- [ ] Documentation updated if needed

### Common Tasks

#### Adding a New Feature

1. Create/verify on correct branch
2. Use TodoWrite to plan implementation
3. Read relevant existing files
4. Implement functionality following conventions
5. Add tests
6. Run tests to verify
7. Update documentation
8. Commit with conventional message
9. Push to branch

#### Fixing a Bug

1. Understand the issue (read code, check tests)
2. Create todos for fix steps
3. Write a failing test that reproduces the bug
4. Fix the bug
5. Verify test now passes
6. Check for similar issues elsewhere
7. Update documentation if needed
8. Commit and push

#### Refactoring Code

1. Ensure existing tests pass
2. Plan refactoring steps
3. Make changes incrementally
4. Run tests after each change
5. Maintain backward compatibility (if it's an API)
6. Update documentation
7. Commit and push

---

## Future Development

### Recommended Next Steps

1. **Project Configuration**
   - [ ] Add `.gitignore` file
   - [ ] Create `requirements.txt` or `pyproject.toml`
   - [ ] Add `README.md` with project description
   - [ ] Set up `setup.py` if building a package

2. **Development Infrastructure**
   - [ ] Set up virtual environment guidelines
   - [ ] Configure testing framework (pytest)
   - [ ] Add code quality tools (black, isort, pylint)
   - [ ] Create pre-commit hooks

3. **Documentation**
   - [ ] Write comprehensive README
   - [ ] Add inline documentation
   - [ ] Create API documentation (if applicable)
   - [ ] Add usage examples

4. **CI/CD**
   - [ ] Set up GitHub Actions or similar
   - [ ] Automate testing
   - [ ] Automate linting
   - [ ] Add coverage reporting

5. **Code Organization**
   - [ ] Create `src/` directory structure
   - [ ] Move code into modules
   - [ ] Add `__init__.py` files
   - [ ] Organize into logical components

### Scalability Considerations

As the project grows:

- **Modularization:** Break code into logical modules
- **Configuration Management:** Use environment variables or config files
- **Logging:** Implement structured logging
- **Error Handling:** Comprehensive exception handling
- **Documentation:** Keep docs in sync with code
- **Performance:** Profile and optimize as needed

### Technology Recommendations

Depending on project direction, consider:

- **Web Framework:** Flask, FastAPI, Django
- **CLI Framework:** Click, Typer, argparse
- **Database:** SQLite, PostgreSQL, MongoDB
- **Caching:** Redis, Memcached
- **API Client:** requests, httpx
- **Async:** asyncio, aiohttp
- **Data Processing:** pandas, numpy
- **Testing:** pytest, unittest, mock

---

## Appendix

### Useful Commands

#### Git Commands

```bash
# Check status
git status

# View changes
git diff

# Stage changes
git add <file>
git add .

# Commit
git commit -m "type(scope): message"

# Push to remote
git push -u origin <branch-name>

# Fetch updates
git fetch origin <branch-name>

# Pull updates
git pull origin <branch-name>

# View commit history
git log --oneline --graph --all

# View branches
git branch -a
```

#### Python Commands

```bash
# Run script
python hello_ganesh.py

# Run with module syntax
python -m module_name

# Check Python version
python --version

# Install package
pip install <package>

# List installed packages
pip list

# Freeze dependencies
pip freeze > requirements.txt

# Create virtual environment
python -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Deactivate virtual environment
deactivate
```

#### Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test
pytest tests/test_file.py::test_function

# Run verbose
pytest -v

# Run with output
pytest -s

# Run and stop on first failure
pytest -x
```

### Resources

- **PEP 8:** https://pep8.org/
- **Python Documentation:** https://docs.python.org/3/
- **pytest Documentation:** https://docs.pytest.org/
- **Git Documentation:** https://git-scm.com/doc
- **Conventional Commits:** https://www.conventionalcommits.org/

### Contact and Support

For questions or issues related to this repository:

1. Check existing documentation
2. Review commit history for context
3. Consult this CLAUDE.md file
4. Refer to external resources listed above

---

**Document Version:** 1.0
**Last Updated:** 2025-11-15
**Maintained By:** AI Assistants working on this repository
