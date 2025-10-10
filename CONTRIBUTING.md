# 🤝 Contributing to Grocery List & Expense Optimizer

Thank you for your interest in contributing to the Grocery List & Expense Optimizer! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Contribution Guidelines](#contribution-guidelines)
- [Priority TODOs](#priority-todos)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project follows a code of conduct that ensures a welcoming environment for all contributors. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Basic knowledge of Python, SQLite, and CLI applications

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/grocery-optimizer.git
   cd grocery-optimizer
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/originalowner/grocery-optimizer.git
   ```

## 🛠️ Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 3. Verify Installation

```bash
# Run the application
python main.py

# Run the demo
python demo.py

# Run tests (if available)
pytest
```

## 📁 Project Structure

```
grocery_optimizer/
├── main.py                 # CLI entry point
├── grocery.py              # Grocery items management
├── expense.py              # Expense tracking and analytics
├── reports.py              # Report generation and charts
├── utils.py                # Utility functions
├── demo.py                 # Demo script
├── data/                   # Database storage
│   └── grocery_data.db     # SQLite database
├── reports/                # Generated reports
├── tests/                  # Test files (to be created)
├── requirements.txt        # Dependencies
├── README.md              # Project documentation
└── CONTRIBUTING.md        # This file
```

### Module Responsibilities

- **`main.py`**: CLI interface, user interaction, menu handling
- **`grocery.py`**: Grocery item CRUD operations, database management
- **`expense.py`**: Budget tracking, spending analytics, cost optimization
- **`reports.py`**: Chart generation, report creation, data visualization
- **`utils.py`**: Validation, formatting, date handling, common utilities

## 📝 Contribution Guidelines

### Types of Contributions

We welcome various types of contributions:

1. **🐛 Bug Fixes**: Fix existing issues and bugs
2. **✨ New Features**: Add new functionality
3. **📚 Documentation**: Improve documentation and examples
4. **🧪 Tests**: Add or improve test coverage
5. **🎨 UI/UX**: Enhance user interface and experience
6. **⚡ Performance**: Optimize code performance
7. **🔧 Refactoring**: Improve code structure and maintainability

### Before You Start

1. **Check existing issues** to see if your idea is already being worked on
2. **Create an issue** for significant changes to discuss the approach
3. **Read the Priority TODOs** section below for high-priority items
4. **Follow the coding standards** outlined in this document

## 🎯 Priority TODOs

These are high-priority items that contributors can work on:

### 🔥 Critical Issues

1. **Fix bug: total cost sometimes miscalculates when quantity changes**
   - **File**: `grocery.py` (GroceryItem class)
   - **Description**: The `total_cost` property may not update correctly when quantity changes
   - **Priority**: High
   - **Estimated Effort**: 2-4 hours

2. **Add unit tests for grocery and expense modules**
   - **Files**: Create `tests/test_grocery.py`, `tests/test_expense.py`
   - **Description**: Add comprehensive test coverage for core functionality
   - **Priority**: High
   - **Estimated Effort**: 8-12 hours

### 🚀 New Features

3. **Add online price scraping**
   - **Description**: Fetch real prices from grocery APIs or websites
   - **Files**: New module `price_scraper.py`
   - **Priority**: Medium
   - **Estimated Effort**: 12-16 hours
   - **Dependencies**: `requests`, `beautifulsoup4`, `selenium`

4. **Add sort by cost-per-unit feature**
   - **File**: `grocery.py` (GroceryManager class)
   - **Description**: Add sorting by cost per unit in addition to total cost
   - **Priority**: Medium
   - **Estimated Effort**: 2-3 hours

5. **Add list sharing via JSON export/import**
   - **Files**: New module `import_export.py`
   - **Description**: Allow users to export/import grocery lists as JSON
   - **Priority**: Medium
   - **Estimated Effort**: 4-6 hours

6. **Add budget suggestion feature**
   - **File**: `expense.py` (ExpenseTracker class)
   - **Description**: Auto-suggest cheaper alternatives for expensive items
   - **Priority**: Medium
   - **Estimated Effort**: 6-8 hours

7. **Integrate voice input for adding grocery items**
   - **Files**: New module `voice_input.py`, update `main.py`
   - **Description**: Allow users to add items using voice commands
   - **Priority**: Low
   - **Estimated Effort**: 8-10 hours
   - **Dependencies**: `speech_recognition`, `pyttsx3`

8. **Improve Tkinter GUI layout for better UX**
   - **Files**: New module `gui.py`
   - **Description**: Create a better GUI interface using Tkinter
   - **Priority**: Low
   - **Estimated Effort**: 10-15 hours

## 📏 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all functions, classes, and modules
- Use **descriptive variable names** (avoid abbreviations)
- Keep **line length** under 88 characters (Black formatter standard)

### Code Formatting

We use **Black** for code formatting:

```bash
# Format code
black grocery_optimizer/

# Check formatting
black --check grocery_optimizer/
```

### Linting

We use **flake8** for linting:

```bash
# Run linter
flake8 grocery_optimizer/

# Run with specific rules
flake8 --max-line-length=88 --extend-ignore=E203,W503 grocery_optimizer/
```

### Type Checking

We use **mypy** for type checking:

```bash
# Run type checker
mypy grocery_optimizer/
```

### Example Code Style

```python
def calculate_total_cost(items: List[GroceryItem]) -> float:
    """
    Calculate the total cost of a list of grocery items.
    
    Args:
        items: List of GroceryItem objects
        
    Returns:
        float: Total cost of all items
        
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    
    return sum(item.total_cost for item in items)
```

## 🧪 Testing Guidelines

### Test Structure

Create tests in the `tests/` directory:

```
tests/
├── test_grocery.py      # Tests for grocery.py
├── test_expense.py      # Tests for expense.py
├── test_reports.py      # Tests for reports.py
├── test_utils.py        # Tests for utils.py
└── conftest.py          # Pytest configuration
```

### Test Naming Convention

- Test functions should start with `test_`
- Use descriptive names: `test_add_item_success`, `test_invalid_price_raises_error`
- Group related tests in classes: `class TestGroceryManager:`

### Example Test

```python
import pytest
from grocery import GroceryManager, GroceryItem

class TestGroceryManager:
    """Test cases for GroceryManager class."""
    
    def test_add_item_success(self):
        """Test successful item addition."""
        manager = GroceryManager()
        item = GroceryItem(
            name="Test Item",
            category="Test Category",
            quantity=1.0,
            unit="piece",
            price_per_unit=10.0,
            store_name="Test Store"
        )
        
        item_id = manager.add_item(item)
        assert item_id is not None
        assert item_id > 0
    
    def test_add_item_invalid_data(self):
        """Test item addition with invalid data."""
        manager = GroceryManager()
        item = GroceryItem(
            name="",  # Invalid empty name
            category="Test Category",
            quantity=1.0,
            unit="piece",
            price_per_unit=10.0,
            store_name="Test Store"
        )
        
        with pytest.raises(ValueError, match="Item name cannot be empty"):
            manager.add_item(item)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=grocery_optimizer --cov-report=html

# Run specific test file
pytest tests/test_grocery.py

# Run with verbose output
pytest -v
```

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Add tests** for new functionality

4. **Update documentation** if needed

5. **Run tests and linting**:
   ```bash
   pytest
   flake8 grocery_optimizer/
   black --check grocery_optimizer/
   mypy grocery_optimizer/
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Template

When creating a PR, include:

- **Description**: What changes were made and why
- **Type**: Bug fix, new feature, documentation, etc.
- **Testing**: How the changes were tested
- **Screenshots**: If applicable (for UI changes)
- **Checklist**: Ensure all items are completed

### PR Checklist

- [ ] Code follows the project's coding standards
- [ ] Self-review of code has been performed
- [ ] Code has been commented, particularly in hard-to-understand areas
- [ ] Tests have been added/updated for new functionality
- [ ] Documentation has been updated if necessary
- [ ] All tests pass
- [ ] No linting errors
- [ ] Type checking passes

## 🐛 Issue Guidelines

### Bug Reports

When reporting bugs, include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the bug
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots** if applicable
6. **Error messages** and stack traces

### Feature Requests

When requesting features, include:

1. **Clear title** describing the feature
2. **Use case** and motivation
3. **Proposed solution** or approach
4. **Alternatives considered**
5. **Additional context** if relevant

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority: high`: High priority issue
- `priority: medium`: Medium priority issue
- `priority: low`: Low priority issue

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version number is updated
- [ ] CHANGELOG.md is updated
- [ ] Release notes are prepared
- [ ] Tag is created
- [ ] Release is published

## 📚 Additional Resources

### Documentation

- [Python Documentation](https://docs.python.org/3/)
- [Rich Library Documentation](https://rich.readthedocs.io/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pytest Documentation](https://docs.pytest.org/)

### Development Tools

- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Pytest Testing Framework](https://docs.pytest.org/)

## 💬 Getting Help

If you need help or have questions:

1. **Check existing issues** for similar problems
2. **Read the documentation** and code comments
3. **Create a new issue** with detailed information
4. **Join discussions** in GitHub Discussions
5. **Ask questions** in the community forum

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Project documentation**

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for contributing to the Grocery List & Expense Optimizer!** 🛒💰

*Together, we can make grocery shopping smarter and more efficient for everyone!*
