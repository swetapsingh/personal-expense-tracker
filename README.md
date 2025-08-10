# Personal Expense Tracker

A command-line Python application for tracking and analyzing personal expenses using SQLite database storage.

## Features

- Generate fake expense data for testing
- Import expenses from CSV files into SQLite database
- Avoid duplicate entries when importing
- Generate formatted reports and analytics
- View spending by category, monthly trends, and biggest expenses
- Filter expenses above a threshold amount
- Use only Python standard libraries for maximum portability

## Project Structure

```
expense-tracker/
├── main.py              # Main CLI application
├── generate_data.py     # Fake data generator
├── expenses.csv         # Sample/imported expense data
├── queries.sql          # Reusable SQL queries
├── README.md           # Documentation
├── .gitignore          # Git ignore rules
└── expenses.db         # SQLite database (created automatically)
```

## Installation

No external dependencies required! This project uses only Python standard libraries:
- `sqlite3` - Database operations
- `csv` - CSV file handling
- `argparse` - Command-line argument parsing
- `random`, `datetime` - Data generation

Simply clone or download the project files.

## Usage

### 1. Generate Fake Data

Create a CSV file with fake expense records for testing:

```bash
# Generate 200 fake expense records
python generate_data.py 200

# Generate 50 records to a custom file
python generate_data.py 50 --output my_expenses.csv
```

### 2. Import CSV Data

Load expense data from a CSV file into the SQLite database:

```bash
# Import from default expenses.csv
python main.py --import_csv expenses.csv

# Import using custom database
python main.py --db my_expenses.db --import_csv expenses.csv
```

### 3. Generate Reports

Run various expense analysis reports:

```bash
# Show all reports
python main.py --report all

# Show spending by category
python main.py --report by_category

# Show monthly spending trends
python main.py --report monthly

# Show top 10 biggest expenses
python main.py --report biggest

# Show expenses over ₹5000
python main.py --report over_threshold --threshold 5000

# Use custom database
python main.py --db my_expenses.db --report all
```

### 4. Combined Operations

Import data and generate reports in one command:

```bash
python main.py --import_csv expenses.csv --report all
```

## CSV Format

The CSV file must have these columns:
- `date` - Date in YYYY-MM-DD format
- `category` - Expense category (e.g., Food, Transport, Shopping)
- `description` - Brief description of the expense
- `amount` - Amount spent (decimal number)

Example:
```csv
date,category,description,amount
2025-01-15,Food,Coffee,150.00
2025-01-15,Transport,Bus ticket,45.00
2025-01-16,Shopping,Books,1250.00
```

## Report Examples

### Spending by Category
```
SPENDING BY CATEGORY
====================

Category     | Transactions | Total      | Average
-------------|--------------|------------|--------
Food         | 45           | ₹45,892.35 | ₹1,019.83
Transport    | 38           | ₹22,456.78 | ₹591.02
Shopping     | 22           | ₹61,234.56 | ₹2,783.39
```

### Monthly Spending
```
MONTHLY SPENDING
================

Month   | Transactions | Total Spent
--------|--------------|------------
2025-01 | 156          | ₹1,62,345.67
2024-12 | 143          | ₹1,49,387.43
2024-11 | 134          | ₹1,37,856.89
```

### Top 10 Biggest Expenses
```
TOP 10 BIGGEST EXPENSES
=======================

Date       | Category | Description    | Amount
-----------|----------|----------------|--------
2025-01-10 | Travel   | Flight tickets | ₹45,789.00
2025-01-05 | Shopping | Laptop         | ₹28,567.89
2024-12-25 | Food     | Holiday dinner | ₹12,234.56
```

## Database Schema

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    UNIQUE(date, category, description, amount)
);
```

## Command-Line Options

### generate_data.py
- `num_records` - Number of records to generate (default: 100)
- `--output` - Output CSV filename (default: expenses.csv)

### main.py
- `--db` - Database path (default: expenses.db)
- `--import_csv` - CSV file path to import
- `--report` - Report type: by_category, monthly, biggest, over_threshold, all
- `--threshold` - Amount threshold for filtering in ₹ (default: 100)

## Terminal Testing Commands

### Quick Start (Complete Workflow)
```bash
# 1. Generate sample data
python generate_data.py 200

# 2. Import and view all reports
python main.py --import_csv expenses.csv --report all

