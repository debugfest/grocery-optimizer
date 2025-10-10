"""
Utility functions for the grocery optimizer.

This module contains helper functions for validation, date parsing,
formatting, and other common operations used throughout the application.
"""

import re
from datetime import datetime, date, timedelta
from typing import Optional, List, Tuple, Union


def validate_price(price: Union[str, float, int]) -> bool:
    """
    Validate if a price is a valid positive number.
    
    Args:
        price: Price to validate
        
    Returns:
        bool: True if price is valid, False otherwise
    """
    try:
        if isinstance(price, str):
            # Remove currency symbols and spaces
            cleaned = re.sub(r'[₹$€£¥\s,]', '', price.strip())
            value = float(cleaned)
        else:
            value = float(price)
        
        return value >= 0
    except (ValueError, TypeError):
        return False


def parse_price(price_input: str) -> float:
    """
    Parse a price string and return a float value.
    
    Args:
        price_input: Price string (e.g., "10.50", "₹10.50", "$10.50")
        
    Returns:
        float: Parsed price value
        
    Raises:
        ValueError: If price string cannot be parsed
    """
    if not price_input:
        raise ValueError("Price cannot be empty")
    
    # Remove currency symbols, spaces, and commas
    cleaned = re.sub(r'[₹$€£¥\s,]', '', price_input.strip())
    
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError(f"Invalid price format: {price_input}")


def validate_quantity(quantity: Union[str, float, int]) -> bool:
    """
    Validate if a quantity is a valid positive number.
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        bool: True if quantity is valid, False otherwise
    """
    try:
        if isinstance(quantity, str):
            value = float(quantity.strip())
        else:
            value = float(quantity)
        
        return value > 0
    except (ValueError, TypeError):
        return False


def parse_quantity(quantity_input: str) -> float:
    """
    Parse a quantity string and return a float value.
    
    Args:
        quantity_input: Quantity string (e.g., "2.5", "1", "0.5")
        
    Returns:
        float: Parsed quantity value
        
    Raises:
        ValueError: If quantity string cannot be parsed
    """
    if not quantity_input:
        raise ValueError("Quantity cannot be empty")
    
    try:
        return float(quantity_input.strip())
    except ValueError:
        raise ValueError(f"Invalid quantity format: {quantity_input}")


def format_currency(amount: float, currency_symbol: str = "$") -> str:
    """
    Format a float amount as currency string.
    
    Args:
        amount: Amount to format
        currency_symbol: Currency symbol to use
        
    Returns:
        str: Formatted currency string
    """
    return f"{currency_symbol}{amount:,.2f}"


def validate_date(date_string: str) -> bool:
    """
    Validate if a date string is in the correct format (YYYY-MM-DD).
    
    Args:
        date_string: Date string to validate
        
    Returns:
        bool: True if date is valid, False otherwise
    """
    if not date_string:
        return False
    
    # Check format with regex
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_pattern, date_string):
        return False
    
    try:
        # Try to parse the date
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_date(date_string: str, input_format: str = '%Y-%m-%d', output_format: str = '%B %d, %Y') -> str:
    """
    Format a date string from one format to another.
    
    Args:
        date_string: Date string to format
        input_format: Format of the input date string
        output_format: Desired output format
        
    Returns:
        str: Formatted date string
        
    Raises:
        ValueError: If date string is invalid
    """
    try:
        date_obj = datetime.strptime(date_string, input_format)
        return date_obj.strftime(output_format)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")


def get_current_date_string() -> str:
    """
    Get current date as a string in YYYY-MM-DD format.
    
    Returns:
        str: Current date string
    """
    return date.today().strftime('%Y-%m-%d')


def get_week_start_date(target_date: str) -> str:
    """
    Get the start date of the week (Monday) for a given date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        str: Start date of the week in YYYY-MM-DD format
    """
    if not validate_date(target_date):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    # Calculate days since Monday (0 = Monday, 6 = Sunday)
    days_since_monday = date_obj.weekday()
    week_start = date_obj - timedelta(days=days_since_monday)
    
    return week_start.strftime('%Y-%m-%d')


def get_month_start_date(target_date: str) -> str:
    """
    Get the start date of the month for a given date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        str: Start date of the month in YYYY-MM-DD format
    """
    if not validate_date(target_date):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
    month_start = date_obj.replace(day=1)
    
    return month_start.strftime('%Y-%m-%d')


def get_month_end_date(target_date: str) -> str:
    """
    Get the end date of the month for a given date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        str: End date of the month in YYYY-MM-DD format
    """
    if not validate_date(target_date):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    # Get first day of next month, then subtract one day
    if date_obj.month == 12:
        next_month = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
    else:
        next_month = date_obj.replace(month=date_obj.month + 1, day=1)
    
    month_end = next_month - timedelta(days=1)
    
    return month_end.strftime('%Y-%m-%d')


