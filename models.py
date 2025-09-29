#!/usr/bin/env python3
"""
Model classes for Employee Management System
Handles all database operations using SQLite
"""

import sqlite3
from typing import List, Dict, Optional, Any
from pathlib import Path

class DatabaseConnection:
    """Handles database connection and basic operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory for dict-like access"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def execute_modification(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        """Execute INSERT/UPDATE/DELETE query and return result info"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return {
                "rows_affected": cursor.rowcount,
                "lastrowid": cursor.lastrowid
            }
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

class DepartmentModel:
    """Model for Department operations"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all departments"""
        return self.db.execute_query("SELECT * FROM departments ORDER BY name")
    
    def get_by_id(self, dept_id: int) -> Optional[Dict[str, Any]]:
        """Get department by ID"""
        results = self.db.execute_query("SELECT * FROM departments WHERE id = ?", (dept_id,))
        return results[0] if results else None
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get department by name"""
        results = self.db.execute_query("SELECT * FROM departments WHERE name = ?", (name,))
        return results[0] if results else None
    
    def create(self, name: str) -> Dict[str, Any]:
        """Create a new department"""
        return self.db.execute_modification(
            "INSERT INTO departments (name) VALUES (?)", 
            (name,)
        )
    
    def update(self, dept_id: int, name: str) -> Dict[str, Any]:
        """Update department name"""
        return self.db.execute_modification(
            "UPDATE departments SET name = ? WHERE id = ?", 
            (name, dept_id)
        )
    
    def delete(self, dept_id: int) -> Dict[str, Any]:
        """Delete department (only if no employees are assigned)"""
        # Check if any employees are assigned to this department
        employees = self.db.execute_query(
            "SELECT COUNT(*) as count FROM employees WHERE department_id = ?", 
            (dept_id,)
        )
        
        if employees[0]['count'] > 0:
            raise ValueError(f"Cannot delete department. {employees[0]['count']} employees are still assigned to it.")
        
        return self.db.execute_modification(
            "DELETE FROM departments WHERE id = ?", 
            (dept_id,)
        )

class EmployeeModel:
    """Model for Employee operations"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all employees with department names"""
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e 
            LEFT JOIN departments d ON e.department_id = d.id 
            ORDER BY e.name
        """)
    
    def get_by_id(self, emp_id: int) -> Optional[Dict[str, Any]]:
        """Get employee by ID with department name"""
        results = self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e 
            LEFT JOIN departments d ON e.department_id = d.id 
            WHERE e.id = ?
        """, (emp_id,))
        return results[0] if results else None
    
    def get_by_department(self, dept_id: int) -> List[Dict[str, Any]]:
        """Get all employees in a specific department"""
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e 
            LEFT JOIN departments d ON e.department_id = d.id 
            WHERE e.department_id = ? 
            ORDER BY e.name
        """, (dept_id,))
    
    def search_by_name(self, name_pattern: str) -> List[Dict[str, Any]]:
        """Search employees by name pattern"""
        return self.db.execute_query("""
            SELECT e.*, d.name as department_name 
            FROM employees e 
            LEFT JOIN departments d ON e.department_id = d.id 
            WHERE e.name LIKE ? 
            ORDER BY e.name
        """, (f"%{name_pattern}%",))
    
    def create(self, name: str, department_id: int, salary: float, hire_date: str) -> Dict[str, Any]:
        """Create a new employee"""
        # Validate department exists
        dept = self.db.execute_query("SELECT id FROM departments WHERE id = ?", (department_id,))
        if not dept:
            raise ValueError(f"Department with ID {department_id} does not exist")
        
        return self.db.execute_modification(
            "INSERT INTO employees (name, department_id, salary, hire_date) VALUES (?, ?, ?, ?)", 
            (name, department_id, salary, hire_date)
        )
    
    def update(self, emp_id: int, name: str, department_id: int, salary: float, hire_date: str) -> Dict[str, Any]:
        """Update employee information"""
        # Validate department exists
        dept = self.db.execute_query("SELECT id FROM departments WHERE id = ?", (department_id,))
        if not dept:
            raise ValueError(f"Department with ID {department_id} does not exist")
        
        return self.db.execute_modification(
            "UPDATE employees SET name = ?, department_id = ?, salary = ?, hire_date = ? WHERE id = ?", 
            (name, department_id, salary, hire_date, emp_id)
        )
    
    def delete(self, emp_id: int) -> Dict[str, Any]:
        """Delete employee"""
        return self.db.execute_modification(
            "DELETE FROM employees WHERE id = ?", 
            (emp_id,)
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get employee statistics"""
        stats = self.db.execute_query("""
            SELECT 
                COUNT(*) as total_employees,
                AVG(salary) as average_salary,
                MIN(salary) as min_salary,
                MAX(salary) as max_salary
            FROM employees
        """)
        
        dept_stats = self.db.execute_query("""
            SELECT 
                d.name as department_name,
                COUNT(e.id) as employee_count,
                AVG(e.salary) as avg_salary
            FROM departments d
            LEFT JOIN employees e ON d.id = e.department_id
            GROUP BY d.id, d.name
            ORDER BY employee_count DESC
        """)
        
        return {
            "overall": stats[0] if stats else {},
            "by_department": dept_stats
        }
