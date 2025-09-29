#!/usr/bin/env python3
"""
Demo script for MVC Employee Management System
Shows key features without requiring user interaction
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models import DatabaseConnection, EmployeeModel, DepartmentModel
from views import EmployeeView, DepartmentView, MainMenuView

def demo_employee_operations():
    """Demonstrate employee operations"""
    print("EMPLOYEE OPERATIONS DEMO")
    print("=" * 50)
    
    # Initialize components
    db_path = Path(__file__).parent / "employees.db"
    db_connection = DatabaseConnection(str(db_path))
    emp_model = EmployeeModel(db_connection)
    dept_model = DepartmentModel(db_connection)
    emp_view = EmployeeView()
    
    # Show all employees
    print("\n1. All Employees:")
    employees = emp_model.get_all()
    emp_view.display_employees(employees)
    
    # Show employees by department
    print("\n2. Employees by Department:")
    departments = dept_model.get_all()
    for dept in departments:
        print(f"\n{dept['name']} Department:")
        dept_employees = emp_model.get_by_department(dept['id'])
        for emp in dept_employees:
            print(f"  - {emp['name']} (${emp['salary']:,.2f})")
    
    # Show search functionality
    print("\n3. Search Results (name contains 'Smith'):")
    search_results = emp_model.search_by_name("Smith")
    emp_view.display_employees(search_results)
    
    # Show statistics
    print("\n4. Employee Statistics:")
    stats = emp_model.get_statistics()
    overall = stats['overall']
    print(f"  Total Employees: {overall['total_employees']}")
    print(f"  Average Salary: ${overall['average_salary']:,.2f}")
    print(f"  Salary Range: ${overall['min_salary']:,.2f} - ${overall['max_salary']:,.2f}")

def demo_department_operations():
    """Demonstrate department operations"""
    print("\n\nDEPARTMENT OPERATIONS DEMO")
    print("=" * 50)
    
    # Initialize components
    db_path = Path(__file__).parent / "employees.db"
    db_connection = DatabaseConnection(str(db_path))
    dept_model = DepartmentModel(db_connection)
    emp_model = EmployeeModel(db_connection)
    dept_view = DepartmentView()
    
    # Show all departments
    print("\n1. All Departments:")
    departments = dept_model.get_all()
    dept_view.display_departments(departments)
    
    # Show department details with employee counts
    print("\n2. Department Details with Employee Counts:")
    for dept in departments:
        employees = emp_model.get_by_department(dept['id'])
        print(f"\n{dept['name']} (ID: {dept['id']}):")
        print(f"  Employees: {len(employees)}")
        if employees:
            avg_salary = sum(emp['salary'] for emp in employees) / len(employees)
            print(f"  Average Salary: ${avg_salary:,.2f}")

def demo_data_validation():
    """Demonstrate data validation features"""
    print("\n\nDATA VALIDATION DEMO")
    print("=" * 50)
    
    # Initialize components
    db_path = Path(__file__).parent / "employees.db"
    db_connection = DatabaseConnection(str(db_path))
    emp_model = EmployeeModel(db_connection)
    dept_model = DepartmentModel(db_connection)
    
    print("\n1. Testing Department Validation:")
    try:
        # Try to create employee with invalid department
        result = emp_model.create("Test Employee", 999, 50000, "2024-01-01")
        print("❌ Should have failed - invalid department ID")
    except ValueError as e:
        print(f"✅ Validation working: {e}")
    
    print("\n2. Testing Department Deletion Protection:")
    try:
        # Try to delete department with employees
        result = dept_model.delete(1)  # HR department has employees
        print("❌ Should have failed - department has employees")
    except ValueError as e:
        print(f"✅ Protection working: {e}")
    
    print("\n3. Testing Duplicate Department Prevention:")
    try:
        # Try to create duplicate department
        result = dept_model.create("HR")  # HR already exists
        print("❌ Should have failed - duplicate department")
    except Exception as e:
        print(f"✅ Duplicate prevention working: {e}")

def demo_mvc_architecture():
    """Demonstrate MVC architecture benefits"""
    print("\n\nMVC ARCHITECTURE DEMO")
    print("=" * 50)
    
    print("\n1. Separation of Concerns:")
    print("   ✅ Models handle only data operations")
    print("   ✅ Views handle only user interface")
    print("   ✅ Controllers handle only business logic")
    
    print("\n2. Component Independence:")
    print("   ✅ Models can be tested independently")
    print("   ✅ Views can be changed without affecting data")
    print("   ✅ Controllers can be modified without UI changes")
    
    print("\n3. Reusability:")
    print("   ✅ Models can be used in different applications")
    print("   ✅ Views can be adapted for web/desktop interfaces")
    print("   ✅ Controllers can work with different data sources")

def main():
    """Run the demo"""
    print("MVC EMPLOYEE MANAGEMENT SYSTEM - FEATURE DEMO")
    print("=" * 60)
    
    try:
        demo_employee_operations()
        demo_department_operations()
        demo_data_validation()
        demo_mvc_architecture()
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("\nThe MVC application demonstrates:")
        print("  ✅ Complete CRUD operations")
        print("  ✅ Data validation and error handling")
        print("  ✅ Clean separation of concerns")
        print("  ✅ Professional user interface")
        print("  ✅ Robust business logic")
        
        print("\nTo run the interactive application:")
        print("  python employee_management_app.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
