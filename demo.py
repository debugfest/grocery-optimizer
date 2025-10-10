#!/usr/bin/env python3
"""
Demo script for Grocery Optimizer.

This script demonstrates the functionality of the grocery optimizer
by adding some sample data and generating reports.
"""

from grocery import GroceryManager, GroceryItem
from expense import ExpenseTracker
from reports import ReportGenerator
from utils import get_current_date_string
from datetime import date, timedelta


def create_sample_data():
    """Create sample grocery data for demonstration."""
    grocery_manager = GroceryManager()
    expense_tracker = ExpenseTracker()
    
    # Sample grocery items
    sample_items = [
        GroceryItem(
            name="Organic Apples",
            category="Fruits & Vegetables",
            quantity=2.0,
            unit="kg",
            price_per_unit=4.50,
            store_name="Whole Foods",
            is_purchased=True,
            purchase_date="2024-01-15",
            notes="Red delicious apples"
        ),
        GroceryItem(
            name="Whole Milk",
            category="Dairy & Eggs",
            quantity=1.0,
            unit="gallon",
            price_per_unit=3.50,
            store_name="Walmart",
            is_purchased=True,
            purchase_date="2024-01-15",
            notes="Organic whole milk"
        ),
        GroceryItem(
            name="Chicken Breast",
            category="Meat & Seafood",
            quantity=1.5,
            unit="kg",
            price_per_unit=8.99,
            store_name="Costco",
            is_purchased=True,
            purchase_date="2024-01-16",
            notes="Free-range chicken"
        ),
        GroceryItem(
            name="Bread",
            category="Bakery",
            quantity=2.0,
            unit="loaf",
            price_per_unit=2.50,
            store_name="Walmart",
            is_purchased=True,
            purchase_date="2024-01-16",
            notes="Whole wheat bread"
        ),
        GroceryItem(
            name="Rice",
            category="Pantry Staples",
            quantity=5.0,
            unit="kg",
            price_per_unit=3.99,
            store_name="Target",
            is_purchased=True,
            purchase_date="2024-01-17",
            notes="Basmati rice"
        ),
        GroceryItem(
            name="Orange Juice",
            category="Beverages",
            quantity=1.0,
            unit="bottle",
            price_per_unit=4.25,
            store_name="Walmart",
            is_purchased=True,
            purchase_date="2024-01-17",
            notes="Fresh squeezed"
        ),
        GroceryItem(
            name="Potato Chips",
            category="Snacks",
            quantity=3.0,
            unit="bag",
            price_per_unit=3.99,
            store_name="Target",
            is_purchased=True,
            purchase_date="2024-01-18",
            notes="Sea salt flavor"
        ),
        GroceryItem(
            name="Frozen Pizza",
            category="Frozen Foods",
            quantity=2.0,
            unit="pack",
            price_per_unit=6.50,
            store_name="Costco",
            is_purchased=True,
            purchase_date="2024-01-18",
            notes="Margherita pizza"
        ),
        GroceryItem(
            name="Shampoo",
            category="Health & Beauty",
            quantity=1.0,
            unit="bottle",
            price_per_unit=12.99,
            store_name="Target",
            is_purchased=True,
            purchase_date="2024-01-19",
            notes="Organic shampoo"
        ),
        GroceryItem(
            name="Paper Towels",
            category="Household Items",
            quantity=1.0,
            unit="pack",
            price_per_unit=8.99,
            store_name="Walmart",
            is_purchased=True,
            purchase_date="2024-01-19",
            notes="12-pack"
        ),
        # Some unpurchased items
        GroceryItem(
            name="Bananas",
            category="Fruits & Vegetables",
            quantity=1.0,
            unit="bunch",
            price_per_unit=2.99,
            store_name="Whole Foods",
            is_purchased=False,
            purchase_date="",
            notes="Organic bananas"
        ),
        GroceryItem(
            name="Greek Yogurt",
            category="Dairy & Eggs",
            quantity=4.0,
            unit="pack",
            price_per_unit=5.99,
            store_name="Costco",
            is_purchased=False,
            purchase_date="",
            notes="Plain Greek yogurt"
        ),
        GroceryItem(
            name="Salmon Fillet",
            category="Meat & Seafood",
            quantity=1.0,
            unit="kg",
            price_per_unit=15.99,
            store_name="Whole Foods",
            is_purchased=False,
            purchase_date="",
            notes="Atlantic salmon"
        ),
        GroceryItem(
            name="Pasta",
            category="Pantry Staples",
            quantity=2.0,
            unit="pack",
            price_per_unit=1.99,
            store_name="Walmart",
            is_purchased=False,
            purchase_date="",
            notes="Whole wheat pasta"
        ),
        GroceryItem(
            name="Coffee Beans",
            category="Beverages",
            quantity=1.0,
            unit="bag",
            price_per_unit=9.99,
            store_name="Target",
            is_purchased=False,
            purchase_date="",
            notes="Dark roast coffee"
        )
    ]
    
    print("Adding sample grocery data...")
    
    # Add grocery items
    for item in sample_items:
        try:
            item_id = grocery_manager.add_item(item)
            print(f"✅ Added item: {item.name} - ${item.total_cost:.2f} (ID: {item_id})")
        except Exception as e:
            print(f"❌ Failed to add item {item.name}: {e}")
    
    # Set sample budgets
    try:
        grocery_manager.set_weekly_budget(100.0)
        print("✅ Set weekly budget: $100.00")
    except Exception as e:
        print(f"❌ Failed to set weekly budget: {e}")
    
    try:
        grocery_manager.set_monthly_budget(400.0)
        print("✅ Set monthly budget: $400.00")
    except Exception as e:
        print(f"❌ Failed to set monthly budget: {e}")
    
    return grocery_manager, expense_tracker


