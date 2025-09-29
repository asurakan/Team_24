#!/usr/bin/env python3
"""
Controller classes for Employee Management System
Handles business logic and coordinates between Models and Views
"""

from typing import List, Dict, Any, Optional
from models import DatabaseConnection, EmployeeModel, DepartmentModel
from views import EmployeeView, DepartmentView, MainMenuView

class EmployeeController:
    """Controller for Employee operations"""
    
    def __init__(self, employee_model: EmployeeModel, department_model: DepartmentModel, 
                 employee_view: EmployeeView, main_view: MainMenuView):
        self.employee_model = employee_model
        self.department_model = department_model
        self.employee_view = employee_view
        self.main_view = main_view
    
    def view_all_employees(self):
        """Display all employees"""
        try:
            employees = self.employee_model.get_all()
            self.employee_view.display_employees(employees)
        except Exception as e:
            self.main_view.display_error_message(f"Failed to retrieve employees: {str(e)}")
    
    def view_employee_details(self):
        """Display specific employee details"""
        try:
            emp_id = self.employee_view.get_employee_id()
            employee = self.employee_model.get_by_id(emp_id)
            self.employee_view.display_employee_detail(employee)
        except Exception as e:
            self.main_view.display_error_message(f"Failed to retrieve employee: {str(e)}")
    
    def add_employee(self):
        """Add a new employee"""
        try:
            departments = self.department_model.get_all()
            if not departments:
                self.main_view.display_error_message("No departments available. Please add a department first.")
                return
            
            employee_data = self.employee_view.get_employee_data(departments)
            
            # Validate hire date format
            try:
                from datetime import datetime
                datetime.strptime(employee_data['hire_date'], '%Y-%m-%d')
            except ValueError:
                self.main_view.display_error_message("Invalid date format. Please use YYYY-MM-DD.")
                return
            
            result = self.employee_model.create(**employee_data)
            self.main_view.display_success_message(f"Employee '{employee_data['name']}' added successfully!")
            
        except Exception as e:
            self.main_view.display_error_message(f"Failed to add employee: {str(e)}")
    
    def update_employee(self):
        """Update an existing employee"""
        try:
            emp_id = self.employee_view.get_employee_id()
            employee = self.employee_model.get_by_id(emp_id)
            
            if not employee:
                self.main_view.display_error_message("Employee not found.")
                return
            
            self.employee_view.display_employee_detail(employee)
            
            if not self.main_view.display_confirmation_message("Do you want to update this employee?"):
                return
            
            departments = self.department_model.get_all()
            employee_data = self.employee_view.get_employee_data(departments, employee)
            
            # Validate hire date format
            try:
                from datetime import datetime
                datetime.strptime(employee_data['hire_date'], '%Y-%m-%d')
            except ValueError:
                self.main_view.display_error_message("Invalid date format. Please use YYYY-MM-DD.")
                return
            
            result = self.employee_model.update(emp_id, **employee_data)
            self.main_view.display_success_message(f"Employee '{employee_data['name']}' updated successfully!")
            
        except Exception as e:
            self.main_view.display_error_message(f"Failed to update employee: {str(e)}")
    
    def delete_employee(self):
        """Delete an employee"""
        try:
            emp_id = self.employee_view.get_employee_id()
            employee = self.employee_model.get_by_id(emp_id)
            
            if not employee:
                self.main_view.display_error_message("Employee not found.")
                return
            
            self.employee_view.display_employee_detail(employee)
            
            if not self.main_view.display_confirmation_message("Are you sure you want to delete this employee?"):
                return
            
            result = self.employee_model.delete(emp_id)
            self.main_view.display_success_message(f"Employee '{employee['name']}' deleted successfully!")
            
        except Exception as e:
            self.main_view.display_error_message(f"Failed to delete employee: {str(e)}")
    
    def search_employees(self):
        """Search employees by name"""
        try:
            search_term = self.employee_view.get_search_term()
            if not search_term:
                self.main_view.display_error_message("Search term cannot be empty.")
                return
            
            employees = self.employee_model.search_by_name(search_term)
            self.employee_view.display_employees(employees)
            
        except Exception as e:
            self.main_view.display_error_message(f"Failed to search employees: {str(e)}")
    
    def run_employee_menu(self):
        """Run the employee management menu"""
        while True:
            self.main_view.clear_screen()
            self.main_view.display_employee_menu()
            
            choice = self.main_view.get_menu_choice(7)
            
            if choice == 1:
                self.view_all_employees()
            elif choice == 2:
                self.view_employee_details()
            elif choice == 3:
                self.add_employee()
            elif choice == 4:
                self.update_employee()
            elif choice == 5:
                self.delete_employee()
            elif choice == 6:
                self.search_employees()
            elif choice == 7:
                break
            
            if choice != 7:
                input("\nPress Enter to continue...")

