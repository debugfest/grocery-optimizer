#!/usr/bin/env python3
"""
Grocery List & Expense Optimizer CLI Application.

This is the main entry point for the grocery optimizer application.
It provides a command-line interface for managing grocery items, tracking expenses, and generating reports.
"""

import sys
import os
from typing import Optional, List, Tuple
from datetime import datetime, date

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from grocery import GroceryManager, GroceryItem
from expense import ExpenseTracker, ExpenseSummary, CategorySummary, StoreSummary, BudgetAlert
from reports import ReportGenerator
from utils import (
    validate_price, validate_quantity, validate_item_name, validate_category,
    validate_unit, validate_store_name, validate_notes, validate_date,
    parse_price, parse_quantity, format_currency, format_date,
    get_common_grocery_categories, get_common_units, get_common_stores,
    get_current_date_string
)


class GroceryOptimizerCLI:
    """Command-line interface for the grocery optimizer."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.console = Console()
        self.grocery_manager = GroceryManager()
        self.expense_tracker = ExpenseTracker()
        self.report_generator = ReportGenerator(self.grocery_manager, self.expense_tracker)
        self.running = True
    
    def display_welcome(self) -> None:
        """Display welcome message and main menu."""
        welcome_text = """
        🛒 GROCERY LIST & EXPENSE OPTIMIZER 🛒
        
        Manage your grocery shopping, track expenses, and optimize your budget
        with smart suggestions and detailed analytics!
        """
        
        self.console.print(Panel(welcome_text, title="Welcome", border_style="green"))
    
    def display_main_menu(self) -> None:
        """Display the main menu options."""
        menu_options = [
            "🛒 Grocery Items Management",
            "💰 Expense Tracking & Analytics", 
            "📊 Budget Management",
            "📈 Reports & Visualizations",
            "🔍 Search & Filter Items",
            "⚙️ Settings & Configuration",
            "❌ Exit"
        ]
        
        table = Table(title="Main Menu", show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        descriptions = [
            "Add, edit, and manage grocery items",
            "Track spending and view analytics",
            "Set and monitor budget limits",
            "Generate reports and charts",
            "Search and filter grocery items",
            "Configure application settings",
            "Exit the application"
        ]
        
        for i, (option, desc) in enumerate(zip(menu_options, descriptions), 1):
            table.add_row(f"{i}", f"{option} - {desc}")
        
        self.console.print(table)
    
    def get_user_choice(self) -> str:
        """Get user's menu choice."""
        while True:
            try:
                choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7"])
                return choice
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Exiting...[/yellow]")
                sys.exit(0)
    
    def grocery_management_menu(self) -> None:
        """Handle grocery items management operations."""
        while True:
            self.console.print("\n[bold blue]🛒 Grocery Items Management[/bold blue]")
            self.console.print("1. Add New Item")
            self.console.print("2. View All Items")
            self.console.print("3. Edit Item")
            self.console.print("4. Delete Item")
            self.console.print("5. Mark as Purchased")
            self.console.print("6. Mark as Unpurchased")
            self.console.print("7. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "1":
                self.add_grocery_item()
            elif choice == "2":
                self.view_all_items()
            elif choice == "3":
                self.edit_item()
            elif choice == "4":
                self.delete_item()
            elif choice == "5":
                self.mark_as_purchased()
            elif choice == "6":
                self.mark_as_unpurchased()
            elif choice == "7":
                break
    
    def add_grocery_item(self) -> None:
        """Add a new grocery item."""
        self.console.print("\n[bold green]Add New Grocery Item[/bold green]")
        
        try:
            # Get item name
            name = Prompt.ask("Item name")
            if not validate_item_name(name):
                self.console.print("[red]Invalid item name.[/red]")
                return
            
            # Get category
            common_categories = get_common_grocery_categories()
            self.console.print(f"Common categories: {', '.join(common_categories)}")
            category = Prompt.ask("Category")
            if not validate_category(category):
                self.console.print("[red]Invalid category.[/red]")
                return
            
            # Get quantity
            quantity_input = Prompt.ask("Quantity")
            try:
                quantity = parse_quantity(quantity_input)
            except ValueError as e:
                self.console.print(f"[red]Invalid quantity: {e}[/red]")
                return
            
            # Get unit
            common_units = get_common_units()
            self.console.print(f"Common units: {', '.join(common_units)}")
            unit = Prompt.ask("Unit")
            if not validate_unit(unit):
                self.console.print("[red]Invalid unit.[/red]")
                return
            
            # Get price per unit
            price_input = Prompt.ask("Price per unit")
            try:
                price_per_unit = parse_price(price_input)
            except ValueError as e:
                self.console.print(f"[red]Invalid price: {e}[/red]")
                return
            
            # Get store name
            common_stores = get_common_stores()
            self.console.print(f"Common stores: {', '.join(common_stores)}")
            store_name = Prompt.ask("Store name")
            if not validate_store_name(store_name):
                self.console.print("[red]Invalid store name.[/red]")
                return
            
            # Get notes
            notes = Prompt.ask("Notes (optional)", default="")
            if not validate_notes(notes):
                self.console.print("[red]Notes too long.[/red]")
                return
            
            # Create and add item
            item = GroceryItem(
                name=name,
                category=category,
                quantity=quantity,
                unit=unit,
                price_per_unit=price_per_unit,
                store_name=store_name,
                is_purchased=False,
                purchase_date="",
                notes=notes
            )
            
            item_id = self.grocery_manager.add_item(item)
            self.console.print(f"[green]✅ Grocery item added successfully with ID: {item_id}[/green]")
            self.console.print(f"[green]Total cost: {item.total_cost_display}[/green]")
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error adding item: {e}[/red]")
    
    def view_all_items(self) -> None:
        """View all grocery items."""
        items = self.grocery_manager.get_all_items()
        
        if not items:
            self.console.print("[yellow]No grocery items found.[/yellow]")
            return
        
        table = Table(title="All Grocery Items", show_header=True, header_style="bold blue")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Category", style="blue")
        table.add_column("Quantity", style="white", justify="right")
        table.add_column("Unit", style="white")
        table.add_column("Price/Unit", style="green", justify="right")
        table.add_column("Total Cost", style="green", justify="right")
        table.add_column("Store", style="yellow")
        table.add_column("Status", style="white")
        
        for item in items:
            status = "✅ Purchased" if item.is_purchased else "⏳ Pending"
            table.add_row(
                str(item.id),
                item.name,
                item.category,
                str(item.quantity),
                item.unit,
                item.cost_per_unit_display,
                item.total_cost_display,
                item.store_name,
                status
            )
        
        self.console.print(table)
        
        # Show summary
        total_cost = sum(item.total_cost for item in items)
        purchased_cost = sum(item.total_cost for item in items if item.is_purchased)
        pending_cost = sum(item.total_cost for item in items if not item.is_purchased)
        
        self.console.print(f"\n[bold green]Total Cost: {format_currency(total_cost)}[/bold green]")
        self.console.print(f"[green]Purchased: {format_currency(purchased_cost)}[/green]")
        self.console.print(f"[yellow]Pending: {format_currency(pending_cost)}[/yellow]")
    
    def edit_item(self) -> None:
        """Edit an existing grocery item."""
        self.console.print("\n[bold blue]Edit Grocery Item[/bold blue]")
        
        # First show all items
        self.view_all_items()
        
        try:
            item_id = int(Prompt.ask("Enter item ID to edit"))
            item = self.grocery_manager.get_item_by_id(item_id)
            
            if not item:
                self.console.print("[red]Item not found.[/red]")
                return
            
            self.console.print(f"\n[bold]Editing: {item.name}[/bold]")
            
            # Get updated values
            name = Prompt.ask("Item name", default=item.name)
            if not validate_item_name(name):
                self.console.print("[red]Invalid item name.[/red]")
                return
            
            category = Prompt.ask("Category", default=item.category)
            if not validate_category(category):
                self.console.print("[red]Invalid category.[/red]")
                return
            
            quantity_input = Prompt.ask("Quantity", default=str(item.quantity))
            try:
                quantity = parse_quantity(quantity_input)
            except ValueError as e:
                self.console.print(f"[red]Invalid quantity: {e}[/red]")
                return
            
            unit = Prompt.ask("Unit", default=item.unit)
            if not validate_unit(unit):
                self.console.print("[red]Invalid unit.[/red]")
                return
            
            price_input = Prompt.ask("Price per unit", default=str(item.price_per_unit))
            try:
                price_per_unit = parse_price(price_input)
            except ValueError as e:
                self.console.print(f"[red]Invalid price: {e}[/red]")
                return
            
            store_name = Prompt.ask("Store name", default=item.store_name)
            if not validate_store_name(store_name):
                self.console.print("[red]Invalid store name.[/red]")
                return
            
            notes = Prompt.ask("Notes", default=item.notes)
            if not validate_notes(notes):
                self.console.print("[red]Notes too long.[/red]")
                return
            
            # Update item
            item.name = name
            item.category = category
            item.quantity = quantity
            item.unit = unit
            item.price_per_unit = price_per_unit
            item.store_name = store_name
            item.notes = notes
            
            success = self.grocery_manager.update_item(item)
            if success:
                self.console.print(f"[green]✅ Item updated successfully![/green]")
                self.console.print(f"[green]New total cost: {item.total_cost_display}[/green]")
            else:
                self.console.print("[red]❌ Failed to update item.[/red]")
                
        except ValueError:
            self.console.print("[red]Invalid item ID.[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error editing item: {e}[/red]")
    
    def delete_item(self) -> None:
        """Delete a grocery item."""
        self.console.print("\n[bold red]Delete Grocery Item[/bold red]")
        
        # First show all items
        self.view_all_items()
        
        try:
            item_id = int(Prompt.ask("Enter item ID to delete"))
            item = self.grocery_manager.get_item_by_id(item_id)
            
            if not item:
                self.console.print("[red]Item not found.[/red]")
                return
            
            self.console.print(f"\n[bold]Item to delete: {item.name} - {item.total_cost_display}[/bold]")
            
            if Confirm.ask("Are you sure you want to delete this item?"):
                success = self.grocery_manager.delete_item(item_id)
                if success:
                    self.console.print(f"[green]✅ Item deleted successfully![/green]")
                else:
                    self.console.print("[red]❌ Failed to delete item.[/red]")
            else:
                self.console.print("[yellow]Deletion cancelled.[/yellow]")
                
        except ValueError:
            self.console.print("[red]Invalid item ID.[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error deleting item: {e}[/red]")
    
    def mark_as_purchased(self) -> None:
        """Mark an item as purchased."""
        self.console.print("\n[bold green]Mark Item as Purchased[/bold green]")
        
        # Show unpurchased items
        unpurchased_items = self.grocery_manager.get_unpurchased_items()
        if not unpurchased_items:
            self.console.print("[yellow]No unpurchased items found.[/yellow]")
            return
        
        table = Table(title="Unpurchased Items", show_header=True, header_style="bold yellow")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Total Cost", style="green", justify="right")
        table.add_column("Store", style="yellow")
        
        for item in unpurchased_items:
            table.add_row(
                str(item.id),
                item.name,
                item.total_cost_display,
                item.store_name
            )
        
        self.console.print(table)
        
        try:
            item_id = int(Prompt.ask("Enter item ID to mark as purchased"))
            item = self.grocery_manager.get_item_by_id(item_id)
            
            if not item:
                self.console.print("[red]Item not found.[/red]")
                return
            
            purchase_date = Prompt.ask("Purchase date (YYYY-MM-DD)", default=get_current_date_string())
            if not validate_date(purchase_date):
                self.console.print("[red]Invalid date format.[/red]")
                return
            
            success = self.grocery_manager.mark_as_purchased(item_id, purchase_date)
            if success:
                self.console.print(f"[green]✅ Item marked as purchased![/green]")
            else:
                self.console.print("[red]❌ Failed to mark item as purchased.[/red]")
                
        except ValueError:
            self.console.print("[red]Invalid item ID.[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error marking item: {e}[/red]")
    
    def mark_as_unpurchased(self) -> None:
        """Mark an item as unpurchased."""
        self.console.print("\n[bold yellow]Mark Item as Unpurchased[/bold yellow]")
        
        # Show purchased items
        purchased_items = self.grocery_manager.get_purchased_items()
        if not purchased_items:
            self.console.print("[yellow]No purchased items found.[/yellow]")
            return
        
        table = Table(title="Purchased Items", show_header=True, header_style="bold green")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Total Cost", style="green", justify="right")
        table.add_column("Purchase Date", style="white")
        
        for item in purchased_items:
            table.add_row(
                str(item.id),
                item.name,
                item.total_cost_display,
                item.purchase_date
            )
        
        self.console.print(table)
        
        try:
            item_id = int(Prompt.ask("Enter item ID to mark as unpurchased"))
            item = self.grocery_manager.get_item_by_id(item_id)
            
            if not item:
                self.console.print("[red]Item not found.[/red]")
                return
            
            success = self.grocery_manager.mark_as_unpurchased(item_id)
            if success:
                self.console.print(f"[green]✅ Item marked as unpurchased![/green]")
            else:
                self.console.print("[red]❌ Failed to mark item as unpurchased.[/red]")
                
        except ValueError:
            self.console.print("[red]Invalid item ID.[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error marking item: {e}[/red]")
    
    def expense_tracking_menu(self) -> None:
        """Handle expense tracking and analytics operations."""
        while True:
            self.console.print("\n[bold green]💰 Expense Tracking & Analytics[/bold green]")
            self.console.print("1. View Expense Summary")
            self.console.print("2. View Spending by Category")
            self.console.print("3. View Spending by Store")
            self.console.print("4. View Budget Alerts")
            self.console.print("5. View Cost Optimization Suggestions")
            self.console.print("6. View Store Price Comparisons")
            self.console.print("7. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "1":
                self.view_expense_summary()
            elif choice == "2":
                self.view_spending_by_category()
            elif choice == "3":
                self.view_spending_by_store()
            elif choice == "4":
                self.view_budget_alerts()
            elif choice == "5":
                self.view_optimization_suggestions()
            elif choice == "6":
                self.view_store_comparisons()
            elif choice == "7":
                break
    
    def view_expense_summary(self) -> None:
        """View comprehensive expense summary."""
        expense_summary = self.expense_tracker.get_expense_summary()
        
        summary_text = f"""
        Total Spent: {format_currency(expense_summary.total_spent)}
        Total Items: {expense_summary.total_items}
        Average Item Cost: {format_currency(expense_summary.average_item_cost)}
        
        Most Expensive Item: {expense_summary.most_expensive_item} ({format_currency(expense_summary.most_expensive_cost)})
        Cheapest Item: {expense_summary.cheapest_item} ({format_currency(expense_summary.cheapest_cost)})
        
        Budget Remaining: {format_currency(expense_summary.budget_remaining)}
        Budget Used: {expense_summary.budget_used_percentage:.1f}%
        """
        
        self.console.print(Panel(summary_text, title="Expense Summary", border_style="green"))
    
    def view_spending_by_category(self) -> None:
        """View spending breakdown by category."""
        category_summaries = self.expense_tracker.get_spending_by_category()
        
        if not category_summaries:
            self.console.print("[yellow]No spending data available by category.[/yellow]")
            return
        
        table = Table(title="Spending by Category", show_header=True, header_style="bold blue")
        table.add_column("Category", style="cyan")
        table.add_column("Total Spent", style="green", justify="right")
        table.add_column("Items", style="white", justify="right")
        table.add_column("Average Cost", style="white", justify="right")
        table.add_column("Percentage", style="yellow", justify="right")
        
        for category in category_summaries:
            table.add_row(
                category.category,
                format_currency(category.total_spent),
                str(category.item_count),
                format_currency(category.average_cost),
                f"{category.percentage_of_total:.1f}%"
            )
        
        self.console.print(table)
    
    def view_spending_by_store(self) -> None:
        """View spending breakdown by store."""
        store_summaries = self.expense_tracker.get_spending_by_store()
        
        if not store_summaries:
            self.console.print("[yellow]No spending data available by store.[/yellow]")
            return
        
        table = Table(title="Spending by Store", show_header=True, header_style="bold yellow")
        table.add_column("Store", style="cyan")
        table.add_column("Total Spent", style="green", justify="right")
        table.add_column("Items", style="white", justify="right")
        table.add_column("Average Cost", style="white", justify="right")
        table.add_column("Percentage", style="yellow", justify="right")
        
        for store in store_summaries:
            table.add_row(
                store.store_name,
                format_currency(store.total_spent),
                str(store.item_count),
                format_currency(store.average_cost),
                f"{store.percentage_of_total:.1f}%"
            )
        
        self.console.print(table)
    
    def view_budget_alerts(self) -> None:
        """View budget alerts and warnings."""
        budget_alerts = self.expense_tracker.get_budget_alerts()
        
        if not budget_alerts:
            self.console.print("[green]✅ No budget alerts. You're within your budget![/green]")
            return
        
        for alert in budget_alerts:
            if alert.alert_type == "exceeded":
                self.console.print(f"[red]🔴 {alert.message}[/red]")
            elif alert.alert_type == "warning":
                self.console.print(f"[yellow]🟡 {alert.message}[/yellow]")
            elif alert.alert_type == "suggestion":
                self.console.print(f"[blue]💡 {alert.message}[/blue]")
    
    def view_optimization_suggestions(self) -> None:
        """View cost optimization suggestions."""
        suggestions = self.expense_tracker.get_cost_optimization_suggestions()
        
        if not suggestions:
            self.console.print("[green]✅ No optimization suggestions. Your spending looks good![/green]")
            return
        
        self.console.print("[bold blue]💡 Cost Optimization Suggestions[/bold blue]")
        for suggestion in suggestions:
            if suggestion['type'] == 'expensive_item':
                self.console.print(f"[yellow]• {suggestion['suggestion']}[/yellow]")
            elif suggestion['type'] == 'high_spending_category':
                self.console.print(f"[blue]• {suggestion['suggestion']}[/blue]")
    
    def view_store_comparisons(self) -> None:
        """View store price comparisons."""
        comparisons = self.expense_tracker.get_store_comparison()
        
        if not comparisons:
            self.console.print("[yellow]No store comparison data available.[/yellow]")
            return
        
        # Show top 10 comparisons
        top_comparisons = sorted(comparisons, key=lambda x: x['potential_savings'], reverse=True)[:10]
        
        table = Table(title="Store Price Comparisons (Top 10 Savings)", show_header=True, header_style="bold green")
        table.add_column("Item", style="white")
        table.add_column("Cheapest Store", style="green")
        table.add_column("Cheapest Price", style="green", justify="right")
        table.add_column("Most Expensive Store", style="red")
        table.add_column("Most Expensive Price", style="red", justify="right")
        table.add_column("Potential Savings", style="blue", justify="right")
        
        for comp in top_comparisons:
            table.add_row(
                comp['item'],
                comp['cheapest_store'],
                format_currency(comp['cheapest_price']),
                comp['most_expensive_store'],
                format_currency(comp['most_expensive_price']),
                format_currency(comp['potential_savings'])
            )
        
        self.console.print(table)
    
    def budget_management_menu(self) -> None:
        """Handle budget management operations."""
        while True:
            self.console.print("\n[bold yellow]📊 Budget Management[/bold yellow]")
            self.console.print("1. Set Weekly Budget")
            self.console.print("2. Set Monthly Budget")
            self.console.print("3. View Current Budgets")
            self.console.print("4. View Budget Status")
            self.console.print("5. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self.set_weekly_budget()
            elif choice == "2":
                self.set_monthly_budget()
            elif choice == "3":
                self.view_current_budgets()
            elif choice == "4":
                self.view_budget_status()
            elif choice == "5":
                break
    
    def set_weekly_budget(self) -> None:
        """Set weekly budget limit."""
        self.console.print("\n[bold yellow]Set Weekly Budget[/bold yellow]")
        
        try:
            budget_input = Prompt.ask("Weekly budget amount")
            budget = parse_price(budget_input)
            
            success = self.grocery_manager.set_weekly_budget(budget)
            if success:
                self.console.print(f"[green]✅ Weekly budget set to {format_currency(budget)}[/green]")
            else:
                self.console.print("[red]❌ Failed to set weekly budget.[/red]")
                
        except ValueError as e:
            self.console.print(f"[red]Invalid budget amount: {e}[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error setting budget: {e}[/red]")
    
    def set_monthly_budget(self) -> None:
        """Set monthly budget limit."""
        self.console.print("\n[bold yellow]Set Monthly Budget[/bold yellow]")
        
        try:
            budget_input = Prompt.ask("Monthly budget amount")
            budget = parse_price(budget_input)
            
            success = self.grocery_manager.set_monthly_budget(budget)
            if success:
                self.console.print(f"[green]✅ Monthly budget set to {format_currency(budget)}[/green]")
            else:
                self.console.print("[red]❌ Failed to set monthly budget.[/red]")
                
        except ValueError as e:
            self.console.print(f"[red]Invalid budget amount: {e}[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error setting budget: {e}[/red]")
    
    def view_current_budgets(self) -> None:
        """View current budget settings."""
        weekly_budget = self.grocery_manager.get_weekly_budget()
        monthly_budget = self.grocery_manager.get_monthly_budget()
        
        budget_text = f"""
        Weekly Budget: {format_currency(weekly_budget)}
        Monthly Budget: {format_currency(monthly_budget)}
        """
        
        self.console.print(Panel(budget_text, title="Current Budgets", border_style="yellow"))
    
    def view_budget_status(self) -> None:
        """View budget status and spending."""
        weekly_budget = self.grocery_manager.get_weekly_budget()
        monthly_budget = self.grocery_manager.get_monthly_budget()
        
        if weekly_budget == 0 and monthly_budget == 0:
            self.console.print("[yellow]No budgets set. Set weekly or monthly budgets to track spending.[/yellow]")
            return
        
        status_lines = []
        
        if weekly_budget > 0:
            weekly_spending = self.expense_tracker.get_weekly_spending()
            weekly_remaining = weekly_budget - weekly_spending
            weekly_percentage = (weekly_spending / weekly_budget * 100) if weekly_budget > 0 else 0
            
            status_lines.append(f"Weekly Budget: {format_currency(weekly_budget)}")
            status_lines.append(f"Weekly Spending: {format_currency(weekly_spending)} ({weekly_percentage:.1f}%)")
            status_lines.append(f"Weekly Remaining: {format_currency(weekly_remaining)}")
            status_lines.append("")
        
        if monthly_budget > 0:
            monthly_spending = self.expense_tracker.get_monthly_spending()
            monthly_remaining = monthly_budget - monthly_spending
            monthly_percentage = (monthly_spending / monthly_budget * 100) if monthly_budget > 0 else 0
            
            status_lines.append(f"Monthly Budget: {format_currency(monthly_budget)}")
            status_lines.append(f"Monthly Spending: {format_currency(monthly_spending)} ({monthly_percentage:.1f}%)")
            status_lines.append(f"Monthly Remaining: {format_currency(monthly_remaining)}")
        
        status_text = "\n".join(status_lines)
        self.console.print(Panel(status_text, title="Budget Status", border_style="blue"))
    
    def reports_menu(self) -> None:
        """Handle reports and visualizations operations."""
        while True:
            self.console.print("\n[bold magenta]📈 Reports & Visualizations[/bold magenta]")
            self.console.print("1. Generate Grocery Summary Report")
            self.console.print("2. Generate Spending by Category Chart")
            self.console.print("3. Generate Spending by Store Chart")
            self.console.print("4. Generate Price Distribution Chart")
            self.console.print("5. Generate Spending Trend Chart")
            self.console.print("6. Generate Budget vs Actual Chart")
            self.console.print("7. Generate Store Comparison Chart")
            self.console.print("8. Generate Comprehensive Report")
            self.console.print("9. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
            
            if choice == "1":
                self.generate_grocery_summary()
            elif choice == "2":
                self.generate_category_chart()
            elif choice == "3":
                self.generate_store_chart()
            elif choice == "4":
                self.generate_price_distribution_chart()
            elif choice == "5":
                self.generate_trend_chart()
            elif choice == "6":
                self.generate_budget_chart()
            elif choice == "7":
                self.generate_comparison_chart()
            elif choice == "8":
                self.generate_comprehensive_report()
            elif choice == "9":
                break
    
    def generate_grocery_summary(self) -> None:
        """Generate grocery summary report."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating grocery summary...", total=None)
            self.report_generator.generate_grocery_summary()
        
        self.console.print("[green]✅ Grocery summary report generated![/green]")
    
    def generate_category_chart(self) -> None:
        """Generate spending by category chart."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating category chart...", total=None)
            self.report_generator.generate_spending_by_category_chart()
        
        self.console.print("[green]✅ Category chart generated![/green]")
    
    def generate_store_chart(self) -> None:
        """Generate spending by store chart."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating store chart...", total=None)
            self.report_generator.generate_spending_by_store_chart()
        
        self.console.print("[green]✅ Store chart generated![/green]")
    
    def generate_price_distribution_chart(self) -> None:
        """Generate price distribution chart."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating price distribution chart...", total=None)
            self.report_generator.generate_price_distribution_chart()
        
        self.console.print("[green]✅ Price distribution chart generated![/green]")
    
    def generate_trend_chart(self) -> None:
        """Generate spending trend chart."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating trend chart...", total=None)
            self.report_generator.generate_spending_trend_chart()
        
        self.console.print("[green]✅ Trend chart generated![/green]")
    
    def generate_budget_chart(self) -> None:
        """Generate budget vs actual chart."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating budget chart...", total=None)
            self.report_generator.generate_budget_vs_actual_chart()
        
        self.console.print("[green]✅ Budget chart generated![/green]")
    
    def generate_comparison_chart(self) -> None:
        """Generate store comparison chart."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating comparison chart...", total=None)
            self.report_generator.generate_store_comparison_chart()
        
        self.console.print("[green]✅ Comparison chart generated![/green]")
    
    def generate_comprehensive_report(self) -> None:
        """Generate comprehensive report with all charts."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating comprehensive report...", total=None)
            self.report_generator.generate_comprehensive_report()
        
        self.console.print("[green]✅ Comprehensive report generated![/green]")
    
    def search_menu(self) -> None:
        """Handle search and filter operations."""
        while True:
            self.console.print("\n[bold cyan]🔍 Search & Filter Items[/bold cyan]")
            self.console.print("1. Search Items")
            self.console.print("2. Filter by Category")
            self.console.print("3. Filter by Store")
            self.console.print("4. Filter by Price Range")
            self.console.print("5. Show Expensive Items")
            self.console.print("6. Show Budget-Friendly Items")
            self.console.print("7. Sort Items")
            self.console.print("8. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
            
            if choice == "1":
                self.search_items()
            elif choice == "2":
                self.filter_by_category()
            elif choice == "3":
                self.filter_by_store()
            elif choice == "4":
                self.filter_by_price_range()
            elif choice == "5":
                self.show_expensive_items()
            elif choice == "6":
                self.show_budget_friendly_items()
            elif choice == "7":
                self.sort_items()
            elif choice == "8":
                break
    
    def search_items(self) -> None:
        """Search items by name, category, or store."""
        query = Prompt.ask("Enter search term")
        
        if not query.strip():
            self.console.print("[yellow]Search term cannot be empty.[/yellow]")
            return
        
        matching_items = self.grocery_manager.search_items(query)
        
        if not matching_items:
            self.console.print(f"[yellow]No items found matching '{query}'.[/yellow]")
            return
        
        table = Table(title=f"Search Results for '{query}'", show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Category", style="blue")
        table.add_column("Total Cost", style="green", justify="right")
        table.add_column("Store", style="yellow")
        table.add_column("Status", style="white")
        
        for item in matching_items:
            status = "✅ Purchased" if item.is_purchased else "⏳ Pending"
            table.add_row(
                str(item.id),
                item.name,
                item.category,
                item.total_cost_display,
                item.store_name,
                status
            )
        
        self.console.print(table)
    
    def filter_by_category(self) -> None:
        """Filter items by category."""
        categories = self.grocery_manager.get_categories()
        
        if not categories:
            self.console.print("[yellow]No categories found.[/yellow]")
            return
        
        self.console.print(f"Available categories: {', '.join(categories)}")
        category = Prompt.ask("Enter category name")
        
        items = self.grocery_manager.get_items_by_category(category)
        
        if not items:
            self.console.print(f"[yellow]No items found in category '{category}'.[/yellow]")
            return
        
        table = Table(title=f"Items in Category: {category}", show_header=True, header_style="bold blue")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Total Cost", style="green", justify="right")
        table.add_column("Store", style="yellow")
        table.add_column("Status", style="white")
        
        for item in items:
            status = "✅ Purchased" if item.is_purchased else "⏳ Pending"
            table.add_row(
                str(item.id),
                item.name,
                item.total_cost_display,
                item.store_name,
                status
            )
        
        self.console.print(table)
    
    def filter_by_store(self) -> None:
        """Filter items by store."""
        stores = self.grocery_manager.get_stores()
        
        if not stores:
            self.console.print("[yellow]No stores found.[/yellow]")
            return
        
        self.console.print(f"Available stores: {', '.join(stores)}")
        store_name = Prompt.ask("Enter store name")
        
        items = self.grocery_manager.get_items_by_store(store_name)
        
        if not items:
            self.console.print(f"[yellow]No items found from store '{store_name}'.[/yellow]")
            return
        
        table = Table(title=f"Items from Store: {store_name}", show_header=True, header_style="bold yellow")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Category", style="blue")
        table.add_column("Total Cost", style="green", justify="right")
        table.add_column("Status", style="white")
        
        for item in items:
            status = "✅ Purchased" if item.is_purchased else "⏳ Pending"
            table.add_row(
                str(item.id),
                item.name,
                item.category,
                item.total_cost_display,
                status
            )
        
        self.console.print(table)
    
    def filter_by_price_range(self) -> None:
        """Filter items by price range."""
        try:
            min_price = parse_price(Prompt.ask("Minimum price"))
            max_price = parse_price(Prompt.ask("Maximum price"))
            
            if min_price > max_price:
                self.console.print("[red]Minimum price cannot be greater than maximum price.[/red]")
                return
            
            items = self.grocery_manager.get_items_by_price_range(min_price, max_price)
            
            if not items:
                self.console.print(f"[yellow]No items found in price range {format_currency(min_price)} - {format_currency(max_price)}.[/yellow]")
                return
            
            table = Table(title=f"Items in Price Range: {format_currency(min_price)} - {format_currency(max_price)}", 
                         show_header=True, header_style="bold green")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="white")
            table.add_column("Price/Unit", style="green", justify="right")
            table.add_column("Total Cost", style="green", justify="right")
            table.add_column("Store", style="yellow")
            
            for item in items:
                table.add_row(
                    str(item.id),
                    item.name,
                    item.cost_per_unit_display,
                    item.total_cost_display,
                    item.store_name
                )
            
            self.console.print(table)
            
        except ValueError as e:
            self.console.print(f"[red]Invalid price: {e}[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
    
    def show_expensive_items(self) -> None:
        """Show expensive items above threshold."""
        try:
            threshold = parse_price(Prompt.ask("Price threshold", default="10.0"))
            
            expensive_items = self.grocery_manager.get_expensive_items(threshold)
            
            if not expensive_items:
                self.console.print(f"[green]✅ No items found above {format_currency(threshold)}. Great job![/green]")
                return
            
            table = Table(title=f"Expensive Items (Above {format_currency(threshold)})", 
                         show_header=True, header_style="bold red")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="white")
            table.add_column("Price/Unit", style="red", justify="right")
            table.add_column("Total Cost", style="red", justify="right")
            table.add_column("Store", style="yellow")
            
            for item in expensive_items:
                table.add_row(
                    str(item.id),
                    item.name,
                    item.cost_per_unit_display,
                    item.total_cost_display,
                    item.store_name
                )
            
            self.console.print(table)
            
        except ValueError as e:
            self.console.print(f"[red]Invalid threshold: {e}[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
    
    def show_budget_friendly_items(self) -> None:
        """Show budget-friendly items below threshold."""
        try:
            threshold = parse_price(Prompt.ask("Price threshold", default="5.0"))
            
            budget_items = self.grocery_manager.get_budget_friendly_items(threshold)
            
            if not budget_items:
                self.console.print(f"[yellow]No items found below {format_currency(threshold)}.[/yellow]")
                return
            
            table = Table(title=f"Budget-Friendly Items (Below {format_currency(threshold)})", 
                         show_header=True, header_style="bold green")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="white")
            table.add_column("Price/Unit", style="green", justify="right")
            table.add_column("Total Cost", style="green", justify="right")
            table.add_column("Store", style="yellow")
            
            for item in budget_items:
                table.add_row(
                    str(item.id),
                    item.name,
                    item.cost_per_unit_display,
                    item.total_cost_display,
                    item.store_name
                )
            
            self.console.print(table)
            
        except ValueError as e:
            self.console.print(f"[red]Invalid threshold: {e}[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
    
    def sort_items(self) -> None:
        """Sort items by various criteria."""
        self.console.print("\n[bold cyan]Sort Items[/bold cyan]")
        self.console.print("1. Sort by Price (Low to High)")
        self.console.print("2. Sort by Price (High to Low)")
        self.console.print("3. Sort by Total Cost (Low to High)")
        self.console.print("4. Sort by Total Cost (High to Low)")
        self.console.print("5. Sort by Category")
        self.console.print("6. Sort by Name")
        self.console.print("7. Sort by Store")
        
        choice = Prompt.ask("Choose sorting option", choices=["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            items = self.grocery_manager.sort_items_by_price(ascending=True)
            title = "Items Sorted by Price (Low to High)"
        elif choice == "2":
            items = self.grocery_manager.sort_items_by_price(ascending=False)
            title = "Items Sorted by Price (High to Low)"
        elif choice == "3":
            items = self.grocery_manager.sort_items_by_total_cost(ascending=True)
            title = "Items Sorted by Total Cost (Low to High)"
        elif choice == "4":
            items = self.grocery_manager.sort_items_by_total_cost(ascending=False)
            title = "Items Sorted by Total Cost (High to Low)"
        elif choice == "5":
            items = self.grocery_manager.sort_items_by_category()
            title = "Items Sorted by Category"
        elif choice == "6":
            items = self.grocery_manager.sort_items_by_name()
            title = "Items Sorted by Name"
        elif choice == "7":
            items = self.grocery_manager.sort_items_by_store()
            title = "Items Sorted by Store"
        
        if not items:
            self.console.print("[yellow]No items found.[/yellow]")
            return
        
        table = Table(title=title, show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Category", style="blue")
        table.add_column("Price/Unit", style="green", justify="right")
        table.add_column("Total Cost", style="green", justify="right")
        table.add_column("Store", style="yellow")
        table.add_column("Status", style="white")
        
        for item in items:
            status = "✅ Purchased" if item.is_purchased else "⏳ Pending"
            table.add_row(
                str(item.id),
                item.name,
                item.category,
                item.cost_per_unit_display,
                item.total_cost_display,
                item.store_name,
                status
            )
        
        self.console.print(table)
    
    def settings_menu(self) -> None:
        """Handle settings and configuration operations."""
        while True:
            self.console.print("\n[bold purple]⚙️ Settings & Configuration[/bold purple]")
            self.console.print("1. View Application Statistics")
            self.console.print("2. Clear All Data")
            self.console.print("3. Export Data")
            self.console.print("4. Import Data")
            self.console.print("5. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self.view_statistics()
            elif choice == "2":
                self.clear_all_data()
            elif choice == "3":
                self.export_data()
            elif choice == "4":
                self.import_data()
            elif choice == "5":
                break
    
    def view_statistics(self) -> None:
        """View application statistics."""
        total_items = self.grocery_manager.get_total_items_count()
        purchased_items = self.grocery_manager.get_purchased_items_count()
        unpurchased_items = self.grocery_manager.get_unpurchased_items_count()
        categories = len(self.grocery_manager.get_categories())
        stores = len(self.grocery_manager.get_stores())
        total_cost = self.grocery_manager.get_total_cost()
        
        stats_text = f"""
        Total Items: {total_items}
        Purchased Items: {purchased_items}
        Unpurchased Items: {unpurchased_items}
        Categories: {categories}
        Stores: {stores}
        Total Cost: {format_currency(total_cost)}
        """
        
        self.console.print(Panel(stats_text, title="Application Statistics", border_style="purple"))
    
    def clear_all_data(self) -> None:
        """Clear all data from the database."""
        self.console.print("\n[bold red]⚠️ Clear All Data[/bold red]")
        self.console.print("This will permanently delete all grocery items and budget settings.")
        
        if Confirm.ask("Are you sure you want to clear all data?"):
            if Confirm.ask("This action cannot be undone. Are you absolutely sure?"):
                # This would require implementing a clear_all_data method
                self.console.print("[yellow]Clear all data functionality not implemented yet.[/yellow]")
            else:
                self.console.print("[yellow]Operation cancelled.[/yellow]")
        else:
            self.console.print("[yellow]Operation cancelled.[/yellow]")
    
    def export_data(self) -> None:
        """Export data to file."""
        self.console.print("[yellow]Export data functionality not implemented yet.[/yellow]")
    
    def import_data(self) -> None:
        """Import data from file."""
        self.console.print("[yellow]Import data functionality not implemented yet.[/yellow]")
    
    def run(self) -> None:
        """Run the main application loop."""
        self.display_welcome()
        
        while self.running:
            try:
                self.display_main_menu()
                choice = self.get_user_choice()
                
                if choice == "1":
                    self.grocery_management_menu()
                elif choice == "2":
                    self.expense_tracking_menu()
                elif choice == "3":
                    self.budget_management_menu()
                elif choice == "4":
                    self.reports_menu()
                elif choice == "5":
                    self.search_menu()
                elif choice == "6":
                    self.settings_menu()
                elif choice == "7":
                    self.console.print("\n[bold green]Thank you for using Grocery Optimizer![/bold green]")
                    self.running = False
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Exiting...[/yellow]")
                self.running = False
            except Exception as e:
                self.console.print(f"\n[red]❌ Unexpected error: {e}[/red]")


def main():
    """Main entry point for the application."""
    try:
        app = GroceryOptimizerCLI()
        app.run()
    except Exception as e:
        console = Console()
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()


# TODO: Add online price scraping (e.g., fetch real prices from a grocery API)
# TODO: Add sort by cost-per-unit feature
# TODO: Add list sharing via JSON export/import
# TODO: Fix bug: total cost sometimes miscalculates when quantity changes
# TODO: Add budget suggestion feature (auto suggest cheaper alternatives)
# TODO: Integrate voice input for adding grocery items
# TODO: Add unit tests for grocery and expense modules
# TODO: Improve Tkinter GUI layout for better UX
