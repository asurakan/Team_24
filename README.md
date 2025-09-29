# Employee Management System - MVC Architecture

A complete CRUD (Create, Read, Update, Delete) application built using the Model-View-Controller (MVC) architecture pattern for managing employees and departments in a SQLite database.

## 🏗️ Architecture Overview

This application demonstrates professional software architecture with clear separation of concerns:

### **Model Layer** (`models.py`)
- **DatabaseConnection**: Handles SQLite database connections and basic operations
- **EmployeeModel**: Manages all employee-related database operations
- **DepartmentModel**: Manages all department-related database operations

### **View Layer** (`views.py`)
- **BaseView**: Common display methods and input validation
- **EmployeeView**: User interface for employee operations
- **DepartmentView**: User interface for department operations
- **MainMenuView**: Main menu and navigation interface

### **Controller Layer** (`controllers.py`)
- **EmployeeController**: Business logic for employee operations
- **DepartmentController**: Business logic for department operations
- **MainController**: Coordinates all operations and manages application flow

## 🚀 Features

### Employee Management
- ✅ **View All Employees** - Display all employees with department info
- ✅ **View Employee Details** - Show detailed information for a specific employee
- ✅ **Add New Employee** - Create new employee records
- ✅ **Update Employee** - Modify existing employee information
- ✅ **Delete Employee** - Remove employee records
- ✅ **Search Employees** - Find employees by name pattern

### Department Management
- ✅ **View All Departments** - Display all departments
- ✅ **View Department Details** - Show department info and assigned employees
- ✅ **Add New Department** - Create new departments
- ✅ **Update Department** - Modify department names
- ✅ **Delete Department** - Remove departments (with validation)

### System Features
- ✅ **Statistics Dashboard** - View employee and salary statistics
- ✅ **Data Validation** - Input validation and error handling
- ✅ **Confirmation Dialogs** - User confirmation for destructive operations
- ✅ **Clean Interface** - Console-based menu system with clear navigation

## 📊 Database Schema

### Departments Table
```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
```

### Employees Table
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER,
    salary REAL,
    hire_date TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

## 🎯 Sample Data

The application comes with sample data:

**Departments:**
- HR
- Engineering  
- Sales

**Employees:**
- Alice Smith (HR, $60,000, hired 2020-01-15)
- Bob Johnson (Engineering, $80,000, hired 2019-03-22)
- Carol Lee (Engineering, $95,000, hired 2018-07-10)
- David Kim (Sales, $55,000, hired 2021-11-01)
- Eva Brown (HR, $62,000, hired 2022-05-18)

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses built-in SQLite)

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd employee-management-mvc
   ```

2. **Run the application:**
   ```bash
   python employee_management_app.py
   ```

3. **Follow the menu prompts** to navigate through the application

### Testing the Application

1. **Test all components:**
   ```bash
   python test_mvc_components.py
   ```

2. **See feature demonstration:**
   ```bash
   python demo_mvc_app.py
   ```

## 🔧 Key MVC Benefits Demonstrated

### **Separation of Concerns**
- **Models** handle only data operations
- **Views** handle only user interface
- **Controllers** handle only business logic

### **Maintainability**
- Easy to modify database operations without touching UI
- Easy to change UI without affecting business logic
- Easy to add new features by extending existing classes

### **Testability**
- Each component can be tested independently
- Models can be tested with mock data
- Controllers can be tested with mock models and views

### **Reusability**
- Models can be reused in different applications
- Views can be adapted for different interfaces (web, desktop)
- Controllers can be reused with different data sources

## 📁 Project Structure

```
employee-management-mvc/
├── employee_management_app.py    # Main application entry point
├── models.py                     # Database models and operations
├── views.py                      # User interface components
├── controllers.py                # Business logic controllers
├── test_mvc_components.py        # Component testing script
├── demo_mvc_app.py               # Feature demonstration script
├── employees.db                  # SQLite database file
├── .gitignore                    # Git ignore file
└── README.md                     # This documentation
```

## 🎨 User Interface Features

- **Clear Menu Navigation** - Intuitive menu system
- **Input Validation** - Comprehensive input validation and error handling
- **Confirmation Dialogs** - User confirmation for destructive operations
- **Formatted Output** - Clean, readable data display
- **Error Messages** - Clear error messages with helpful guidance
- **Success Feedback** - Confirmation messages for successful operations

## 🔒 Data Integrity Features

- **Foreign Key Constraints** - Maintains referential integrity
- **Input Validation** - Validates data types and formats
- **Business Rules** - Prevents deletion of departments with assigned employees
- **Duplicate Prevention** - Prevents duplicate department names
- **Date Validation** - Validates hire date format

## 🚀 Future Enhancements

Potential improvements that could be added:

- **Web Interface** - Convert to web application using Flask/Django
- **Data Export** - Export data to CSV/Excel
- **Advanced Search** - Search by multiple criteria
- **Reporting** - Generate detailed reports
- **User Authentication** - Add user login system
- **Audit Trail** - Track all changes made to data
- **Data Backup** - Automatic database backup functionality

## 🐛 Troubleshooting

### Common Issues

1. **Database Locked Error**
   - Ensure no other application is using the database
   - Check file permissions

2. **Import Errors**
   - Ensure all Python files are in the same directory
   - Check Python version compatibility

3. **Permission Errors**
   - Run with appropriate file permissions
   - Check database file is writable

### Getting Help

If you encounter issues:
1. Check the error messages displayed by the application
2. Verify database file exists and is accessible
3. Ensure Python 3.6+ is installed
4. Check file permissions in the application directory

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

If you have any questions or suggestions, please feel free to reach out.

---

**Built with ❤️ using Python and SQLite**

*This project demonstrates professional MVC architecture implementation with complete CRUD functionality, data validation, error handling, and a clean user interface.*