# 🤝 Contributing to Subscription Manager

Thank you for your interest in contributing! This guide will help you get started.

## 📜 Code of Conduct

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community

## 🚀 Getting Started

**Prerequisites:** Python 3.8+, Git, GitHub account

**Setup:**
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/subscription-manager.git
cd subscription-manager

# Add upstream remote
git remote add upstream https://github.com/debugfest/subscription-manager.git

# Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Verify installation
python launcher.py        # Choose interface
python demo.py            # Run demo
pytest                    # Run tests
```

## 📁 Project Structure

- **`main.py`**: CLI interface and user interaction
- **`gui.py`**: Tkinter GUI interface
- **`launcher.py`**: Interface launcher
- **`subscription.py`**: Data model and database operations
- **`report.py`**: Report generation and visualizations
- **`utils.py`**: Validation and utility functions
- **`demo.py`**: Demo script with sample data

## 📝 How to Contribute

**We welcome:**
- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🧪 Tests and test coverage
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🔧 Code refactoring

## 🔄 Pull Request Process

**Steps:**
1. Create feature branch: `git checkout -b feature/your-feature-name`
2. Make changes following coding standards
3. Add tests for new functionality
4. Run tests and linting:
   ```bash
   pytest
   flake8 subscription_manager/
   black --check subscription_manager/
   mypy subscription_manager/
   ```
5. Commit and push: `git push origin feature/your-feature-name`

**PR Checklist:**
- [ ] Code follows coding standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No linting errors

## 🐛 Issue Guidelines

**Bug Reports:**
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages and stack traces

**Feature Requests:**
- Clear description and use case
- Proposed solution
- Alternatives considered

**Labels:** `bug`, `enhancement`, `documentation`, `good first issue`, `help wanted`

## 📚 Resources

- [Python Docs](https://docs.python.org/3/)
- [Matplotlib](https://matplotlib.org/)
- [SQLite](https://www.sqlite.org/docs.html)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pytest](https://docs.pytest.org/)
- [Black](https://black.readthedocs.io/)
- [Flake8](https://flake8.pycqa.org/)
- [MyPy](https://mypy.readthedocs.io/)

## 💬 Getting Help

- Check existing issues
- Read documentation and code comments
- Create a new issue with details
- Join GitHub Discussions

---

**Thank you for contributing!** 💳📊
