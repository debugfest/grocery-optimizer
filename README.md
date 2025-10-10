# 🛒 Grocery List & Expense Optimizer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-blue.svg)](https://pep8.org)

A comprehensive Python application for managing your grocery shopping, tracking expenses, and optimizing your budget with smart suggestions and detailed analytics. Built with a beautiful CLI interface using the Rich library and powerful data visualization with matplotlib.

## ✨ Features

### 🛒 **Grocery Items Management**
- **CRUD Operations**: Add, edit, delete, and organize grocery items
- **Detailed Tracking**: Track quantity, price per unit, categories, and stores
- **Purchase Status**: Mark items as purchased/unpurchased with dates
- **Smart Validation**: Comprehensive input validation and error handling
- **Notes Support**: Add optional notes and descriptions to items

### 💰 **Expense Tracking & Analytics**
- **Spending Analysis**: Track spending by category, store, and time period
- **Budget Monitoring**: Set weekly and monthly budget limits with alerts
- **Cost Insights**: Get insights into spending patterns and trends
- **Optimization Suggestions**: Receive suggestions for cheaper alternatives
- **Store Comparisons**: Compare prices across different stores

### 📊 **Data Visualization & Reports**
- **Rich CLI Interface**: Beautiful, colored console output with tables and panels
- **Chart Generation**: Generate charts and graphs with matplotlib
- **Comprehensive Reports**: Detailed spending summaries and analytics
- **Multiple Chart Types**: Pie charts, bar charts, histograms, and line charts
- **Export Capabilities**: Save reports and charts to files

### 🔍 **Search & Filter**
- **Advanced Search**: Find items by name, category, or store
- **Smart Filtering**: Filter by price ranges, categories, and stores
- **Flexible Sorting**: Sort by price, cost, category, name, or store
- **Quick Access**: Identify expensive and budget-friendly items

### 🏗️ **Technical Features**
- **Data Persistence**: SQLite database for reliable data storage
- **Modular Design**: Clean, maintainable code structure with type hints
- **Error Handling**: Graceful failure modes and user-friendly error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/grocery-optimizer.git
   cd grocery-optimizer
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Demo

Try the demo to see the application in action:

```bash
python demo.py
```

## 📖 Usage Guide

### Main Menu Navigation

The application features an intuitive CLI interface with the following main sections:

```
🛒 Grocery Items Management    - Add, edit, and manage grocery items
💰 Expense Tracking & Analytics - Track spending and view analytics  
📊 Budget Management          - Set and monitor budget limits
📈 Reports & Visualizations   - Generate reports and charts
🔍 Search & Filter Items      - Search and filter grocery items
⚙️ Settings & Configuration   - Configure application settings
❌ Exit                       - Close the application
```

### Adding Grocery Items

1. Select "Grocery Items Management" from the main menu
2. Choose "Add New Item"
3. Fill in the required information:
   - **Item Name**: Name of the grocery item
   - **Category**: Choose from predefined categories or enter custom
   - **Quantity**: Amount needed (supports decimal values)
   - **Unit**: Measurement unit (kg, g, piece, pack, etc.)
   - **Price per Unit**: Cost per unit (supports various formats)
   - **Store Name**: Where you plan to buy the item
   - **Notes**: Optional additional details

### Setting Budgets

1. Navigate to "Budget Management"
2. Set your weekly and/or monthly budget limits
3. Monitor your spending against these limits
4. Receive alerts when approaching or exceeding budgets

### Generating Reports

1. Go to "Reports & Visualizations"
2. Choose from various report types:
   - Grocery Summary Report
   - Spending by Category Chart
   - Spending by Store Chart
   - Price Distribution Chart
   - Spending Trend Chart
   - Budget vs Actual Chart
   - Store Comparison Chart
   - Comprehensive Report (all charts)

### Searching and Filtering

1. Access "Search & Filter Items"
2. Use various filtering options:
   - Search by name, category, or store
   - Filter by price range
   - Show expensive or budget-friendly items
   - Sort by different criteria

## 🏗️ Project Structure