def get_common_grocery_categories() -> List[str]:
    """
    Get a list of common grocery categories.
    
    Returns:
        List[str]: List of common categories
    """
    return [
        "Fruits & Vegetables",
        "Dairy & Eggs",
        "Meat & Seafood",
        "Bakery",
        "Pantry Staples",
        "Beverages",
        "Snacks",
        "Frozen Foods",
        "Health & Beauty",
        "Household Items",
        "Organic",
        "International",
        "Other"
    ]


def get_common_units() -> List[str]:
    """
    Get a list of common measurement units.
    
    Returns:
        List[str]: List of common units
    """
    return [
        "kg",
        "g",
        "lb",
        "oz",
        "l",
        "ml",
        "piece",
        "pack",
        "box",
        "bottle",
        "can",
        "bag",
        "dozen",
        "bunch",
        "head",
        "clove",
        "slice",
        "cup",
        "tbsp",
        "tsp"
    ]


def get_common_stores() -> List[str]:
    """
    Get a list of common grocery stores.
    
    Returns:
        List[str]: List of common stores
    """
    return [
        "Walmart",
        "Target",
        "Kroger",
        "Safeway",
        "Whole Foods",
        "Trader Joe's",
        "Costco",
        "Sam's Club",
        "Aldi",
        "Lidl",
        "Publix",
        "Wegmans",
        "Local Market",
        "Farmers Market",
        "Online Store",
        "Other"
    ]


def validate_item_name(name: str) -> bool:
    """
    Validate item name.
    
    Args:
        name: Item name to validate
        
    Returns:
        bool: True if name is valid, False otherwise
    """
    if not name or not name.strip():
        return False
    
    # Check for reasonable length
    if len(name.strip()) < 1 or len(name.strip()) > 100:
        return False
    
    return True


def validate_category(category: str) -> bool:
    """
    Validate category name.
    
    Args:
        category: Category to validate
        
    Returns:
        bool: True if category is valid, False otherwise
    """
    if not category or not category.strip():
        return False
    
    # Check for reasonable length
    if len(category.strip()) < 1 or len(category.strip()) > 50:
        return False
    
    return True


def validate_unit(unit: str) -> bool:
    """
    Validate unit name.
    
    Args:
        unit: Unit to validate
        
    Returns:
        bool: True if unit is valid, False otherwise
    """
    if not unit or not unit.strip():
        return False
    
    # Check for reasonable length
    if len(unit.strip()) < 1 or len(unit.strip()) > 20:
        return False
    
    return True


def validate_store_name(store_name: str) -> bool:
    """
    Validate store name.
    
    Args:
        store_name: Store name to validate
        
    Returns:
        bool: True if store name is valid, False otherwise
    """
    if not store_name or not store_name.strip():
        return False
    
    # Check for reasonable length
    if len(store_name.strip()) < 1 or len(store_name.strip()) > 50:
        return False
    
    return True


def validate_notes(notes: str) -> bool:
    """
    Validate notes text.
    
    Args:
        notes: Notes to validate
        
    Returns:
        bool: True if notes are valid, False otherwise
    """
    if not notes:
        return True  # Notes are optional
    
    # Check for reasonable length
    if len(notes.strip()) > 500:
        return False
    
    return True


