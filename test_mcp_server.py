#!/usr/bin/env python3
"""
Test script for the SQLite MCP Server
This script tests the MCP server functionality
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

async def test_mcp_server():
    """Test the MCP server by running it and checking basic functionality"""
    
    server_path = Path(__file__).parent / "mcp_sqlite_server.py"
    
    print("Testing MCP SQLite Server...")
    print(f"Server path: {server_path}")
    
    # Check if the database exists
    db_path = Path(__file__).parent / "employees.db"
    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return False
    
    print(f"Database found at: {db_path}")
    
    # Test basic SQLite functionality
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM employees")
        employee_count = cursor.fetchone()[0]
        print(f"Employee count: {employee_count}")
        
        cursor.execute("SELECT COUNT(*) FROM departments")
        dept_count = cursor.fetchone()[0]
        print(f"Department count: {dept_count}")
        
        conn.close()
        print("✓ Basic SQLite functionality works")
        
    except Exception as e:
        print(f"ERROR: SQLite test failed: {e}")
        return False
    
    # Test MCP server import
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from mcp_sqlite_server import SQLiteMCPServer
        print("✓ MCP server imports successfully")
        
        # Test server initialization
        server = SQLiteMCPServer()
        print("✓ MCP server initializes successfully")
        
    except Exception as e:
        print(f"ERROR: MCP server test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! The MCP server is ready to use.")
    print("\nTo use this MCP server:")
    print("1. Install dependencies: pip install mcp")
    print("2. Add the mcp_client_config.json to your MCP client configuration")
    print("3. The server provides these tools:")
    print("   - query_employees: Query the employees table")
    print("   - query_departments: Query the departments table") 
    print("   - execute_sql: Execute any SQL query")
    print("   - get_schema: Get database schema")
    print("   - get_table_info: Get table structure")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)
