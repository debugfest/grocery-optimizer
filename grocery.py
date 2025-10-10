"""
Grocery item management module.

This module handles all grocery item operations including
CRUD operations, data validation, and item categorization.
"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from utils import validate_price, validate_quantity, validate_date, format_currency, get_current_date_string


@dataclass
class GroceryItem:
    """Data class representing a grocery item."""
    id: Optional[int] = None
    name: str = ""
    category: str = ""
    quantity: float = 0.0
    unit: str = ""
    price_per_unit: float = 0.0
    store_name: str = ""
    is_purchased: bool = False
    purchase_date: str = ""
    notes: str = ""

    def __post_init__(self):
        """Validate data after initialization."""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price_per_unit < 0:
            raise ValueError("Price per unit cannot be negative")
        if not self.name.strip():
            raise ValueError("Item name cannot be empty")
        if not self.category.strip():
            raise ValueError("Category cannot be empty")
        if not self.unit.strip():
            raise ValueError("Unit cannot be empty")
        if not self.store_name.strip():
            raise ValueError("Store name cannot be empty")

    @property
    def total_cost(self) -> float:
        """Calculate total cost for this item."""
        return self.quantity * self.price_per_unit

    @property
    def cost_per_unit_display(self) -> str:
        """Get formatted cost per unit string."""
        return f"{format_currency(self.price_per_unit)}/{self.unit}"

    @property
    def total_cost_display(self) -> str:
        """Get formatted total cost string."""
        return format_currency(self.total_cost)


class GroceryManager:
    """Manages grocery items and database operations."""
    
    def __init__(self, db_path: str = "data/grocery_data.db"):
        """Initialize the grocery manager with database path."""
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Grocery items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grocery_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    unit TEXT NOT NULL,
                    price_per_unit REAL NOT NULL,
                    store_name TEXT NOT NULL,
                    is_purchased BOOLEAN DEFAULT FALSE,
                    purchase_date TEXT DEFAULT '',
                    notes TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Budget settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budget_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    weekly_budget REAL DEFAULT 0.0,
                    monthly_budget REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    # CRUD operations for grocery items
    def add_item(self, item: GroceryItem) -> int:
        """
        Add a new grocery item to the database.
        
        Args:
            item: GroceryItem object to add
            
        Returns:
            int: ID of the created item
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO grocery_items 
                    (name, category, quantity, unit, price_per_unit, store_name, 
                     is_purchased, purchase_date, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.name,
                    item.category,
                    item.quantity,
                    item.unit,
                    item.price_per_unit,
                    item.store_name,
                    item.is_purchased,
                    item.purchase_date,
                    item.notes
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")
    
    def get_all_items(self) -> List[GroceryItem]:
        """Get all grocery items."""
        items = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM grocery_items ORDER BY created_at DESC")
                rows = cursor.fetchall()
                
                for row in rows:
                    item = GroceryItem(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        quantity=row[3],
                        unit=row[4],
                        price_per_unit=row[5],
                        store_name=row[6],
                        is_purchased=bool(row[7]),
                        purchase_date=row[8] or "",
                        notes=row[9] or ""
                    )
                    items.append(item)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return items
    
    def get_item_by_id(self, item_id: int) -> Optional[GroceryItem]:
        """Get a specific item by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM grocery_items WHERE id = ?", (item_id,))
                row = cursor.fetchone()
                
                if row:
                    return GroceryItem(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        quantity=row[3],
                        unit=row[4],
                        price_per_unit=row[5],
                        store_name=row[6],
                        is_purchased=bool(row[7]),
                        purchase_date=row[8] or "",
                        notes=row[9] or ""
                    )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return None
    
    def update_item(self, item: GroceryItem) -> bool:
        """
        Update an existing grocery item.
        
        Args:
            item: GroceryItem object with updated data
            
        Returns:
            bool: True if update was successful
        """
        if not item.id:
            raise ValueError("Item ID is required for update")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE grocery_items 
                    SET name = ?, category = ?, quantity = ?, unit = ?, 
                        price_per_unit = ?, store_name = ?, is_purchased = ?, 
                        purchase_date = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    item.name,
                    item.category,
                    item.quantity,
                    item.unit,
                    item.price_per_unit,
                    item.store_name,
                    item.is_purchased,
                    item.purchase_date,
                    item.notes,
                    item.id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def delete_item(self, item_id: int) -> bool:
        """Delete a grocery item by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM grocery_items WHERE id = ?", (item_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def mark_as_purchased(self, item_id: int, purchase_date: str = None) -> bool:
        """
        Mark an item as purchased.
        
        Args:
            item_id: ID of the item to mark as purchased
            purchase_date: Date of purchase (defaults to current date)
            
        Returns:
            bool: True if successful
        """
        if purchase_date is None:
            purchase_date = get_current_date_string()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE grocery_items 
                    SET is_purchased = TRUE, purchase_date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (purchase_date, item_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def mark_as_unpurchased(self, item_id: int) -> bool:
        """Mark an item as not purchased."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE grocery_items 
                    SET is_purchased = FALSE, purchase_date = '', updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (item_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    # Query methods
    def get_items_by_category(self, category: str) -> List[GroceryItem]:
        """Get all items in a specific category."""
        items = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM grocery_items WHERE category = ? ORDER BY name", (category,))
                rows = cursor.fetchall()
                
                for row in rows:
                    item = GroceryItem(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        quantity=row[3],
                        unit=row[4],
                        price_per_unit=row[5],
                        store_name=row[6],
                        is_purchased=bool(row[7]),
                        purchase_date=row[8] or "",
                        notes=row[9] or ""
                    )
                    items.append(item)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return items
    
    def get_items_by_store(self, store_name: str) -> List[GroceryItem]:
        """Get all items from a specific store."""
        items = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM grocery_items WHERE store_name = ? ORDER BY name", (store_name,))
                rows = cursor.fetchall()
                
                for row in rows:
                    item = GroceryItem(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        quantity=row[3],
                        unit=row[4],
                        price_per_unit=row[5],
                        store_name=row[6],
                        is_purchased=bool(row[7]),
                        purchase_date=row[8] or "",
                        notes=row[9] or ""
                    )
                    items.append(item)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return items
    
    def get_purchased_items(self) -> List[GroceryItem]:
        """Get all purchased items."""
        all_items = self.get_all_items()
        return [item for item in all_items if item.is_purchased]
    
    def get_unpurchased_items(self) -> List[GroceryItem]:
        """Get all unpurchased items."""
        all_items = self.get_all_items()
        return [item for item in all_items if not item.is_purchased]
    
    def search_items(self, query: str) -> List[GroceryItem]:
        """Search items by name, category, or store."""
        query_lower = query.lower()
        matching_items = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM grocery_items 
                    WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(store_name) LIKE ?
                    ORDER BY name
                """, (f"%{query_lower}%", f"%{query_lower}%", f"%{query_lower}%"))
                rows = cursor.fetchall()
                
                for row in rows:
                    item = GroceryItem(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        quantity=row[3],
                        unit=row[4],
                        price_per_unit=row[5],
                        store_name=row[6],
                        is_purchased=bool(row[7]),
                        purchase_date=row[8] or "",
                        notes=row[9] or ""
                    )
                    matching_items.append(item)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return matching_items
    
    def get_items_by_price_range(self, min_price: float, max_price: float) -> List[GroceryItem]:
        """Get items within a specific price range."""
        all_items = self.get_all_items()
        return [item for item in all_items if min_price <= item.price_per_unit <= max_price]
    
    def get_expensive_items(self, threshold: float = 10.0) -> List[GroceryItem]:
        """Get items above a price threshold."""
        all_items = self.get_all_items()
        return [item for item in all_items if item.price_per_unit > threshold]
    
    def get_budget_friendly_items(self, threshold: float = 5.0) -> List[GroceryItem]:
        """Get items below a price threshold."""
        all_items = self.get_all_items()
        return [item for item in all_items if item.price_per_unit <= threshold]
    
    # Sorting methods
    def sort_items_by_price(self, ascending: bool = True) -> List[GroceryItem]:
        """Sort items by price per unit."""
        items = self.get_all_items()
        return sorted(items, key=lambda x: x.price_per_unit, reverse=not ascending)
    
    def sort_items_by_total_cost(self, ascending: bool = True) -> List[GroceryItem]:
        """Sort items by total cost."""
        items = self.get_all_items()
        return sorted(items, key=lambda x: x.total_cost, reverse=not ascending)
    
    def sort_items_by_category(self) -> List[GroceryItem]:
        """Sort items by category."""
        items = self.get_all_items()
        return sorted(items, key=lambda x: (x.category, x.name))
    
    def sort_items_by_name(self) -> List[GroceryItem]:
        """Sort items by name."""
        items = self.get_all_items()
        return sorted(items, key=lambda x: x.name.lower())
    
    def sort_items_by_store(self) -> List[GroceryItem]:
        """Sort items by store name."""
        items = self.get_all_items()
        return sorted(items, key=lambda x: (x.store_name, x.name))
    
    # Budget management
    def set_weekly_budget(self, budget: float) -> bool:
        """Set weekly budget limit."""
        if budget < 0:
            raise ValueError("Budget cannot be negative")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO budget_settings (id, weekly_budget, updated_at)
                    VALUES (1, ?, CURRENT_TIMESTAMP)
                """, (budget,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def set_monthly_budget(self, budget: float) -> bool:
        """Set monthly budget limit."""
        if budget < 0:
            raise ValueError("Budget cannot be negative")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO budget_settings (id, monthly_budget, updated_at)
                    VALUES (1, ?, CURRENT_TIMESTAMP)
                """, (budget,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_weekly_budget(self) -> float:
        """Get current weekly budget."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT weekly_budget FROM budget_settings WHERE id = 1")
                row = cursor.fetchone()
                return row[0] if row else 0.0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.0
    
    def get_monthly_budget(self) -> float:
        """Get current monthly budget."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT monthly_budget FROM budget_settings WHERE id = 1")
                row = cursor.fetchone()
                return row[0] if row else 0.0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.0
    
    # Statistics methods
    def get_total_items_count(self) -> int:
        """Get total number of items."""
        return len(self.get_all_items())
    
    def get_purchased_items_count(self) -> int:
        """Get number of purchased items."""
        return len(self.get_purchased_items())
    
    def get_unpurchased_items_count(self) -> int:
        """Get number of unpurchased items."""
        return len(self.get_unpurchased_items())
    
    def get_categories(self) -> List[str]:
        """Get list of all categories."""
        all_items = self.get_all_items()
        categories = set(item.category for item in all_items)
        return sorted(list(categories))
    
    def get_stores(self) -> List[str]:
        """Get list of all stores."""
        all_items = self.get_all_items()
        stores = set(item.store_name for item in all_items)
        return sorted(list(stores))
    
    def get_total_cost(self) -> float:
        """Get total cost of all items."""
        all_items = self.get_all_items()
        return sum(item.total_cost for item in all_items)
    
    def get_purchased_total_cost(self) -> float:
        """Get total cost of purchased items."""
        purchased_items = self.get_purchased_items()
        return sum(item.total_cost for item in purchased_items)
    
    def get_unpurchased_total_cost(self) -> float:
        """Get total cost of unpurchased items."""
        unpurchased_items = self.get_unpurchased_items()
        return sum(item.total_cost for item in unpurchased_items)


# TODO: Add online price scraping (e.g., fetch real prices from a grocery API)
# TODO: Add sort by cost-per-unit feature
# TODO: Add list sharing via JSON export/import
# TODO: Fix bug: total cost sometimes miscalculates when quantity changes
# TODO: Add budget suggestion feature (auto suggest cheaper alternatives)
# TODO: Integrate voice input for adding grocery items
# TODO: Add unit tests for grocery and expense modules
# TODO: Improve Tkinter GUI layout for better UX
