#!/usr/bin/env python3
import csv
import random
import argparse
from datetime import datetime, timedelta

def generate_fake_expenses(num_records=100):
    """Generate fake expense data"""
    categories = {
        'Food': ['Coffee', 'Lunch', 'Dinner', 'Groceries', 'Breakfast', 'Snacks', 'Fast Food'],
        'Transport': ['Bus ticket', 'Taxi', 'Gas', 'Parking', 'Train', 'Uber', 'Metro'],
        'Shopping': ['Clothes', 'Electronics', 'Books', 'Shoes', 'Home goods', 'Gifts'],
        'Entertainment': ['Movie', 'Concert', 'Games', 'Streaming', 'Sports event', 'Theater'],
        'Utilities': ['Electricity', 'Water', 'Internet', 'Phone', 'Gas bill', 'Cable'],
        'Healthcare': ['Medicine', 'Doctor visit', 'Dental', 'Insurance', 'Vitamins', 'Pharmacy'],
        'Education': ['Books', 'Course fee', 'Supplies', 'Software', 'Training'],
        'Travel': ['Hotel', 'Flight', 'Rental car', 'Tourism', 'Accommodation']
    }
    
    # Amount ranges by category (min, max) in Indian Rupees
    amount_ranges = {
        'Food': (50.0, 2000.0),
        'Transport': (25.0, 1200.0),
        'Shopping': (500.0, 15000.0),
        'Entertainment': (200.0, 4000.0),
        'Utilities': (800.0, 8000.0),
        'Healthcare': (300.0, 20000.0),
        'Education': (1000.0, 35000.0),
        'Travel': (2000.0, 50000.0)
    }
    
    expenses = []
    start_date = datetime.now() - timedelta(days=365)
    
    for _ in range(num_records):
        # Random date within the last year
        random_days = random.randint(0, 365)
        expense_date = start_date + timedelta(days=random_days)
        
        # Random category and description
        category = random.choice(list(categories.keys()))
        description = random.choice(categories[category])
        
        # Random amount based on category
        min_amount, max_amount = amount_ranges[category]
        amount = round(random.uniform(min_amount, max_amount), 2)
        
        expenses.append({
            'date': expense_date.strftime('%Y-%m-%d'),
            'category': category,
            'description': description,
            'amount': amount
        })
    
    return expenses

def write_to_csv(expenses, filename='expenses.csv'):
    """Write expenses to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['date', 'category', 'description', 'amount']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

def main():
    parser = argparse.ArgumentParser(description='Generate fake expense data')
    parser.add_argument('num_records', type=int, nargs='?', default=100,
                        help='Number of expense records to generate (default: 100)')
    parser.add_argument('--output', default='expenses.csv',
                        help='Output CSV filename (default: expenses.csv)')
    
    args = parser.parse_args()
    
    print(f"Generating {args.num_records} fake expense records...")
    expenses = generate_fake_expenses(args.num_records)
    
    write_to_csv(expenses, args.output)
    print(f"✓ Generated {len(expenses)} records and saved to {args.output}")

if __name__ == "__main__":
    main()
