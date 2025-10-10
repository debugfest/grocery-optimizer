"""
Expense tracking and analytics module.

This module handles spending calculations, budget analysis,
and expense optimization features.
"""

import sqlite3
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from utils import format_currency, format_date, get_current_date_string, get_week_start_date, get_month_start_date


@dataclass
class ExpenseSummary:
    """Data class representing expense summary."""
    total_spent: float = 0.0
    total_items: int = 0
    average_item_cost: float = 0.0
    most_expensive_item: str = ""
    most_expensive_cost: float = 0.0
    cheapest_item: str = ""
    cheapest_cost: float = 0.0
    budget_remaining: float = 0.0
    budget_used_percentage: float = 0.0


@dataclass
class CategorySummary:
    """Data class representing category-wise spending summary."""
    category: str = ""
    total_spent: float = 0.0
    item_count: int = 0
    average_cost: float = 0.0
    percentage_of_total: float = 0.0


@dataclass
class StoreSummary:
    """Data class representing store-wise spending summary."""
    store_name: str = ""
    total_spent: float = 0.0
    item_count: int = 0
    average_cost: float = 0.0
    percentage_of_total: float = 0.0


@dataclass
class BudgetAlert:
    """Data class representing budget alert."""
    alert_type: str = ""  # "warning", "exceeded", "suggestion"
    message: str = ""
    amount: float = 0.0
    percentage: float = 0.0