def demonstrate_features(grocery_manager, expense_tracker):
    """Demonstrate various features of the grocery optimizer."""
    print("\n" + "="*60)
    print("GROCERY OPTIMIZER DEMONSTRATION")
    print("="*60)
    
    # Overall summary
    total_items = grocery_manager.get_total_items_count()
    purchased_items = grocery_manager.get_purchased_items_count()
    unpurchased_items = grocery_manager.get_unpurchased_items_count()
    total_cost = grocery_manager.get_total_cost()
    purchased_cost = grocery_manager.get_purchased_total_cost()
    unpurchased_cost = grocery_manager.get_unpurchased_total_cost()
    
    print(f"\n1. OVERALL SUMMARY:")
    print("-" * 20)
    print(f"Total Items: {total_items}")
    print(f"Purchased Items: {purchased_items}")
    print(f"Unpurchased Items: {unpurchased_items}")
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Purchased Cost: ${purchased_cost:.2f}")
    print(f"Unpurchased Cost: ${unpurchased_cost:.2f}")
    
    # Budget information
    weekly_budget = grocery_manager.get_weekly_budget()
    monthly_budget = grocery_manager.get_monthly_budget()
    weekly_spending = expense_tracker.get_weekly_spending()
    monthly_spending = expense_tracker.get_monthly_spending()
    
    print(f"\n2. BUDGET INFORMATION:")
    print("-" * 25)
    print(f"Weekly Budget: ${weekly_budget:.2f}")
    print(f"Weekly Spending: ${weekly_spending:.2f}")
    print(f"Weekly Remaining: ${weekly_budget - weekly_spending:.2f}")
    print(f"Monthly Budget: ${monthly_budget:.2f}")
    print(f"Monthly Spending: ${monthly_spending:.2f}")
    print(f"Monthly Remaining: ${monthly_budget - monthly_spending:.2f}")
    
    # Category breakdown
    print(f"\n3. SPENDING BY CATEGORY:")
    print("-" * 30)
    category_summaries = expense_tracker.get_spending_by_category()
    for category in category_summaries:
        print(f"{category.category}: ${category.total_spent:.2f} "
              f"({category.item_count} items, {category.percentage_of_total:.1f}%)")
    
    # Store breakdown
    print(f"\n4. SPENDING BY STORE:")
    print("-" * 25)
    store_summaries = expense_tracker.get_spending_by_store()
    for store in store_summaries:
        print(f"{store.store_name}: ${store.total_spent:.2f} "
              f"({store.item_count} items, {store.percentage_of_total:.1f}%)")
    
    # Expense summary
    print(f"\n5. EXPENSE SUMMARY:")
    print("-" * 20)
    expense_summary = expense_tracker.get_expense_summary()
    print(f"Total Spent: ${expense_summary.total_spent:.2f}")
    print(f"Total Items: {expense_summary.total_items}")
    print(f"Average Item Cost: ${expense_summary.average_item_cost:.2f}")
    print(f"Most Expensive Item: {expense_summary.most_expensive_item} (${expense_summary.most_expensive_cost:.2f})")
    print(f"Cheapest Item: {expense_summary.cheapest_item} (${expense_summary.cheapest_cost:.2f})")
    
    # Budget alerts
    print(f"\n6. BUDGET ALERTS:")
    print("-" * 18)
    budget_alerts = expense_tracker.get_budget_alerts()
    if budget_alerts:
        for alert in budget_alerts:
            if alert.alert_type == "exceeded":
                print(f"🔴 {alert.message}")
            elif alert.alert_type == "warning":
                print(f"🟡 {alert.message}")
            elif alert.alert_type == "suggestion":
                print(f"💡 {alert.message}")
    else:
        print("✅ No budget alerts. You're within your budget!")
    
    # Cost optimization suggestions
    print(f"\n7. COST OPTIMIZATION SUGGESTIONS:")
    print("-" * 40)
    suggestions = expense_tracker.get_cost_optimization_suggestions()
    if suggestions:
        for suggestion in suggestions:
            if suggestion['type'] == 'expensive_item':
                print(f"💡 {suggestion['suggestion']}")
            elif suggestion['type'] == 'high_spending_category':
                print(f"📊 {suggestion['suggestion']}")
    else:
        print("✅ No optimization suggestions. Your spending looks good!")
    
    # Store comparisons
    print(f"\n8. STORE PRICE COMPARISONS:")
    print("-" * 35)
    comparisons = expense_tracker.get_store_comparison()
    if comparisons:
        # Show top 5 comparisons
        top_comparisons = sorted(comparisons, key=lambda x: x['potential_savings'], reverse=True)[:5]
        for comp in top_comparisons:
            print(f"{comp['item']}: Save ${comp['potential_savings']:.2f} by buying from {comp['cheapest_store']} "
                  f"instead of {comp['most_expensive_store']}")
    else:
        print("No store comparison data available.")
    
    # Categories and stores
    print(f"\n9. CATEGORIES AND STORES:")
    print("-" * 30)
    categories = grocery_manager.get_categories()
    stores = grocery_manager.get_stores()
    print(f"Categories: {', '.join(categories)}")
    print(f"Stores: {', '.join(stores)}")


