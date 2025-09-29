#!/usr/bin/env python3
"""
View classes for Employee Management System
Handles all user interface and display logic
"""

from typing import List, Dict, Any, Optional
import sys

class BaseView:
    """Base view class with common display methods"""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title: str):
        """Print a formatted header"""
        print("=" * 60)
        print(f" {title}")
        print("=" * 60)
    
    @staticmethod
    def print_separator():
        """Print a separator line"""
        print("-" * 60)
    
    @staticmethod
    def get_input(prompt: str, required: bool = True) -> str:
        """Get user input with validation"""
        while True:
            value = input(f"{prompt}: ").strip()
            if value or not required:
                return value
            print("This field is required. Please try again.")
    
    @staticmethod
    def get_numeric_input(prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
        """Get numeric input with validation"""
        while True:
            try:
                value = float(input(f"{prompt}: "))
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number.")
    
    @staticmethod
    def get_integer_input(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
        """Get integer input with validation"""
        while True:
            try:
                value = int(input(f"{prompt}: "))
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid integer.")
    
    @staticmethod
    def confirm_action(message: str) -> bool:
        """Get confirmation from user"""
        response = input(f"{message} (y/n): ").lower().strip()
        return response in ['y', 'yes']

class EmployeeView(BaseView):
    """View for Employee operations"""
    
    def display_employees(self, employees: List[Dict[str, Any]]):
        """Display a list of employees"""
        if not employees:
            print("No employees found.")
            return
        
        print(f"\nFound {len(employees)} employee(s):")
        self.print_separator()
        print(f"{'ID':<4} {'Name':<20} {'Department':<15} {'Salary':<10} {'Hire Date':<12}")
        print("-" * 70)
        
        for emp in employees:
            salary = f"${emp['salary']:,.2f}" if emp['salary'] else "N/A"
            dept_name = emp.get('department_name', 'Unknown')
            print(f"{emp['id']:<4} {emp['name']:<20} {dept_name:<15} {salary:<10} {emp['hire_date']:<12}")
    
    def display_employee_detail(self, employee: Dict[str, Any]):
        """Display detailed employee information"""
        if not employee:
            print("Employee not found.")
            return
        
        self.print_header("Employee Details")
        print(f"ID: {employee['id']}")
        print(f"Name: {employee['name']}")
        print(f"Department: {employee.get('department_name', 'Unknown')}")
        print(f"Salary: ${employee['salary']:,.2f}" if employee['salary'] else "Salary: N/A")
        print(f"Hire Date: {employee['hire_date']}")
    
    def get_employee_data(self, departments: List[Dict[str, Any]], employee: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get employee data from user input"""
        self.print_header("Employee Information")
        
        # Name
        name = self.get_input("Employee Name", required=True)
        
        # Department selection
        print("\nAvailable Departments:")
        for dept in departments:
            print(f"{dept['id']}. {dept['name']}")
        
        dept_id = self.get_integer_input("Department ID", min_val=1)
        
        # Salary
        salary = self.get_numeric_input("Salary", min_val=0)
        
        # Hire date
        hire_date = self.get_input("Hire Date (YYYY-MM-DD)", required=True)
        
        return {
            'name': name,
            'department_id': dept_id,
            'salary': salary,
            'hire_date': hire_date
        }
    
    def get_employee_id(self) -> int:
        """Get employee ID from user"""
        return self.get_integer_input("Enter Employee ID", min_val=1)
    
    def get_search_term(self) -> str:
        """Get search term from user"""
        return self.get_input("Enter name to search for", required=False)

class DepartmentView(BaseView):
    """View for Department operations"""
    
    def display_departments(self, departments: List[Dict[str, Any]]):
        """Display a list of departments"""
        if not departments:
            print("No departments found.")
            return
        
        print(f"\nFound {len(departments)} department(s):")
        self.print_separator()
        print(f"{'ID':<4} {'Name':<20}")
        print("-" * 25)
        
        for dept in departments:
            print(f"{dept['id']:<4} {dept['name']:<20}")
    
    def display_department_detail(self, department: Dict[str, Any]):
        """Display detailed department information"""
        if not department:
            print("Department not found.")
            return
        
        self.print_header("Department Details")
        print(f"ID: {department['id']}")
        print(f"Name: {department['name']}")
    
    def get_department_data(self, department: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get department data from user input"""
        self.print_header("Department Information")
        
        name = self.get_input("Department Name", required=True)
        
        return {'name': name}
    
    def get_department_id(self) -> int:
        """Get department ID from user"""
        return self.get_integer_input("Enter Department ID", min_val=1)

class MainMenuView(BaseView):
    """View for main menu and navigation"""
    
    def display_main_menu(self):
        """Display the main menu"""
        self.print_header("Employee Management System")
        print("1. Employee Management")
        print("2. Department Management")
        print("3. View Statistics")
        print("4. Exit")
        self.print_separator()
    
    def display_employee_menu(self):
        """Display employee management menu"""
        self.print_header("Employee Management")
        print("1. View All Employees")
        print("2. View Employee Details")
        print("3. Add New Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Search Employees")
        print("7. Back to Main Menu")
        self.print_separator()
    
    def display_department_menu(self):
        """Display department management menu"""
        self.print_header("Department Management")
        print("1. View All Departments")
        print("2. View Department Details")
        print("3. Add New Department")
        print("4. Update Department")
        print("5. Delete Department")
        print("6. Back to Main Menu")
        self.print_separator()
    
    def get_menu_choice(self, max_choice: int) -> int:
        """Get menu choice from user"""
        return self.get_integer_input("Enter your choice", min_val=1, max_val=max_choice)
    
    def display_statistics(self, stats: Dict[str, Any]):
        """Display system statistics"""
        self.print_header("System Statistics")
        
        overall = stats.get('overall', {})
        print(f"Total Employees: {overall.get('total_employees', 0)}")
        print(f"Average Salary: ${overall.get('average_salary', 0):,.2f}")
        print(f"Minimum Salary: ${overall.get('min_salary', 0):,.2f}")
        print(f"Maximum Salary: ${overall.get('max_salary', 0):,.2f}")
        
        print("\nBy Department:")
        self.print_separator()
        print(f"{'Department':<15} {'Employees':<10} {'Avg Salary':<12}")
        print("-" * 40)
        
        for dept_stat in stats.get('by_department', []):
            avg_salary = f"${dept_stat['avg_salary']:,.2f}" if dept_stat['avg_salary'] else "N/A"
            print(f"{dept_stat['department_name']:<15} {dept_stat['employee_count']:<10} {avg_salary:<12}")
    
    def display_success_message(self, message: str):
        """Display success message"""
        print(f"\n✅ {message}")
        input("Press Enter to continue...")
    
    def display_error_message(self, message: str):
        """Display error message"""
        print(f"\n❌ Error: {message}")
        input("Press Enter to continue...")
    
    def display_confirmation_message(self, message: str) -> bool:
        """Display confirmation message and get response"""
        return self.confirm_action(f"\n⚠️  {message}")