def truncate_string(text: str, max_length: int = 30) -> str:
    """
    Truncate a string to a maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of the result
        
    Returns:
        str: Truncated string with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def format_percentage(value: float, total: float) -> str:
    """
    Format a percentage value.
    
    Args:
        value: Current value
        total: Total value
        
    Returns:
        str: Formatted percentage string
    """
    if total == 0:
        return "0.0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"


def format_progress_bar(current: float, total: float, width: int = 20) -> str:
    """
    Create a text-based progress bar.
    
    Args:
        current: Current value
        total: Total value
        width: Width of the progress bar
        
    Returns:
        str: Text-based progress bar
    """
    if total == 0:
        return "[" + " " * width + "] 0.0%"
    
    percentage = current / total
    filled_width = int(percentage * width)
    bar = "█" * filled_width + "░" * (width - filled_width)
    
    return f"[{bar}] {percentage * 100:.1f}%"


def calculate_average(values: List[float]) -> float:
    """
    Calculate average from a list of values.
    
    Args:
        values: List of values
        
    Returns:
        float: Average value
    """
    if not values:
        return 0.0
    
    return sum(values) / len(values)


def calculate_median(values: List[float]) -> float:
    """
    Calculate median from a list of values.
    
    Args:
        values: List of values
        
    Returns:
        float: Median value
    """
    if not values:
        return 0.0
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n % 2 == 0:
        return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    else:
        return sorted_values[n // 2]


def get_date_range_days(start_date: str, end_date: str) -> int:
    """
    Calculate the number of days between two dates.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        int: Number of days between dates
    """
    if not validate_date(start_date) or not validate_date(end_date):
        raise ValueError("Invalid date format")
    
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    return (end - start).days


def is_date_in_range(check_date: str, start_date: str, end_date: str) -> bool:
    """
    Check if a date falls within a given range.
    
    Args:
        check_date: Date to check in YYYY-MM-DD format
        start_date: Start of range in YYYY-MM-DD format
        end_date: End of range in YYYY-MM-DD format
        
    Returns:
        bool: True if date is in range, False otherwise
    """
    if not all(validate_date(d) for d in [check_date, start_date, end_date]):
        raise ValueError("Invalid date format")
    
    check = datetime.strptime(check_date, '%Y-%m-%d').date()
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    return start <= check <= end


def parse_csv_line(line: str) -> List[str]:
    """
    Parse a CSV line, handling quoted fields.
    
    Args:
        line: CSV line to parse
        
    Returns:
        List[str]: List of fields
    """
    fields = []
    current_field = ""
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # Escaped quote
                current_field += '"'
                i += 1
            else:
                # Toggle quote state
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            # Field separator
            fields.append(current_field.strip())
            current_field = ""
        else:
            current_field += char
        
        i += 1
    
    # Add the last field
    fields.append(current_field.strip())
    
    return fields


def validate_csv_data(data: List[List[str]], expected_columns: int) -> Tuple[bool, str]:
    """
    Validate CSV data format.
    
    Args:
        data: List of CSV rows
        expected_columns: Expected number of columns
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not data:
        return False, "CSV file is empty"
    
    for i, row in enumerate(data):
        if len(row) != expected_columns:
            return False, f"Row {i + 1} has {len(row)} columns, expected {expected_columns}"
    
    return True, ""


def get_color_for_price(price: float, threshold: float = 10.0) -> str:
    """
    Get a color name based on price value.
    
    Args:
        price: Price value
        threshold: Price threshold for color determination
        
    Returns:
        str: Color name for display
    """
    if price > threshold * 2:
        return "red"  # Very expensive
    elif price > threshold:
        return "yellow"  # Expensive
    elif price > threshold / 2:
        return "blue"  # Moderate
    else:
        return "green"  # Cheap


def format_time_elapsed(start_time: datetime, end_time: Optional[datetime] = None) -> str:
    """
    Format elapsed time between two datetime objects.
    
    Args:
        start_time: Start datetime
        end_time: End datetime (defaults to now)
        
    Returns:
        str: Formatted elapsed time
    """
    if end_time is None:
        end_time = datetime.now()
    
    elapsed = end_time - start_time
    total_seconds = int(elapsed.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "untitled"
    
    return filename


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted file size
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_weekday_name(date_string: str) -> str:
    """
    Get weekday name for a date.
    
    Args:
        date_string: Date in YYYY-MM-DD format
        
    Returns:
        str: Weekday name
    """
    if not validate_date(date_string):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
    return date_obj.strftime('%A')


def get_month_name(date_string: str) -> str:
    """
    Get month name for a date.
    
    Args:
        date_string: Date in YYYY-MM-DD format
        
    Returns:
        str: Month name
    """
    if not validate_date(date_string):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
    return date_obj.strftime('%B')


def is_weekend(date_string: str) -> bool:
    """
    Check if a date falls on a weekend.
    
    Args:
        date_string: Date in YYYY-MM-DD format
        
    Returns:
        bool: True if weekend, False otherwise
    """
    if not validate_date(date_string):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
    return date_obj.weekday() >= 5  # Saturday = 5, Sunday = 6


def get_quarter(date_string: str) -> int:
    """
    Get quarter number for a date.
    
    Args:
        date_string: Date in YYYY-MM-DD format
        
    Returns:
        int: Quarter number (1-4)
    """
    if not validate_date(date_string):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
    return (date_obj.month - 1) // 3 + 1


# TODO: Add online price scraping (e.g., fetch real prices from a grocery API)
# TODO: Add sort by cost-per-unit feature
# TODO: Add list sharing via JSON export/import
# TODO: Fix bug: total cost sometimes miscalculates when quantity changes
# TODO: Add budget suggestion feature (auto suggest cheaper alternatives)
# TODO: Integrate voice input for adding grocery items
# TODO: Add unit tests for grocery and expense modules
# TODO: Improve Tkinter GUI layout for better UX
