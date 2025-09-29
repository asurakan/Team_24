#!/usr/bin/env python3
"""
Employee Management System - Main Application
MVC Architecture Implementation

This application provides a complete CRUD interface for managing employees and departments
in a SQLite database using the Model-View-Controller pattern.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from controllers import MainController

def check_database_exists(db_path: str) -> bool:
    """Check if the database file exists"""
    return Path(db_path).exists()

def create_sample_data(db_path: str):
    """Create sample data if database doesn't exist"""
    import sqlite3
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department_id INTEGER,
            salary REAL,
            hire_date TEXT,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)
    
    # Insert sample departments
    departments = [
        ('HR',),
        ('Engineering',),
        ('Sales',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO departments (name) VALUES (?)", departments)
    
    # Insert sample employees
    employees = [
        ('Alice Smith', 1, 60000.0, '2020-01-15'),
        ('Bob Johnson', 2, 80000.0, '2019-03-22'),
        ('Carol Lee', 2, 95000.0, '2018-07-10'),
        ('David Kim', 3, 55000.0, '2021-11-01'),
        ('Eva Brown', 1, 62000.0, '2022-05-18')
    ]
    cursor.executemany("INSERT OR IGNORE INTO employees (name, department_id, salary, hire_date) VALUES (?, ?, ?, ?)", employees)
    
    conn.commit()
    conn.close()

def main():
    """Main application entry point"""
    print("Employee Management System")
    print("=" * 40)
    
    # Database path
    db_path = current_dir / "employees.db"
    
    # Check if database exists, create sample data if not
    if not check_database_exists(db_path):
        print("Database not found. Creating sample database...")
        create_sample_data(db_path)
        print("Sample database created successfully!")
        print()
    
    try:
        # Initialize and run the main controller
        app = MainController(str(db_path))
        app.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        print("Please check your database file and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