class DepartmentController:
    """Controller for Department operations"""
    
    def __init__(self, department_model: DepartmentModel, employee_model: EmployeeModel,
                 department_view: DepartmentView, main_view: MainMenuView):
        self.department_model = department_model
        self.employee_model = employee_model
        self.department_view = department_view
        self.main_view = main_view
    
    def view_all_departments(self):
        """Display all departments"""
        try:
            departments = self.department_model.get_all()
            self.department_view.display_departments(departments)
        except Exception as e:
            self.main_view.display_error_message(f"Failed to retrieve departments: {str(e)}")
    
    def view_department_details(self):
        """Display specific department details"""
        try:
            dept_id = self.department_view.get_department_id()
            department = self.department_model.get_by_id(dept_id)
            self.department_view.display_department_detail(department)
            
            if department:
                # Show employees in this department
                employees = self.employee_model.get_by_department(dept_id)
                if employees:
                    print(f"\nEmployees in {department['name']}:")
                    for emp in employees:
                        print(f"  - {emp['name']} (${emp['salary']:,.2f})")
                else:
                    print(f"\nNo employees in {department['name']}")
                    
        except Exception as e:
            self.main_view.display_error_message(f"Failed to retrieve department: {str(e)}")
    
    def add_department(self):
        """Add a new department"""
        try:
            department_data = self.department_view.get_department_data()
            
            # Check if department already exists
            existing = self.department_model.get_by_name(department_data['name'])
            if existing:
                self.main_view.display_error_message(f"Department '{department_data['name']}' already exists.")
                return
            
            result = self.department_model.create(department_data['name'])
            self.main_view.display_success_message(f"Department '{department_data['name']}' added successfully!")
            
        except Exception as e:
            self.main_view.display_error_message(f"Failed to add department: {str(e)}")
    
    def update_department(self):
        """Update an existing department"""
        try:
            dept_id = self.department_view.get_department_id()
            department = self.department_model.get_by_id(dept_id)
            
            if not department:
                self.main_view.display_error_message("Department not found.")
                return
            
            self.department_view.display_department_detail(department)
            
            if not self.main_view.display_confirmation_message("Do you want to update this department?"):
                return
            
            department_data = self.department_view.get_department_data(department)
            
            # Check if new name already exists
            existing = self.department_model.get_by_name(department_data['name'])
            if existing and existing['id'] != dept_id:
                self.main_view.display_error_message(f"Department '{department_data['name']}' already exists.")
                return
            
            result = self.department_model.update(dept_id, department_data['name'])
            self.main_view.display_success_message(f"Department '{department_data['name']}' updated successfully!")
            
        except Exception as e:
            self.main_view.display_error_message(f"Failed to update department: {str(e)}")
    
    def delete_department(self):
        """Delete a department"""
        try:
            dept_id = self.department_view.get_department_id()
            department = self.department_model.get_by_id(dept_id)
            
            if not department:
                self.main_view.display_error_message("Department not found.")
                return
            
            self.department_view.display_department_detail(department)
            
            if not self.main_view.display_confirmation_message("Are you sure you want to delete this department?"):
                return
            
            result = self.department_model.delete(dept_id)
            self.main_view.display_success_message(f"Department '{department['name']}' deleted successfully!")
            
        except Exception as e:
            self.main_view.display_error_message(f"Failed to delete department: {str(e)}")
    
    def run_department_menu(self):
        """Run the department management menu"""
        while True:
            self.main_view.clear_screen()
            self.main_view.display_department_menu()
            
            choice = self.main_view.get_menu_choice(6)
            
            if choice == 1:
                self.view_all_departments()
            elif choice == 2:
                self.view_department_details()
            elif choice == 3:
                self.add_department()
            elif choice == 4:
                self.update_department()
            elif choice == 5:
                self.delete_department()
            elif choice == 6:
                break
            
            if choice != 6:
                input("\nPress Enter to continue...")

class MainController:
    """Main controller that coordinates all operations"""
    
    def __init__(self, db_path: str):
        # Initialize database connection and models
        self.db_connection = DatabaseConnection(db_path)
        self.employee_model = EmployeeModel(self.db_connection)
        self.department_model = DepartmentModel(self.db_connection)
        
        # Initialize views
        self.employee_view = EmployeeView()
        self.department_view = DepartmentView()
        self.main_view = MainMenuView()
        
        # Initialize controllers
        self.employee_controller = EmployeeController(
            self.employee_model, self.department_model, 
            self.employee_view, self.main_view
        )
        self.department_controller = DepartmentController(
            self.department_model, self.employee_model,
            self.department_view, self.main_view
        )
    
    def view_statistics(self):
        """Display system statistics"""
        try:
            stats = self.employee_model.get_statistics()
            self.main_view.display_statistics(stats)
        except Exception as e:
            self.main_view.display_error_message(f"Failed to retrieve statistics: {str(e)}")
    
    def run(self):
        """Run the main application"""
        while True:
            self.main_view.clear_screen()
            self.main_view.display_main_menu()
            
            choice = self.main_view.get_menu_choice(4)
            
            if choice == 1:
                self.employee_controller.run_employee_menu()
            elif choice == 2:
                self.department_controller.run_department_menu()
            elif choice == 3:
                self.view_statistics()
                input("\nPress Enter to continue...")
            elif choice == 4:
                print("\nThank you for using the Employee Management System!")
                break
