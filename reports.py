"""
Report generation module for grocery optimizer.

This module handles generating various reports including summaries,
analytics, and visualizations using matplotlib.
"""

import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from grocery import GroceryManager, GroceryItem
from expense import ExpenseTracker, ExpenseSummary, CategorySummary, StoreSummary, BudgetAlert
from utils import format_currency, format_date, format_percentage, get_current_date_string


class ReportGenerator:
    """Generates various reports and visualizations for grocery tracking."""
    
    def __init__(self, grocery_manager: GroceryManager, expense_tracker: ExpenseTracker):
        """
        Initialize the report generator.
        
        Args:
            grocery_manager: GroceryManager instance
            expense_tracker: ExpenseTracker instance
        """
        self.grocery_manager = grocery_manager
        self.expense_tracker = expense_tracker
        self._ensure_reports_directory()
    
    def _ensure_reports_directory(self) -> None:
        """Ensure the reports directory exists."""
        os.makedirs("reports", exist_ok=True)
    
    def generate_grocery_summary(self, save_to_file: bool = True) -> str:
        """
        Generate a comprehensive grocery summary report.
        
        Args:
            save_to_file: Whether to save the report to a file
            
        Returns:
            str: Generated report content
        """
        all_items = self.grocery_manager.get_all_items()
        purchased_items = self.grocery_manager.get_purchased_items()
        unpurchased_items = self.grocery_manager.get_unpurchased_items()
        
        expense_summary = self.expense_tracker.get_expense_summary()
        budget_alerts = self.expense_tracker.get_budget_alerts()
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("GROCERY LIST & EXPENSE SUMMARY")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        report_lines.append("")
        
        # Overall summary
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Total Items: {len(all_items)}")
        report_lines.append(f"Purchased Items: {len(purchased_items)}")
        report_lines.append(f"Unpurchased Items: {len(unpurchased_items)}")
        report_lines.append(f"Total Cost: {format_currency(expense_summary.total_spent)}")
        report_lines.append(f"Average Item Cost: {format_currency(expense_summary.average_item_cost)}")
        report_lines.append("")
        
        # Budget information
        weekly_budget = self.grocery_manager.get_weekly_budget()
        monthly_budget = self.grocery_manager.get_monthly_budget()
        
        if weekly_budget > 0 or monthly_budget > 0:
            report_lines.append("BUDGET INFORMATION")
            report_lines.append("-" * 20)
            if weekly_budget > 0:
                weekly_spending = self.expense_tracker.get_weekly_spending()
                weekly_remaining = weekly_budget - weekly_spending
                weekly_percentage = (weekly_spending / weekly_budget * 100) if weekly_budget > 0 else 0
                report_lines.append(f"Weekly Budget: {format_currency(weekly_budget)}")
                report_lines.append(f"Weekly Spending: {format_currency(weekly_spending)} ({weekly_percentage:.1f}%)")
                report_lines.append(f"Weekly Remaining: {format_currency(weekly_remaining)}")
            
            if monthly_budget > 0:
                monthly_spending = self.expense_tracker.get_monthly_spending()
                monthly_remaining = monthly_budget - monthly_spending
                monthly_percentage = (monthly_spending / monthly_budget * 100) if monthly_budget > 0 else 0
                report_lines.append(f"Monthly Budget: {format_currency(monthly_budget)}")
                report_lines.append(f"Monthly Spending: {format_currency(monthly_spending)} ({monthly_percentage:.1f}%)")
                report_lines.append(f"Monthly Remaining: {format_currency(monthly_remaining)}")
            report_lines.append("")
        
        # Budget alerts
        if budget_alerts:
            report_lines.append("BUDGET ALERTS")
            report_lines.append("-" * 15)
            for alert in budget_alerts:
                if alert.alert_type == "exceeded":
                    report_lines.append(f"🔴 {alert.message}")
                elif alert.alert_type == "warning":
                    report_lines.append(f"🟡 {alert.message}")
                elif alert.alert_type == "suggestion":
                    report_lines.append(f"💡 {alert.message}")
            report_lines.append("")
        
        # Category breakdown
        category_summaries = self.expense_tracker.get_spending_by_category()
        if category_summaries:
            report_lines.append("SPENDING BY CATEGORY")
            report_lines.append("-" * 25)
            for category in category_summaries:
                report_lines.append(f"{category.category}: {format_currency(category.total_spent)} "
                                  f"({category.item_count} items, {category.percentage_of_total:.1f}%)")
            report_lines.append("")
        
        # Store breakdown
        store_summaries = self.expense_tracker.get_spending_by_store()
        if store_summaries:
            report_lines.append("SPENDING BY STORE")
            report_lines.append("-" * 20)
            for store in store_summaries:
                report_lines.append(f"{store.store_name}: {format_currency(store.total_spent)} "
                                  f"({store.item_count} items, {store.percentage_of_total:.1f}%)")
            report_lines.append("")
        
        # Most expensive items
        if expense_summary.most_expensive_item:
            report_lines.append("MOST EXPENSIVE ITEM")
            report_lines.append("-" * 25)
            report_lines.append(f"{expense_summary.most_expensive_item}: "
                              f"{format_currency(expense_summary.most_expensive_cost)}")
            report_lines.append("")
        
        # Cheapest items
        if expense_summary.cheapest_item:
            report_lines.append("CHEAPEST ITEM")
            report_lines.append("-" * 15)
            report_lines.append(f"{expense_summary.cheapest_item}: "
                              f"{format_currency(expense_summary.cheapest_cost)}")
            report_lines.append("")
        
        # Unpurchased items
        if unpurchased_items:
            report_lines.append("UNPURCHASED ITEMS")
            report_lines.append("-" * 20)
            unpurchased_total = sum(item.total_cost for item in unpurchased_items)
            report_lines.append(f"Total Unpurchased Cost: {format_currency(unpurchased_total)}")
            report_lines.append("Items:")
            for item in unpurchased_items[:10]:  # Show first 10 items
                report_lines.append(f"  • {item.name} - {format_currency(item.total_cost)}")
            if len(unpurchased_items) > 10:
                report_lines.append(f"  ... and {len(unpurchased_items) - 10} more items")
        
        report_content = "\n".join(report_lines)
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/grocery_summary_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write(report_content)
            print(f"Grocery summary saved to: {filename}")
        
        return report_content
    
    def generate_spending_by_category_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a pie chart showing spending by category.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        category_summaries = self.expense_tracker.get_spending_by_category()
        
        if not category_summaries:
            print("No spending data available for chart generation.")
            return None
        
        # Prepare data
        categories = [cat.category for cat in category_summaries]
        amounts = [cat.total_spent for cat in category_summaries]
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        
        wedges, texts, autotexts = plt.pie(
            amounts,
            labels=categories,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Customize the chart
        plt.title('Spending by Category', fontsize=16, fontweight='bold')
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/spending_by_category_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Spending by category chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_spending_by_store_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a bar chart showing spending by store.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        store_summaries = self.expense_tracker.get_spending_by_store()
        
        if not store_summaries:
            print("No store data available for chart generation.")
            return None
        
        # Prepare data
        stores = [store.store_name for store in store_summaries]
        amounts = [store.total_spent for store in store_summaries]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(stores, amounts, color='skyblue', alpha=0.7)
        
        # Customize the chart
        plt.title('Spending by Store', fontsize=16, fontweight='bold')
        plt.xlabel('Store')
        plt.ylabel('Amount Spent')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, amount in zip(bars, amounts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + amount*0.01,
                    f'{amount:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/spending_by_store_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Spending by store chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_price_distribution_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a histogram showing price distribution.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        purchased_items = self.grocery_manager.get_purchased_items()
        
        if not purchased_items:
            print("No purchased items available for chart generation.")
            return None
        
        # Prepare data
        prices = [item.price_per_unit for item in purchased_items]
        
        # Create histogram
        plt.figure(figsize=(10, 6))
        plt.hist(prices, bins=20, color='lightgreen', alpha=0.7, edgecolor='black')
        
        # Customize the chart
        plt.title('Price Distribution (Per Unit)', fontsize=16, fontweight='bold')
        plt.xlabel('Price per Unit')
        plt.ylabel('Number of Items')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add statistics
        mean_price = np.mean(prices)
        median_price = np.median(prices)
        plt.axvline(mean_price, color='red', linestyle='--', label=f'Mean: ${mean_price:.2f}')
        plt.axvline(median_price, color='blue', linestyle='--', label=f'Median: ${median_price:.2f}')
        plt.legend()
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/price_distribution_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Price distribution chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_spending_trend_chart(self, days: int = 30, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a line chart showing spending trend over time.
        
        Args:
            days: Number of days to show
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        trend_data = self.expense_tracker.get_spending_trend(days)
        
        if not trend_data:
            print("No trend data available for chart generation.")
            return None
        
        # Prepare data
        dates = [datetime.strptime(item['date'], '%Y-%m-%d').date() for item in trend_data]
        spending = [item['spending'] for item in trend_data]
        
        # Create line chart
        plt.figure(figsize=(12, 6))
        plt.plot(dates, spending, marker='o', linewidth=2, markersize=4, color='blue')
        
        # Customize the chart
        plt.title(f'Daily Spending Trend - Last {days} Days', fontsize=16, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Amount Spent')
        plt.grid(True, alpha=0.3)
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
        plt.xticks(rotation=45)
        
        # Add trend line
        if len(spending) > 1:
            z = np.polyfit(range(len(spending)), spending, 1)
            p = np.poly1d(z)
            plt.plot(dates, p(range(len(spending))), "r--", alpha=0.8, label='Trend')
            plt.legend()
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/spending_trend_{days}days_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Spending trend chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_budget_vs_actual_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a chart comparing budget vs actual spending.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        weekly_budget = self.grocery_manager.get_weekly_budget()
        monthly_budget = self.grocery_manager.get_monthly_budget()
        
        if weekly_budget == 0 and monthly_budget == 0:
            print("No budget data available for chart generation.")
            return None
        
        # Prepare data
        categories = []
        budgets = []
        actuals = []
        
        if weekly_budget > 0:
            categories.append('Weekly')
            budgets.append(weekly_budget)
            actuals.append(self.expense_tracker.get_weekly_spending())
        
        if monthly_budget > 0:
            categories.append('Monthly')
            budgets.append(monthly_budget)
            actuals.append(self.expense_tracker.get_monthly_spending())
        
        # Create bar chart
        x = np.arange(len(categories))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x - width/2, budgets, width, label='Budget', color='lightblue', alpha=0.7)
        bars2 = ax.bar(x + width/2, actuals, width, label='Actual', color='lightcoral', alpha=0.7)
        
        # Customize the chart
        ax.set_xlabel('Budget Period')
        ax.set_ylabel('Amount')
        ax.set_title('Budget vs Actual Spending')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, amount in zip(bars1, budgets):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + amount*0.01,
                   f'{amount:,.0f}', ha='center', va='bottom', fontsize=10)
        
        for bar, amount in zip(bars2, actuals):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + amount*0.01,
                   f'{amount:,.0f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/budget_vs_actual_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Budget vs actual chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_store_comparison_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a chart comparing prices across stores.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        comparisons = self.expense_tracker.get_store_comparison()
        
        if not comparisons:
            print("No store comparison data available for chart generation.")
            return None
        
        # Take top 10 items with highest savings potential
        top_comparisons = sorted(comparisons, key=lambda x: x['potential_savings'], reverse=True)[:10]
        
        if not top_comparisons:
            print("No significant savings found in store comparisons.")
            return None
        
        # Prepare data
        items = [comp['item'] for comp in top_comparisons]
        cheapest_prices = [comp['cheapest_price'] for comp in top_comparisons]
        most_expensive_prices = [comp['most_expensive_price'] for comp in top_comparisons]
        savings = [comp['potential_savings'] for comp in top_comparisons]
        
        # Create grouped bar chart
        x = np.arange(len(items))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars1 = ax.bar(x - width/2, cheapest_prices, width, label='Cheapest Store', color='green', alpha=0.7)
        bars2 = ax.bar(x + width/2, most_expensive_prices, width, label='Most Expensive Store', color='red', alpha=0.7)
        
        # Customize the chart
        ax.set_xlabel('Items')
        ax.set_ylabel('Price per Unit')
        ax.set_title('Store Price Comparison (Top 10 Items with Highest Savings Potential)')
        ax.set_xticks(x)
        ax.set_xticklabels(items, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add savings annotations
        for i, (bar1, bar2, saving) in enumerate(zip(bars1, bars2, savings)):
            ax.annotate(f'${saving:.2f}', 
                       xy=(i, max(bar1.get_height(), bar2.get_height())),
                       xytext=(0, 10), textcoords='offset points',
                       ha='center', va='bottom', fontweight='bold', color='blue')
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/store_comparison_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Store comparison chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_comprehensive_report(self, save_to_file: bool = True) -> str:
        """
        Generate a comprehensive report with all available data and charts.
        
        Args:
            save_to_file: Whether to save the report and charts to files
            
        Returns:
            str: Generated report content
        """
        print("Generating comprehensive grocery report...")
        
        # Generate text report
        grocery_report = self.generate_grocery_summary(save_to_file)
        
        # Generate charts
        if save_to_file:
            print("Generating charts...")
            self.generate_spending_by_category_chart(save_to_file=True)
            self.generate_spending_by_store_chart(save_to_file=True)
            self.generate_price_distribution_chart(save_to_file=True)
            self.generate_spending_trend_chart(save_to_file=True)
            self.generate_budget_vs_actual_chart(save_to_file=True)
            self.generate_store_comparison_chart(save_to_file=True)
        
        # Add optimization suggestions
        suggestions = self.expense_tracker.get_cost_optimization_suggestions()
        if suggestions:
            print("Generating optimization suggestions...")
            suggestions_content = []
            suggestions_content.append("\n" + "=" * 60)
            suggestions_content.append("COST OPTIMIZATION SUGGESTIONS")
            suggestions_content.append("=" * 60)
            
            for suggestion in suggestions:
                if suggestion['type'] == 'expensive_item':
                    suggestions_content.append(f"💡 {suggestion['suggestion']}")
                elif suggestion['type'] == 'high_spending_category':
                    suggestions_content.append(f"📊 {suggestion['suggestion']}")
            
            suggestions_text = "\n".join(suggestions_content)
            
            if save_to_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reports/optimization_suggestions_{timestamp}.txt"
                with open(filename, 'w') as f:
                    f.write(suggestions_text)
                print(f"Optimization suggestions saved to: {filename}")
        
        return grocery_report


# TODO: Add online price scraping (e.g., fetch real prices from a grocery API)
# TODO: Add sort by cost-per-unit feature
# TODO: Add list sharing via JSON export/import
# TODO: Fix bug: total cost sometimes miscalculates when quantity changes
# TODO: Add budget suggestion feature (auto suggest cheaper alternatives)
# TODO: Integrate voice input for adding grocery items
# TODO: Add unit tests for grocery and expense modules
# TODO: Improve Tkinter GUI layout for better UX