def generate_sample_reports(grocery_manager, expense_tracker):
    """Generate sample reports."""
    print(f"\n10. GENERATING REPORTS:")
    print("-" * 25)
    
    report_generator = ReportGenerator(grocery_manager, expense_tracker)
    
    try:
        print("Generating grocery summary report...")
        report_generator.generate_grocery_summary()
        print("✅ Grocery summary report generated")
        
        print("Generating spending by category chart...")
        report_generator.generate_spending_by_category_chart()
        print("✅ Category chart generated")
        
        print("Generating spending by store chart...")
        report_generator.generate_spending_by_store_chart()
        print("✅ Store chart generated")
        
        print("Generating price distribution chart...")
        report_generator.generate_price_distribution_chart()
        print("✅ Price distribution chart generated")
        
        print("Generating spending trend chart...")
        report_generator.generate_spending_trend_chart()
        print("✅ Spending trend chart generated")
        
        print("Generating budget vs actual chart...")
        report_generator.generate_budget_vs_actual_chart()
        print("✅ Budget vs actual chart generated")
        
        print("Generating store comparison chart...")
        report_generator.generate_store_comparison_chart()
        print("✅ Store comparison chart generated")
        
        print("\nAll reports saved to the 'reports/' directory!")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")


def main():
    """Main demonstration function."""
    print("Grocery Optimizer Demo")
    print("This demo will create sample data and demonstrate features.")
    
    try:
        # Create sample data
        grocery_manager, expense_tracker = create_sample_data()
        
        # Demonstrate features
        demonstrate_features(grocery_manager, expense_tracker)
        
        # Generate reports
        generate_sample_reports(grocery_manager, expense_tracker)
        
        print(f"\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("You can now:")
        print("• Run 'python main.py' for the CLI interface")
        print("• Check the 'reports/' directory for generated files")
        print("• Check the 'data/' directory for the database")
        print("• Use the search functionality to find specific items")
        print("• Generate custom reports for different time periods")
        print("• Track your own grocery shopping")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    main()
