-- Personal Expense Tracker - SQL Queries

-- 1. Total expenses by category (sorted by largest first)
SELECT 
    category,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM expenses
GROUP BY category
ORDER BY total_amount DESC;

-- 2. Monthly total spending
SELECT 
    strftime('%Y-%m', date) as month,
    COUNT(*) as transactions,
    SUM(amount) as total_spent,
    AVG(amount) as avg_per_transaction
FROM expenses
GROUP BY strftime('%Y-%m', date)
ORDER BY month DESC;

-- 3. Top 10 biggest expenses
SELECT date, category, description, amount
FROM expenses
ORDER BY amount DESC
LIMIT 10;

-- 4. Expenses over a threshold (e.g., ₹5000)
SELECT date, category, description, amount
FROM expenses
WHERE amount > 5000
ORDER BY amount DESC;

-- 5. Daily spending pattern (by day of week)
SELECT 
    CASE strftime('%w', date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END as day_of_week,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM expenses
GROUP BY strftime('%w', date)
ORDER BY strftime('%w', date);

-- 6. Recent expenses (last 30 days)
SELECT date, category, description, amount
FROM expenses
WHERE date >= date('now', '-30 days')
ORDER BY date DESC;

-- 7. Category breakdown by month
SELECT 
    strftime('%Y-%m', date) as month,
    category,
    COUNT(*) as transactions,
    SUM(amount) as total
FROM expenses
GROUP BY strftime('%Y-%m', date), category
ORDER BY month DESC, total DESC;

-- 8. Most frequent expense descriptions
SELECT 
    description,
    category,
    COUNT(*) as frequency,
    AVG(amount) as avg_amount,
    SUM(amount) as total_amount
FROM expenses
GROUP BY description, category
ORDER BY frequency DESC
LIMIT 20;

-- 9. Summary statistics
SELECT 
    COUNT(*) as total_transactions,
    SUM(amount) as total_spent,
    AVG(amount) as avg_per_transaction,
    MIN(amount) as smallest_expense,
    MAX(amount) as largest_expense,
    MIN(date) as first_expense_date,
    MAX(date) as last_expense_date
FROM expenses;

-- 10. Find outliers (expenses 2 standard deviations above mean)
WITH stats AS (
    SELECT 
        AVG(amount) as mean_amount,
        (SUM((amount - (SELECT AVG(amount) FROM expenses)) * 
             (amount - (SELECT AVG(amount) FROM expenses))) / 
         (COUNT(*) - 1)) as variance
    FROM expenses
)
SELECT 
    date, category, description, amount,
    ROUND((amount - stats.mean_amount) / SQRT(stats.variance), 2) as std_deviations
FROM expenses, stats
WHERE amount > (stats.mean_amount + 2 * SQRT(stats.variance))
ORDER BY amount DESC;