```
grocery_optimizer/
├── main.py                 # CLI entry point with Rich library
├── grocery.py              # Grocery items CRUD operations
├── expense.py              # Spending calculations and analytics
├── reports.py              # Report generation and matplotlib charts
├── utils.py                # Validation, date parsing, and formatting
├── demo.py                 # Demo script with sample data
├── data/
│   └── grocery_data.db     # SQLite database (auto-created)
├── reports/                # Generated reports and charts
├── venv/                   # Virtual environment (if created)
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── CONTRIBUTING.md        # Contribution guidelines
```

## 🔧 API Reference

### Core Classes

#### `GroceryItem`
Data class representing a grocery item with validation.

```python
from grocery import GroceryItem

item = GroceryItem(
    name="Organic Apples",
    category="Fruits & Vegetables",
    quantity=2.0,
    unit="kg",
    price_per_unit=4.50,
    store_name="Whole Foods",
    notes="Red delicious apples"
)
```

#### `GroceryManager`
Manages grocery items and database operations.

```python
from grocery import GroceryManager

manager = GroceryManager()
item_id = manager.add_item(item)
items = manager.get_all_items()
```

#### `ExpenseTracker`
Handles spending calculations and analytics.

```python
from expense import ExpenseTracker

tracker = ExpenseTracker()
weekly_spending = tracker.get_weekly_spending()
category_breakdown = tracker.get_spending_by_category()
```

#### `ReportGenerator`
Generates reports and visualizations.

```python
from reports import ReportGenerator

generator = ReportGenerator(manager, tracker)
generator.generate_grocery_summary()
generator.generate_spending_by_category_chart()
```

### Utility Functions

```python
from utils import validate_price, parse_price, format_currency

# Validate price input
is_valid = validate_price("$10.50")  # True

# Parse price string
price = parse_price("$10.50")  # 10.5

# Format currency
formatted = format_currency(10.5)  # "$10.50"
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=grocery_optimizer
```

### Test Structure

```
tests/
├── test_grocery.py      # Tests for grocery module
├── test_expense.py      # Tests for expense module
├── test_utils.py        # Tests for utility functions
└── test_reports.py      # Tests for report generation
```

## 🐛 Troubleshooting

### Common Issues

#### Database Not Found
The application automatically creates the database on first run. If you encounter issues:
```bash
# Ensure the data directory exists
mkdir -p data
```

#### Permission Errors
Make sure you have write permissions for the `data/` and `reports/` directories:
```bash
chmod 755 data reports
```

#### Chart Generation Fails
Ensure matplotlib is properly installed:
```bash
pip install --upgrade matplotlib
```

#### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Error Messages

| Error | Solution |
|-------|----------|
| `Invalid price format` | Use supported formats like `$10.50`, `₹100`, or `10.50` |
| `Invalid quantity format` | Use numeric values like `2.5`, `1`, or `0.5` |
| `Database error` | Check file permissions and disk space |
| `No data available` | Add some items first before generating reports |

## 🔮 Roadmap

### Planned Features

- [ ] **Online Price Scraping**: Fetch real prices from grocery APIs
- [ ] **Voice Input**: Add items using voice commands
- [ ] **Mobile App**: Cross-platform mobile support
- [ ] **Barcode Scanning**: Quick item addition via barcode
- [ ] **Recipe Integration**: Add items from recipes
- [ ] **Family Sharing**: Share lists with family members
- [ ] **Nutritional Information**: Add nutritional data to items
- [ ] **Shopping Route Optimization**: Optimize routes for multiple stores

### Known Issues

- [ ] Total cost sometimes miscalculates when quantity changes
- [ ] Store comparison data limited to items available in multiple stores
- [ ] No support for recurring items yet

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) for the beautiful CLI interface
- [Matplotlib](https://matplotlib.org/) for data visualization
- [SQLite](https://www.sqlite.org/) for data persistence
- The Python community for excellent libraries and tools

## 📞 Support

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/yourusername/grocery-optimizer/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/yourusername/grocery-optimizer/discussions)

## 📊 Project Statistics

- **Lines of Code**: ~2,500+
- **Test Coverage**: 85%+ (target)
- **Dependencies**: 3 core, 6 optional
- **Python Version**: 3.8+
- **Database**: SQLite
- **UI Framework**: Rich (CLI)

---

**Made with ❤️ for smart grocery shopping**

*Start optimizing your grocery shopping today!* 🛒💰