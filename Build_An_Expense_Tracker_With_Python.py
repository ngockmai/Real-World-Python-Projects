import os
import json
from datetime import datetime

EXPENSE_FILE = "expenses.json"

#Load expenses from file
def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            return json.load(file)
    return []

#Save expense to file
def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# Get valid date input
def get_valid_date(message="Enter the date (YYYY-MM-DD): "):
    while True:
        try:
            date_str = input(message).strip()
            if date_str == "y":
                print("Returning to main menu.\n")
                return None
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD or enter 'y' to return main menu.\n")

# Get valid category input
def get_valid_category():
    while True:
        try:
            category_str = input("Enter the category: ").strip()
            if category_str == "y":
                print("Returning to main menu.\n")
                return None
            if category_str == "":
                print("category cannot be empty. Please enter a valid category or enter 'y' to return main menu.\n")
            return category_str
        except ValueError:
            print("Invalid category. Please enter a valid category or enter 'y' to return main menu.\n")

#Get valid description
def get_valid_description():
    while True:
        try:
            description_str = input("Enter the description: ").strip()
            if description_str == "y":
                print("Returning to main menu.\n")
                return None
            return description_str
        except ValueError:
            print("Invalid description. Please enter a valid description or enter 'y' to return main menu.\n")  

#Get valid amount input
def get_valid_amount():
    while True:
        try: 
            amount_str = input("Enter the amount: ").strip()
            if amount_str == "y":
                print("Returning to main menu.\n")
                return None
            return float(amount_str)
        except ValueError:
            print("Invalid amount. Please enter a valid amount or enter 'y' to return main menu.\n")

#Add an expense to the expense list
def add_expense(expenses):
        print("\nAdding new Expense")
        date = get_valid_date()
        if date is None:
            return
        category = get_valid_category()
        if category is None:
            return
        description = get_valid_description()

        amount = get_valid_amount()
        if amount is None:
            return

        expense = {"date" : date, 
                   "category" : category, 
                   "description" : description, 
                   "amount" : amount}
        expenses.append(expense)
        save_expenses(expenses)
        print("Expense added successfully! \n")
        
#View all expenses
def view_expense(expenses):
    if not expenses:
        print("No expenses recorded yet. \n")
        return
    
    print ("\n--- All expenses ---")
    print("{:<12} {:<15} {:<25} {:<10}".format("Date", "Category", "Description", "Amount"))
    print("-" * 90)
    total = 0
    for exp in expenses:
        exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")
        print("{:<12} {:<15} {:<25} {:10.2f}".format(exp["date"], exp["category"], exp["description"], exp["amount"]))
        print("\n")

#Search expenses by date
def search_expense(expenses):
    if not expenses:
        print("No expenses recorded yet. \n")
        return
    
    start_date = get_valid_date("Enter the start date (YYYY-MM-DD): ")
    if start_date is None:
        return
    end_date = get_valid_date("Enter the end date (YYYY-MM-DD): ")
    if end_date is None:
        return
    
    print("\n--- Expenses by date ---")
    print("\nSpending between {} and {}".format(start_date, end_date))
    print("{:<12} {:<15} {:<25} {:<10}".format("Date", "Category", "Description", "Amount"))
    print("-" * 90)
    total = 0
    for exp in expenses:
        if start_date <= exp["date"] <= end_date:
            print("{:<12} {:<15} {:<25} {:10.2f}".format(exp["date"], exp["category"], exp["description"], exp["amount"]))
            total += exp["amount"]
            print("\n")
    print(f"\nTotal Spending: + {total:.2f}")

#Calculate total spending

def total_expense(expenses):
    total = 0
    for exp in expenses:
        total += exp["amount"]
    print(f"\nTotal Spending: {total:.2f}")
#Main menu
def main():
    expenses = load_expenses()
    while True:
        print("Welcome to the Expense Tracker!")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. Search expenses by date")
        print("4. Calculate total spending")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()
        

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expense(expenses)
        elif choice == "3":
            search_expense(expenses)
        elif choice == "4":
            total_expense(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again. \n")


if __name__ == "__main__":
    main()