# 3. View specific reports
python main.py --report by_category
python main.py --report monthly
python main.py --report biggest
```

### Step-by-Step Testing
```bash
# Generate different amounts of data
python generate_data.py 50
python generate_data.py 500
python generate_data.py 1000

# Import data
python main.py --import_csv expenses.csv

# Test individual reports
python main.py --report by_category
python main.py --report monthly  
python main.py --report biggest
python main.py --report over_threshold --threshold 5000
python main.py --report over_threshold --threshold 10000

# Test with custom database
python main.py --db test_expenses.db --import_csv expenses.csv
python main.py --db test_expenses.db --report all
```

### Advanced Testing
```bash
# Generate multiple datasets
python generate_data.py 100 --output small_expenses.csv
python generate_data.py 1000 --output large_expenses.csv

# Import different datasets
python main.py --db small.db --import_csv small_expenses.csv --report all
python main.py --db large.db --import_csv large_expenses.csv --report all

# Test duplicate prevention
python main.py --import_csv expenses.csv  # First import
python main.py --import_csv expenses.csv  # Second import (should show duplicates skipped)

# Test different thresholds
python main.py --report over_threshold --threshold 1000
python main.py --report over_threshold --threshold 15000
python main.py --report over_threshold --threshold 25000
```

### Verification Commands
```bash
# Check if files were created
ls -la *.csv *.db

# Check database content (if you have sqlite3 installed)
sqlite3 expenses.db "SELECT COUNT(*) FROM expenses;"
sqlite3 expenses.db "SELECT category, COUNT(*) FROM expenses GROUP BY category;"

# View help for all options
python generate_data.py --help
python main.py --help
```

## New GUI Interface

### Installation for GUI
```bash
# Install matplotlib for charts
pip install matplotlib
```

### Running the GUI Application
```bash
python gui_app.py
```

### GUI Features
- **Import CSV**: Click "Import CSV File" to load expense data
- **Interactive Analysis**: Select different analysis types with radio buttons
- **Multiple Chart Types**: Choose between bar charts, pie charts, and line charts
- **Real-time Updates**: Data and charts update automatically
- **Threshold Filtering**: Set custom threshold amounts for expense filtering

### Available Analysis Types
1. **Spending by Category** - View total spending grouped by expense categories
2. **Monthly Trends** - Track spending patterns over months
3. **Top 10 Expenses** - See your biggest individual expenses
4. **Expenses Over Threshold** - Filter expenses above a specified amount
5. **Daily Patterns** - Analyze spending by day of the week
6. **Category Monthly Breakdown** - Detailed month-by-month category analysis

### Analysis Tab Features
1. **Monthly Category Breakdown**: 
   - Leave month field empty to see all data
   - Enter specific month (YYYY-MM) to filter by month
   
2. **Top 10 Expenses**: 
   - Choose "Overall" for all-time top expenses
   - Choose "Monthly" and specify month for monthly top expenses
   
3. **Daily Spending Pattern**: 
   - Leave date range empty to see all data
   - Specify date range to filter specific period
   
4. **Expenses Above Threshold**: 
   - Leave threshold empty to see top 15 expenses
   - Set threshold amount to filter expensive items
   - Optionally set date range for period-specific analysis

### Chart Improvements
- Better color schemes and formatting
- Proper scaling and proportions
- Value labels on charts
- Grid lines for better readability
- Currency formatting on axes
- Legends with amount details for pie charts

## Quick Start with GUI

1. **Generate sample data**:
   ```bash
   python generate_data.py 200
   ```

2. **Launch GUI**:
   ```bash
   python gui_app.py
   ```

3. **Import data**: Click "Import CSV File" and select `expenses.csv`

4. **Explore**: Select different analysis types and chart formats to visualize your spending patterns

The GUI provides an intuitive interface for analyzing expenses with interactive charts and real-time data updates, all using Python standard libraries plus matplotlib for visualization.

## Tips

1. **Start with fake data**: Use `generate_data.py` to create test data
2. **Import once**: The system prevents duplicate imports automatically
3. **Regular backups**: Copy your `.db` file to backup your data
4. **Custom categories**: Edit `generate_data.py` to add your own expense categories
5. **SQL queries**: Check `queries.sql` for additional analysis ideas

## Troubleshooting

- **"CSV file not found"**: Check the file path and ensure the CSV exists
- **"No data found"**: Import CSV data first before running reports
- **Import errors**: Verify CSV format matches the expected columns and amounts are in ₹
- **Permission errors**: Ensure write permissions in the project directory

## License

This project is open source and available under the MIT License.
