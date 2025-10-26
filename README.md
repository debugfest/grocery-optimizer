# 💳 Subscription Manager

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python application for managing subscriptions with both CLI and GUI interfaces. Track monthly subscriptions, monitor renewal dates, analyze costs, and generate reports with visualizations.

## ✨ Features

- **Subscription Management**: Add, edit, delete, and search subscriptions
- **Cost Tracking**: Monthly and annual cost calculation with category breakdown
- **Renewal Monitoring**: Track upcoming renewals and overdue subscriptions
- **Reports & Charts**: Generate reports and visualize subscription spending
- **Dual Interfaces**: CLI for power users, GUI for easy use
- **Data Visualization**: Pie charts, bar charts, and trend analysis

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/debugfest/subscription-manager.git
cd subscription-manager

# Create virtual environment (optional)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python launcher.py          # Choose CLI or GUI
# Or run directly:
python main.py              # CLI interface
python gui.py               # GUI interface
```

### Demo

```bash
python demo.py
```

## 📖 Usage

**Choose Interface:**
- CLI: Full-featured command-line interface
- GUI: User-friendly graphical interface with buttons and tables

**Key Features:**
- Add subscriptions: Name, category, cost, renewal date, payment method
- View total monthly/annual costs with category breakdown
- Monitor upcoming renewals and overdue subscriptions
- Generate reports: Summary, renewal, cost analysis charts
- Search and filter by name, category, cost, or renewal date

## 🏗️ Project Structure

- **`main.py`**: CLI interface
- **`gui.py`**: Tkinter GUI interface
- **`launcher.py`**: Interface launcher script
- **`subscription.py`**: Data model and database operations
- **`report.py`**: Report generation and visualizations
- **`utils.py`**: Validation and utility functions
- **`demo.py`**: Demo script with sample data
- **`data/subscriptions.db`**: SQLite database (auto-created)
- **`reports/`**: Generated reports and charts

## 🐛 Troubleshooting

**Common Issues:**
- Database errors: Ensure write permissions in project directory
- GUI not displaying: Install `python3-tk` on Linux (`sudo apt-get install python3-tk`)
- Import errors: Run `pip install -r requirements.txt` and verify Python 3.8+

**Input Format:**
- Renewal dates must be YYYY-MM-DD format (e.g., 2024-02-15)
- Cost must be a positive number
- Subscription name: 2-100 characters
- Category: 2-50 characters

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick Start:**
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request


**Acknowledgments:** [Matplotlib](https://matplotlib.org/), [SQLite](https://www.sqlite.org/), [Tkinter](https://docs.python.org/3/library/tkinter.html)

---

**Made with ❤️ for subscription management** 💳📊
