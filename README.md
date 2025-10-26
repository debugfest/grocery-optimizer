# 🛒 Grocery List & Expense Optimizer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)


A Python application for managing grocery shopping, tracking expenses, and optimizing budgets with smart suggestions and analytics. Built with Rich CLI interface and matplotlib visualizations.

## ✨ Features

- **Grocery Management**: Add, edit, delete items with price per unit, categories, and stores
- **Expense Tracking**: Track spending by category, store, and time period
- **Budget Monitoring**: Set weekly/monthly limits with alerts
- **Charts & Reports**: Generate visualizations with pie charts, bar charts, and trends
- **Search & Filter**: Find items by name, category, store, or price range
- **Rich CLI**: Beautiful colored console output with tables

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/debugfest/grocery-optimizer.git
cd grocery-optimizer

# Create virtual environment (optional)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Demo

```bash
python demo.py
```

## 📖 Usage

**Main Sections:**
- Grocery Items Management: Add, edit, delete items
- Expense Tracking: Track spending by category and store
- Budget Management: Set weekly/monthly limits with alerts
- Reports & Visualizations: Generate charts and analytics
- Search & Filter: Find items by name, category, store, or price

**Adding Items:**
Enter item name, category, quantity, unit, price per unit, store name, and optional notes.

**Reports:**
Generate summary reports, spending by category/store charts, price distribution, trends, and budget comparison.

## 🏗️ Project Structure

- **`main.py`**: CLI entry point with Rich library
- **`grocery.py`**: Grocery items CRUD operations
- **`expense.py`**: Spending calculations and analytics
- **`reports.py`**: Report generation and matplotlib charts
- **`utils.py`**: Validation and formatting functions
- **`demo.py`**: Demo script with sample data
- **`data/grocery_data.db`**: SQLite database (auto-created)
- **`reports/`**: Generated reports and charts

## 🐛 Troubleshooting

**Common Issues:**
- Database errors: Ensure `data/` directory exists with write permissions
- Chart generation fails: Run `pip install --upgrade matplotlib`
- Import errors: Run `pip install -r requirements.txt`

**Input Format:**
- Price formats: `$10.50`, `₹100`, or `10.50`
- Quantity: Numeric values like `2.5`, `1`, or `0.5`
- Database created automatically on first run

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick Start:**
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request



**Acknowledgments:** [Rich](https://github.com/Textualize/rich), [Matplotlib](https://matplotlib.org/), [SQLite](https://www.sqlite.org/)

---

**Made with ❤️ for smart grocery shopping** 🛒💰
