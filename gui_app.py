import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1400x900")
        
        self.db_path = "expenses.db"
        self.create_database()
        
        self.setup_gui()
        
    def create_database(self):
        """Create database and table if they don't exist"""
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
        
    def setup_gui(self):
        """Setup the main GUI with tabs"""
        # Main title
        title_label = ttk.Label(self.root, text="Personal Expense Tracker", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: All Expenses
        self.create_all_expenses_tab()
        
        # Tab 2: Visualizations
        self.create_visualizations_tab()
        
        # Tab 3: Analysis
        self.create_analysis_tab()
        
        # Tab 4: SQL Runner
        self.create_sql_runner_tab()
        
    def create_all_expenses_tab(self):
        """Create tab showing all expenses in a data table"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="All Expenses")
        
        # Control panel
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="Refresh Data", command=self.refresh_all_expenses).pack(side=tk.LEFT)
        
        # Data table
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        self.all_expenses_tree = ttk.Treeview(table_frame, columns=("Date", "Category", "Description", "Amount"), show="headings")
        self.all_expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.all_expenses_tree.heading("Date", text="Date")
        self.all_expenses_tree.heading("Category", text="Category")
        self.all_expenses_tree.heading("Description", text="Description")
        self.all_expenses_tree.heading("Amount", text="Amount (₹)")
        
        self.all_expenses_tree.column("Date", width=100)
        self.all_expenses_tree.column("Category", width=120)
        self.all_expenses_tree.column("Description", width=200)
        self.all_expenses_tree.column("Amount", width=120)
        
        # Scrollbar
        scrollbar1 = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.all_expenses_tree.yview)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        self.all_expenses_tree.configure(yscrollcommand=scrollbar1.set)
        
        # Load initial data
        self.refresh_all_expenses()
        
    def create_visualizations_tab(self):
        """Create tab with category-based visualizations"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Visualizations")
        
        # Control panel
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Chart Type:").pack(side=tk.LEFT, padx=5)
        
        self.viz_chart_type = tk.StringVar(value="pie")
        ttk.Radiobutton(control_frame, text="Pie Chart", variable=self.viz_chart_type, value="pie", command=self.update_visualizations).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="Bar Chart", variable=self.viz_chart_type, value="bar", command=self.update_visualizations).pack(side=tk.LEFT, padx=5)
        
        # Chart area
        self.viz_fig, self.viz_ax = plt.subplots(figsize=(10, 6))
        self.viz_canvas = FigureCanvasTkAgg(self.viz_fig, master=frame)
        self.viz_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Load initial chart
        self.update_visualizations()
        
    def create_analysis_tab(self):
        """Create tab with analysis options"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Analysis")
        
        # Left panel - Controls
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Analysis type selection
        ttk.Label(left_frame, text="Analysis Type:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        self.analysis_type = tk.StringVar(value="monthly_category")
        
        ttk.Radiobutton(left_frame, text="Monthly Category Breakdown", variable=self.analysis_type, value="monthly_category", command=self.update_analysis).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(left_frame, text="Top 10 Expenses", variable=self.analysis_type, value="top_10", command=self.update_analysis).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(left_frame, text="Daily Spending Pattern", variable=self.analysis_type, value="daily_pattern", command=self.update_analysis).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(left_frame, text="Expenses Above Threshold", variable=self.analysis_type, value="threshold", command=self.update_analysis).pack(anchor=tk.W, pady=2)
        
        # Parameters frame
        params_frame = ttk.LabelFrame(left_frame, text="Parameters", padding=10)
        params_frame.pack(fill=tk.X, pady=20)
        
        # Month selection
        ttk.Label(params_frame, text="Month (YYYY-MM):").pack(anchor=tk.W)
        self.month_var = tk.StringVar(value="2025-01")
        ttk.Entry(params_frame, textvariable=self.month_var, width=15).pack(anchor=tk.W, pady=(0, 10))
        
        # Top 10 scope
        ttk.Label(params_frame, text="Top 10 Scope:").pack(anchor=tk.W)
        self.top10_scope = tk.StringVar(value="overall")
        ttk.Radiobutton(params_frame, text="Overall", variable=self.top10_scope, value="overall").pack(anchor=tk.W)
        ttk.Radiobutton(params_frame, text="Monthly", variable=self.top10_scope, value="monthly").pack(anchor=tk.W, pady=(0, 10))
        
        # Threshold
        ttk.Label(params_frame, text="Threshold Amount (₹):").pack(anchor=tk.W)
        self.threshold_var = tk.StringVar(value="5000")
        ttk.Entry(params_frame, textvariable=self.threshold_var, width=15).pack(anchor=tk.W, pady=(0, 10))
        
        # Date range for threshold
        ttk.Label(params_frame, text="Date Range (optional):").pack(anchor=tk.W)
        ttk.Label(params_frame, text="From:").pack(anchor=tk.W)
        self.date_from_var = tk.StringVar(value="2024-01-01")
        ttk.Entry(params_frame, textvariable=self.date_from_var, width=15).pack(anchor=tk.W)
        ttk.Label(params_frame, text="To:").pack(anchor=tk.W)
        self.date_to_var = tk.StringVar(value="2025-12-31")
        ttk.Entry(params_frame, textvariable=self.date_to_var, width=15).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Button(params_frame, text="Update Analysis", command=self.update_analysis).pack(fill=tk.X)
        
        # Right panel - Results
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Analysis chart
        self.analysis_fig, self.analysis_ax = plt.subplots(figsize=(8, 6))
        self.analysis_canvas = FigureCanvasTkAgg(self.analysis_fig, master=right_frame)
        self.analysis_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Load initial analysis
        self.update_analysis()
        
    def create_sql_runner_tab(self):
        """Create tab for custom SQL queries"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="SQL Runner")
        
        # Top frame - Query input
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(top_frame, text="Enter SQL Query:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Query text area
        self.sql_query_text = tk.Text(top_frame, height=8, wrap=tk.WORD)
        self.sql_query_text.pack(fill=tk.X, pady=5)
        
        # Default query
        default_query = "SELECT date, category, description, amount FROM expenses ORDER BY date DESC LIMIT 20;"
        self.sql_query_text.insert("1.0", default_query)
        
        # Execute button
        ttk.Button(top_frame, text="Execute Query", command=self.execute_custom_query).pack(pady=5)
        
        # Bottom frame - Results
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(bottom_frame, text="Query Results:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Results table
        self.sql_results_tree = ttk.Treeview(bottom_frame, show="headings")
        self.sql_results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for SQL results
        scrollbar2 = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=self.sql_results_tree.yview)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.sql_results_tree.configure(yscrollcommand=scrollbar2.set)
        
    def refresh_all_expenses(self):
        """Refresh the all expenses table"""
        # Clear existing data
        for item in self.all_expenses_tree.get_children():
            self.all_expenses_tree.delete(item)
        
        # Fetch and display data
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT date, category, description, amount FROM expenses ORDER BY date DESC")
        results = cursor.fetchall()
        conn.close()
        
        for row in results:
            formatted_row = (row[0], row[1], row[2], f"₹{row[3]:.2f}")
            self.all_expenses_tree.insert("", "end", values=formatted_row)
            
    def update_visualizations(self):
        """Update category visualization"""
        self.viz_ax.clear()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            self.viz_ax.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=self.viz_ax.transAxes)
            self.viz_canvas.draw()
            return
            
        categories = [row[0] for row in results]
        amounts = [row[1] for row in results]
        
        if self.viz_chart_type.get() == "pie":
            # Create pie chart with better formatting
            wedges, texts, autotexts = self.viz_ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                                     startangle=90, textprops={'fontsize': 10})
            
            # Improve text positioning
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            self.viz_ax.set_title('Expenses by Category (Share %)', fontsize=14, fontweight='bold', pad=20)
            
            # Add legend with amounts
            legend_labels = [f'{cat}: ₹{amt:.0f}' for cat, amt in zip(categories, amounts)]
            self.viz_ax.legend(wedges, legend_labels, title="Categories", loc="center left", 
                             bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
        else:
            # Create HORIZONTAL bar chart to avoid label overlapping issues
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD']
            
            # Reverse data so highest amounts appear at the top
            categories_reversed = categories[::-1]
            amounts_reversed = amounts[::-1]
            
            # Create horizontal bars
            y_positions = range(len(categories_reversed))
            bars = self.viz_ax.barh(y_positions, amounts_reversed, color=colors[:len(categories_reversed)], 
                                  height=0.6, edgecolor='white', linewidth=1.2)
            
            # Set title and labels
            self.viz_ax.set_title('Total Amount per Category', fontsize=16, fontweight='bold', pad=25)
            self.viz_ax.set_xlabel('Amount (₹)', fontsize=14, fontweight='bold')
            self.viz_ax.set_ylabel('Categories', fontsize=14, fontweight='bold')
            
            # Set y-axis labels (categories) - no rotation needed for horizontal bars
            self.viz_ax.set_yticks(y_positions)
            self.viz_ax.set_yticklabels(categories_reversed, fontsize=12)
            
            # Format x-axis (amounts)
            self.viz_ax.tick_params(axis='x', labelsize=11)
            self.viz_ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
            
            # Add value labels at the end of bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                self.viz_ax.text(width + width*0.02, bar.get_y() + bar.get_height()/2.,
                               f'₹{width:,.0f}', ha='left', va='center', 
                               fontsize=11, fontweight='bold', color='black')
            
            # Add grid for better readability
            self.viz_ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.8)
            self.viz_ax.set_axisbelow(True)
            
            # Set proper margins and limits
            self.viz_ax.set_xlim(0, max(amounts) * 1.15)
            self.viz_ax.margins(y=0.02)
            
            # Improve overall appearance
            self.viz_ax.spines['top'].set_visible(False)
            self.viz_ax.spines['right'].set_visible(False)
            self.viz_ax.spines['left'].set_linewidth(1.2)
            self.viz_ax.spines['bottom'].set_linewidth(1.2)
        
        # Adjust layout with proper spacing
        self.viz_fig.subplots_adjust(left=0.25, bottom=0.1, right=0.85, top=0.9)
        self.viz_canvas.draw()
        
    def update_analysis(self):
        """Update analysis based on selected type"""
        self.analysis_ax.clear()
        
        analysis_type = self.analysis_type.get()
        
        if analysis_type == "monthly_category":
            self.monthly_category_analysis()
        elif analysis_type == "top_10":
            self.top_10_analysis()
        elif analysis_type == "daily_pattern":
            self.daily_pattern_analysis()
        elif analysis_type == "threshold":
            self.threshold_analysis()
            
        self.analysis_fig.tight_layout()
        self.analysis_canvas.draw()
        
    def monthly_category_analysis(self):
        """Monthly category breakdown"""
        month = self.month_var.get().strip()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if month:
            cursor.execute('''
                SELECT category, SUM(amount) as total
                FROM expenses
                WHERE strftime('%Y-%m', date) = ?
                GROUP BY category
                ORDER BY total DESC
            ''', (month,))
            title = f'Category Breakdown for {month}'
        else:
            cursor.execute('''
                SELECT category, SUM(amount) as total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
            ''')
            title = 'Category Breakdown (All Data)'
            
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            self.analysis_ax.text(0.5, 0.5, f'No data available', ha='center', va='center', 
                                transform=self.analysis_ax.transAxes, fontsize=12)
            return
            
        categories = [row[0] for row in results]
        amounts = [row[1] for row in results]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
        bars = self.analysis_ax.bar(categories, amounts, color=colors[:len(categories)])
        
        self.analysis_ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        self.analysis_ax.set_ylabel('Amount (₹)', fontsize=12)
        self.analysis_ax.set_xlabel('Categories', fontsize=12)
        self.analysis_ax.tick_params(axis='x', rotation=45, labelsize=10)
        self.analysis_ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:.0f}'))
        
        for bar in bars:
            height = bar.get_height()
            self.analysis_ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                                f'₹{height:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        self.analysis_ax.grid(axis='y', alpha=0.3, linestyle='--')
        self.analysis_ax.set_axisbelow(True)
                                
    def top_10_analysis(self):
        """Top 10 expenses analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if self.top10_scope.get() == "monthly":
            month = self.month_var.get().strip()
            if month:
                cursor.execute('''
                    SELECT date, category, description, amount
                    FROM expenses
                    WHERE strftime('%Y-%m', date) = ?
                    ORDER BY amount DESC
                    LIMIT 10
                ''', (month,))
                title = f'Top 10 Expenses for {month}'
            else:
                cursor.execute('''
                    SELECT date, category, description, amount
                    FROM expenses
                    ORDER BY amount DESC
                    LIMIT 10
                ''')
                title = 'Top 10 Expenses (All Data)'
        else:
            cursor.execute('''
                SELECT date, category, description, amount
                FROM expenses
                ORDER BY amount DESC
                LIMIT 10
            ''')
            title = 'Top 10 Expenses (Overall)'
            
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            self.analysis_ax.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                                transform=self.analysis_ax.transAxes, fontsize=12)
            return
            
        descriptions = [f"{row[2][:20]}..." if len(row[2]) > 20 else row[2] for row in results]
        amounts = [row[3] for row in results]
        
        # Reverse order for better display (highest at top)
        descriptions.reverse()
        amounts.reverse()
        
        bars = self.analysis_ax.barh(descriptions, amounts, color='orange', alpha=0.8)
        self.analysis_ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        self.analysis_ax.set_xlabel('Amount (₹)', fontsize=12)
        self.analysis_ax.tick_params(axis='both', labelsize=10)
        
        for bar in bars:
            width = bar.get_width()
            self.analysis_ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2.,
                                f'₹{width:.0f}', ha='left', va='center', fontsize=9, fontweight='bold')
        
        self.analysis_ax.grid(axis='x', alpha=0.3, linestyle='--')
        self.analysis_ax.set_axisbelow(True)
                                
    def daily_pattern_analysis(self):
        """Daily spending pattern"""
        # Get optional date range
        date_from = self.date_from_var.get().strip()
        date_to = self.date_to_var.get().strip()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if date_from and date_to:
            cursor.execute('''
                SELECT date, SUM(amount) as total
                FROM expenses
                WHERE date >= ? AND date <= ?
                GROUP BY date
                ORDER BY date
            ''', (date_from, date_to))
            title = f'Daily Spending Pattern ({date_from} to {date_to})'
        else:
            cursor.execute('''
                SELECT date, SUM(amount) as total
                FROM expenses
                GROUP BY date
                ORDER BY date
            ''')
            title = 'Daily Spending Pattern (All Data)'
            
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            self.analysis_ax.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                                transform=self.analysis_ax.transAxes, fontsize=12)
            return
            
        dates = [row[0] for row in results]
        amounts = [row[1] for row in results]
        
        self.analysis_ax.plot(dates, amounts, marker='o', linewidth=2, markersize=6, 
                            color='#4ECDC4', markerfacecolor='#FF6B6B', markeredgecolor='white', markeredgewidth=2)
        self.analysis_ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        self.analysis_ax.set_ylabel('Amount (₹)', fontsize=12)
        self.analysis_ax.tick_params(axis='x', rotation=45, labelsize=9)
        self.analysis_ax.tick_params(axis='y', labelsize=10)
        self.analysis_ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:.0f}'))
        
        # Show only every nth date label to avoid crowding
        if len(dates) > 15:
            step = max(1, len(dates) // 15)
            tick_positions = range(0, len(dates), step)
            self.analysis_ax.set_xticks(tick_positions)
            self.analysis_ax.set_xticklabels([dates[i] for i in tick_positions])
        
        self.analysis_ax.grid(True, alpha=0.3, linestyle='--')
        self.analysis_ax.set_axisbelow(True)
            
    def threshold_analysis(self):
        """Expenses above threshold"""
        threshold_str = self.threshold_var.get().strip()
        date_from = self.date_from_var.get().strip()
        date_to = self.date_to_var.get().strip()
        
        # If no threshold specified, use 0 (show all expenses)
        threshold = float(threshold_str) if threshold_str else 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build query based on what parameters are provided
        if date_from and date_to:
            if threshold > 0:
                cursor.execute('''
                    SELECT date, category, description, amount
                    FROM expenses
                    WHERE amount > ? AND date >= ? AND date <= ?
                    ORDER BY amount DESC
                    LIMIT 15
                ''', (threshold, date_from, date_to))
                title = f'Expenses Above ₹{threshold} ({date_from} to {date_to})'
            else:
                cursor.execute('''
                    SELECT date, category, description, amount
                    FROM expenses
                    WHERE date >= ? AND date <= ?
                    ORDER BY amount DESC
                    LIMIT 15
                ''', (date_from, date_to))
                title = f'Top Expenses ({date_from} to {date_to})'
        else:
            if threshold > 0:
                cursor.execute('''
                    SELECT date, category, description, amount
                    FROM expenses
                    WHERE amount > ?
                    ORDER BY amount DESC
                    LIMIT 15
                ''', (threshold,))
                title = f'Expenses Above ₹{threshold} (All Data)'
            else:
                cursor.execute('''
                    SELECT date, category, description, amount
                    FROM expenses
                    ORDER BY amount DESC
                    LIMIT 15
                ''')
                title = 'Top 15 Expenses (All Data)'
                
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            message = f'No expenses above ₹{threshold}' if threshold > 0 else 'No data available'
            self.analysis_ax.text(0.5, 0.5, message, ha='center', va='center', 
                                transform=self.analysis_ax.transAxes, fontsize=12)
            return
            
        descriptions = [f"{row[2][:15]}..." if len(row[2]) > 15 else row[2] for row in results]
        amounts = [row[3] for row in results]
        
        # Reverse for better display
        descriptions.reverse()
        amounts.reverse()
        
        bars = self.analysis_ax.barh(descriptions, amounts, color='red', alpha=0.7)
        self.analysis_ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        self.analysis_ax.set_xlabel('Amount (₹)', fontsize=12)
        self.analysis_ax.tick_params(axis='both', labelsize=10)
        
        for bar in bars:
            width = bar.get_width()
            self.analysis_ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2.,
                                f'₹{width:.0f}', ha='left', va='center', fontsize=9, fontweight='bold')
        
        self.analysis_ax.grid(axis='x', alpha=0.3, linestyle='--')
        self.analysis_ax.set_axisbelow(True)
                                
    def execute_custom_query(self):
        """Execute custom SQL query"""
        query = self.sql_query_text.get("1.0", tk.END).strip()
        
        if not query:
            messagebox.showwarning("Warning", "Please enter a SQL query")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [description[0] for description in cursor.description] if cursor.description else []
            results = cursor.fetchall()
            conn.close()
            
            # Clear existing results
            for item in self.sql_results_tree.get_children():
                self.sql_results_tree.delete(item)
            
            # Configure columns
            self.sql_results_tree["columns"] = columns
            self.sql_results_tree["show"] = "headings"
            
            for col in columns:
                self.sql_results_tree.heading(col, text=col)
                self.sql_results_tree.column(col, width=120, anchor="center")
            
            # Insert results
            for row in results:
                formatted_row = []
                for item in row:
                    if isinstance(item, float):
                        formatted_row.append(f"₹{item:.2f}")
                    else:
                        formatted_row.append(str(item))
                self.sql_results_tree.insert("", "end", values=formatted_row)
                
            messagebox.showinfo("Success", f"Query executed successfully. {len(results)} rows returned.")
            
        except Exception as e:
            messagebox.showerror("SQL Error", f"Error executing query:\n{str(e)}")

def main():
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
def main():
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
