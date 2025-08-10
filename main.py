#!/usr/bin/env python3
"""
Personal Expense Tracker
Usage examples:
  python main.py --import_csv expenses.csv
  python main.py --report all
  python main.py --import_csv expenses.csv --report by_category
"""

import sqlite3
import csv
import argparse
import sys
from datetime import datetime

class ExpenseTracker:
    def __init__(self, db_path='expenses.db'):
        self.db_path = db_path
        self.create_table()
    
    def create_table(self):
        """Create expenses table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                UNIQUE(date, category, description, amount)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def import_csv(self, csv_path):
        """Import CSV data into SQLite, avoiding duplicates"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            imported_count = 0
            duplicate_count = 0
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        cursor.execute('''
                            INSERT INTO expenses (date, category, description, amount)
                            VALUES (?, ?, ?, ?)
                        ''', (row['date'], row['category'], row['description'], float(row['amount'])))
                        imported_count += 1
                    except sqlite3.IntegrityError:
                        # Duplicate record
                        duplicate_count += 1
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Skipping invalid row: {row} - {e}")
            
            conn.commit()
            conn.close()
            
            print(f"✓ Import completed:")
            print(f"  - {imported_count} new records imported")
            print(f"  - {duplicate_count} duplicates skipped")
            
        except FileNotFoundError:
            print(f"Error: CSV file '{csv_path}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error importing CSV: {e}")
            sys.exit(1)
    
    def get_category_totals(self):
        """Get total expenses by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                category,
                COUNT(*) as transaction_count,
                SUM(amount) as total_amount,
                AVG(amount) as avg_amount
            FROM expenses
            GROUP BY category
            ORDER BY total_amount DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_monthly_totals(self):
        """Get monthly spending totals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', date) as month,
                COUNT(*) as transactions,
                SUM(amount) as total_spent
            FROM expenses
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_biggest_expenses(self, limit=10):
        """Get biggest expenses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, category, description, amount
            FROM expenses
            ORDER BY amount DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_expenses_over_threshold(self, threshold):
        """Get expenses over a threshold amount"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, category, description, amount
            FROM expenses
            WHERE amount > ?
            ORDER BY amount DESC
        ''', (threshold,))
        
        results = cursor.fetchall()
        conn.close()
        return results

def print_table(headers, rows, title=None):
    """Print data in a formatted table"""
    if title:
        print(f"\n{title}")
        print("=" * len(title))
    
    if not rows:
        print("No data found.")
        return
    
    # Calculate column widths
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Print header
    header_row = " | ".join(str(header).ljust(widths[i]) for i, header in enumerate(headers))
    print(f"\n{header_row}")
    print("-" * len(header_row))
    
    # Print rows
    for row in rows:
        formatted_row = []
        for i, cell in enumerate(row):
            if isinstance(cell, float):
                formatted_cell = f"₹{cell:.2f}".ljust(widths[i])
            else:
                formatted_cell = str(cell).ljust(widths[i])
            formatted_row.append(formatted_cell)
        print(" | ".join(formatted_row))

def main():
    parser = argparse.ArgumentParser(description='Personal Expense Tracker')
    parser.add_argument('--db', default='expenses.db',
                        help='Database path (default: expenses.db)')
    parser.add_argument('--import_csv',
                        help='CSV file path to import')
    parser.add_argument('--report', 
                        choices=['by_category', 'monthly', 'biggest', 'over_threshold', 'all'],
                        help='Report type to generate')
    parser.add_argument('--threshold', type=float, default=100.0,
                        help='Threshold amount for filtering expenses (default: 100)')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = ExpenseTracker(args.db)
    
    # Import CSV if specified
    if args.import_csv:
        tracker.import_csv(args.import_csv)
    
    # Generate reports
    if args.report:
        if args.report == 'by_category' or args.report == 'all':
            results = tracker.get_category_totals()
            print_table(['Category', 'Transactions', 'Total', 'Average'],
                       results, 'SPENDING BY CATEGORY')
        
        if args.report == 'monthly' or args.report == 'all':
            results = tracker.get_monthly_totals()
            print_table(['Month', 'Transactions', 'Total Spent'],
                       results, 'MONTHLY SPENDING')
        
        if args.report == 'biggest' or args.report == 'all':
            results = tracker.get_biggest_expenses()
            print_table(['Date', 'Category', 'Description', 'Amount'],
                       results, 'TOP 10 BIGGEST EXPENSES')
        
        if args.report == 'over_threshold' or args.report == 'all':
            results = tracker.get_expenses_over_threshold(args.threshold)
            print_table(['Date', 'Category', 'Description', 'Amount'],
                       results, f'EXPENSES OVER ₹{args.threshold:.2f}')
    
    if not args.import_csv and not args.report:
        parser.print_help()

if __name__ == "__main__":
    main()