class ExpenseTracker:
    """Manages expense tracking and analytics."""
    
    def __init__(self, db_path: str = "data/grocery_data.db"):
        """Initialize the expense tracker with database path."""
        self.db_path = db_path
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_weekly_spending(self, target_date: str = None) -> float:
        """
        Calculate total spending for a specific week.
        
        Args:
            target_date: Date in YYYY-MM-DD format (defaults to current date)
            
        Returns:
            float: Total spending for the week
        """
        if target_date is None:
            target_date = get_current_date_string()
        
        week_start = get_week_start_date(target_date)
        week_end = (datetime.strptime(week_start, '%Y-%m-%d').date() + timedelta(days=6)).strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT SUM(quantity * price_per_unit) 
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND purchase_date >= ? AND purchase_date <= ?
                """, (week_start, week_end))
                
                result = cursor.fetchone()
                return result[0] if result[0] is not None else 0.0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.0
    
    def get_monthly_spending(self, target_date: str = None) -> float:
        """
        Calculate total spending for a specific month.
        
        Args:
            target_date: Date in YYYY-MM-DD format (defaults to current date)
            
        Returns:
            float: Total spending for the month
        """
        if target_date is None:
            target_date = get_current_date_string()
        
        month_start = get_month_start_date(target_date)
        
        # Calculate month end
        date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
        if date_obj.month == 12:
            month_end = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            month_end = date_obj.replace(month=date_obj.month + 1, day=1)
        month_end = (month_end - timedelta(days=1)).strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT SUM(quantity * price_per_unit) 
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND purchase_date >= ? AND purchase_date <= ?
                """, (month_start, month_end))
                
                result = cursor.fetchone()
                return result[0] if result[0] is not None else 0.0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.0
    
    def get_spending_by_category(self, target_date: str = None) -> List[CategorySummary]:
        """
        Get spending breakdown by category.
        
        Args:
            target_date: Date in YYYY-MM-DD format (defaults to current date)
            
        Returns:
            List[CategorySummary]: Category-wise spending data
        """
        if target_date is None:
            target_date = get_current_date_string()
        
        month_start = get_month_start_date(target_date)
        
        # Calculate month end
        date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
        if date_obj.month == 12:
            month_end = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            month_end = date_obj.replace(month=date_obj.month + 1, day=1)
        month_end = (month_end - timedelta(days=1)).strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT category, 
                           SUM(quantity * price_per_unit) as total_spent,
                           COUNT(*) as item_count,
                           AVG(quantity * price_per_unit) as average_cost
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND purchase_date >= ? AND purchase_date <= ?
                    GROUP BY category
                    ORDER BY total_spent DESC
                """, (month_start, month_end))
                
                rows = cursor.fetchall()
                total_spent = sum(row[1] for row in rows)
                
                category_summaries = []
                for row in rows:
                    category, spent, count, avg_cost = row
                    percentage = (spent / total_spent * 100) if total_spent > 0 else 0
                    
                    summary = CategorySummary(
                        category=category,
                        total_spent=spent,
                        item_count=count,
                        average_cost=avg_cost,
                        percentage_of_total=percentage
                    )
                    category_summaries.append(summary)
                
                return category_summaries
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_spending_by_store(self, target_date: str = None) -> List[StoreSummary]:
        """
        Get spending breakdown by store.
        
        Args:
            target_date: Date in YYYY-MM-DD format (defaults to current date)
            
        Returns:
            List[StoreSummary]: Store-wise spending data
        """
        if target_date is None:
            target_date = get_current_date_string()
        
        month_start = get_month_start_date(target_date)
        
        # Calculate month end
        date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
        if date_obj.month == 12:
            month_end = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            month_end = date_obj.replace(month=date_obj.month + 1, day=1)
        month_end = (month_end - timedelta(days=1)).strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT store_name, 
                           SUM(quantity * price_per_unit) as total_spent,
                           COUNT(*) as item_count,
                           AVG(quantity * price_per_unit) as average_cost
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND purchase_date >= ? AND purchase_date <= ?
                    GROUP BY store_name
                    ORDER BY total_spent DESC
                """, (month_start, month_end))
                
                rows = cursor.fetchall()
                total_spent = sum(row[1] for row in rows)
                
                store_summaries = []
                for row in rows:
                    store_name, spent, count, avg_cost = row
                    percentage = (spent / total_spent * 100) if total_spent > 0 else 0
                    
                    summary = StoreSummary(
                        store_name=store_name,
                        total_spent=spent,
                        item_count=count,
                        average_cost=avg_cost,
                        percentage_of_total=percentage
                    )
                    store_summaries.append(summary)
                
                return store_summaries
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_expense_summary(self, target_date: str = None) -> ExpenseSummary:
        """
        Get comprehensive expense summary.
        
        Args:
            target_date: Date in YYYY-MM-DD format (defaults to current date)
            
        Returns:
            ExpenseSummary: Comprehensive expense data
        """
        if target_date is None:
            target_date = get_current_date_string()
        
        month_start = get_month_start_date(target_date)
        
        # Calculate month end
        date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
        if date_obj.month == 12:
            month_end = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            month_end = date_obj.replace(month=date_obj.month + 1, day=1)
        month_end = (month_end - timedelta(days=1)).strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get basic stats
                cursor.execute("""
                    SELECT 
                        SUM(quantity * price_per_unit) as total_spent,
                        COUNT(*) as item_count,
                        AVG(quantity * price_per_unit) as average_cost,
                        MAX(quantity * price_per_unit) as max_cost,
                        MIN(quantity * price_per_unit) as min_cost
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND purchase_date >= ? AND purchase_date <= ?
                """, (month_start, month_end))
                
                basic_stats = cursor.fetchone()
                
                # Get most expensive item
                cursor.execute("""
                    SELECT name, (quantity * price_per_unit) as total_cost
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND purchase_date >= ? AND purchase_date <= ?
                    ORDER BY total_cost DESC
                    LIMIT 1
                """, (month_start, month_end))
                
                most_expensive = cursor.fetchone()
                
                # Get cheapest item
                cursor.execute("""
                    SELECT name, (quantity * price_per_unit) as total_cost
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND purchase_date >= ? AND purchase_date <= ?
                    ORDER BY total_cost ASC
                    LIMIT 1
                """, (month_start, month_end))
                
                cheapest = cursor.fetchone()
                
                # Get monthly budget
                cursor.execute("SELECT monthly_budget FROM budget_settings WHERE id = 1")
                budget_row = cursor.fetchone()
                monthly_budget = budget_row[0] if budget_row else 0.0
                
                total_spent = basic_stats[0] if basic_stats[0] is not None else 0.0
                item_count = basic_stats[1] if basic_stats[1] is not None else 0
                average_cost = basic_stats[2] if basic_stats[2] is not None else 0.0
                max_cost = basic_stats[3] if basic_stats[3] is not None else 0.0
                min_cost = basic_stats[4] if basic_stats[4] is not None else 0.0
                
                budget_remaining = monthly_budget - total_spent
                budget_used_percentage = (total_spent / monthly_budget * 100) if monthly_budget > 0 else 0
                
                return ExpenseSummary(
                    total_spent=total_spent,
                    total_items=item_count,
                    average_item_cost=average_cost,
                    most_expensive_item=most_expensive[0] if most_expensive else "",
                    most_expensive_cost=most_expensive[1] if most_expensive else 0.0,
                    cheapest_item=cheapest[0] if cheapest else "",
                    cheapest_cost=cheapest[1] if cheapest else 0.0,
                    budget_remaining=budget_remaining,
                    budget_used_percentage=budget_used_percentage
                )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return ExpenseSummary()
    
    def get_budget_alerts(self, target_date: str = None) -> List[BudgetAlert]:
        """
        Get budget alerts and suggestions.
        
        Args:
            target_date: Date in YYYY-MM-DD format (defaults to current date)
            
        Returns:
            List[BudgetAlert]: List of budget alerts
        """
        alerts = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get monthly budget and spending
                cursor.execute("SELECT monthly_budget FROM budget_settings WHERE id = 1")
                budget_row = cursor.fetchone()
                monthly_budget = budget_row[0] if budget_row else 0.0
                
                if monthly_budget > 0:
                    monthly_spending = self.get_monthly_spending(target_date)
                    budget_used_percentage = (monthly_spending / monthly_budget * 100)
                    
                    if budget_used_percentage >= 100:
                        alerts.append(BudgetAlert(
                            alert_type="exceeded",
                            message=f"Monthly budget exceeded by {format_currency(monthly_spending - monthly_budget)}",
                            amount=monthly_spending - monthly_budget,
                            percentage=budget_used_percentage
                        ))
                    elif budget_used_percentage >= 80:
                        alerts.append(BudgetAlert(
                            alert_type="warning",
                            message=f"Monthly budget {budget_used_percentage:.1f}% used. Consider reducing spending.",
                            amount=monthly_spending,
                            percentage=budget_used_percentage
                        ))
                    
                    # Weekly budget check
                    cursor.execute("SELECT weekly_budget FROM budget_settings WHERE id = 1")
                    weekly_budget_row = cursor.fetchone()
                    weekly_budget = weekly_budget_row[0] if weekly_budget_row else 0.0
                    
                    if weekly_budget > 0:
                        weekly_spending = self.get_weekly_spending(target_date)
                        weekly_used_percentage = (weekly_spending / weekly_budget * 100)
                        
                        if weekly_used_percentage >= 100:
                            alerts.append(BudgetAlert(
                                alert_type="exceeded",
                                message=f"Weekly budget exceeded by {format_currency(weekly_spending - weekly_budget)}",
                                amount=weekly_spending - weekly_budget,
                                percentage=weekly_used_percentage
                            ))
                        elif weekly_used_percentage >= 80:
                            alerts.append(BudgetAlert(
                                alert_type="warning",
                                message=f"Weekly budget {weekly_used_percentage:.1f}% used.",
                                amount=weekly_spending,
                                percentage=weekly_used_percentage
                            ))
                
                # Get expensive items suggestion
                cursor.execute("""
                    SELECT name, price_per_unit, category
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND price_per_unit > 10.0
                    ORDER BY price_per_unit DESC
                    LIMIT 3
                """)
                
                expensive_items = cursor.fetchall()
                if expensive_items:
                    suggestions = []
                    for item in expensive_items:
                        suggestions.append(f"{item[0]} (${item[1]:.2f}/{item[2]})")
                    
                    alerts.append(BudgetAlert(
                        alert_type="suggestion",
                        message=f"Consider cheaper alternatives for: {', '.join(suggestions)}",
                        amount=0.0,
                        percentage=0.0
                    ))
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return alerts
    
    def get_spending_trend(self, days: int = 30) -> List[Dict[str, any]]:
        """
        Get spending trend over the last N days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            List[Dict]: Daily spending data
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        trend_data = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for i in range(days):
                    current_date = start_date + timedelta(days=i)
                    date_str = current_date.strftime('%Y-%m-%d')
                    
                    cursor.execute("""
                        SELECT SUM(quantity * price_per_unit) 
                        FROM grocery_items 
                        WHERE is_purchased = TRUE 
                        AND purchase_date = ?
                    """, (date_str,))
                    
                    result = cursor.fetchone()
                    daily_spending = result[0] if result[0] is not None else 0.0
                    
                    trend_data.append({
                        'date': date_str,
                        'spending': daily_spending,
                        'day_of_week': current_date.strftime('%A')
                    })
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return trend_data
    
    def get_cost_optimization_suggestions(self) -> List[Dict[str, any]]:
        """
        Get suggestions for cost optimization.
        
        Returns:
            List[Dict]: Optimization suggestions
        """
        suggestions = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Find items with high price per unit
                cursor.execute("""
                    SELECT name, price_per_unit, category, store_name
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    AND price_per_unit > (
                        SELECT AVG(price_per_unit) * 1.5 
                        FROM grocery_items 
                        WHERE is_purchased = TRUE
                    )
                    ORDER BY price_per_unit DESC
                    LIMIT 5
                """)
                
                expensive_items = cursor.fetchall()
                for item in expensive_items:
                    suggestions.append({
                        'type': 'expensive_item',
                        'item': item[0],
                        'price': item[1],
                        'category': item[2],
                        'store': item[3],
                        'suggestion': f"Consider buying {item[0]} from a different store or look for sales"
                    })
                
                # Find categories with high spending
                cursor.execute("""
                    SELECT category, SUM(quantity * price_per_unit) as total_spent
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    GROUP BY category
                    HAVING total_spent > (
                        SELECT AVG(category_total) * 1.2 
                        FROM (
                            SELECT SUM(quantity * price_per_unit) as category_total
                            FROM grocery_items 
                            WHERE is_purchased = TRUE 
                            GROUP BY category
                        )
                    )
                    ORDER BY total_spent DESC
                """)
                
                high_spending_categories = cursor.fetchall()
                for category in high_spending_categories:
                    suggestions.append({
                        'type': 'high_spending_category',
                        'category': category[0],
                        'total_spent': category[1],
                        'suggestion': f"Consider reducing spending in {category[0]} category or look for bulk discounts"
                    })
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return suggestions
    
    def get_store_comparison(self) -> List[Dict[str, any]]:
        """
        Compare prices across different stores.
        
        Returns:
            List[Dict]: Store comparison data
        """
        comparisons = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get items available in multiple stores
                cursor.execute("""
                    SELECT name, category, 
                           GROUP_CONCAT(store_name || ':' || price_per_unit) as store_prices
                    FROM grocery_items 
                    WHERE is_purchased = TRUE 
                    GROUP BY name, category
                    HAVING COUNT(DISTINCT store_name) > 1
                    ORDER BY name
                """)
                
                multi_store_items = cursor.fetchall()
                
                for item in multi_store_items:
                    name, category, store_prices_str = item
                    store_prices = []
                    
                    for store_price in store_prices_str.split(','):
                        store, price = store_price.split(':')
                        store_prices.append((store, float(price)))
                    
                    if len(store_prices) > 1:
                        store_prices.sort(key=lambda x: x[1])  # Sort by price
                        cheapest_store, cheapest_price = store_prices[0]
                        most_expensive_store, most_expensive_price = store_prices[-1]
                        
                        savings = most_expensive_price - cheapest_price
                        savings_percentage = (savings / most_expensive_price * 100) if most_expensive_price > 0 else 0
                        
                        comparisons.append({
                            'item': name,
                            'category': category,
                            'cheapest_store': cheapest_store,
                            'cheapest_price': cheapest_price,
                            'most_expensive_store': most_expensive_store,
                            'most_expensive_price': most_expensive_price,
                            'potential_savings': savings,
                            'savings_percentage': savings_percentage
                        })
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return comparisons


# TODO: Add online price scraping (e.g., fetch real prices from a grocery API)
# TODO: Add sort by cost-per-unit feature
# TODO: Add list sharing via JSON export/import
# TODO: Fix bug: total cost sometimes miscalculates when quantity changes
# TODO: Add budget suggestion feature (auto suggest cheaper alternatives)
# TODO: Integrate voice input for adding grocery items
# TODO: Add unit tests for grocery and expense modules
# TODO: Improve Tkinter GUI layout for better UX
