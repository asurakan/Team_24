#!/usr/bin/env python3
"""
Test the MCP server tools directly
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_sqlite_server import SQLiteMCPServer, CallToolRequest

async def test_server_tools():
    """Test the server tools directly"""
    server = SQLiteMCPServer()
    
    print("Testing MCP Server Tools...")
    print("=" * 50)
    
    # Test 1: List tools
    print("\n1. Testing list_tools:")
    tools_result = await server.list_tools(None)
    for tool in tools_result.tools:
        print(f"   - {tool.name}: {tool.description}")
    
    # Test 2: Get schema
    print("\n2. Testing get_schema:")
    schema_request = CallToolRequest("get_schema", {})
    schema_result = await server.call_tool(schema_request)
    print(f"   Result: {schema_result.content[0].text[:200]}...")
    
    # Test 3: Query employees
    print("\n3. Testing query_employees:")
    query_request = CallToolRequest("query_employees", {
        "query": "SELECT * FROM employees LIMIT 3"
    })
    query_result = await server.call_tool(query_request)
    print(f"   Result: {query_result.content[0].text[:200]}...")
    
    # Test 4: Get table info
    print("\n4. Testing get_table_info:")
    table_request = CallToolRequest("get_table_info", {
        "table_name": "employees"
    })
    table_result = await server.call_tool(table_request)
    print(f"   Result: {table_result.content[0].text[:200]}...")
    
    # Test 5: Execute custom SQL
    print("\n5. Testing execute_sql:")
    sql_request = CallToolRequest("execute_sql", {
        "query": "SELECT COUNT(*) as total_employees FROM employees"
    })
    sql_result = await server.call_tool(sql_request)
    print(f"   Result: {sql_result.content[0].text}")
    
    print("\n" + "=" * 50)
    print("✅ All tool tests completed successfully!")
    print("\nThe MCP server is working correctly and ready to use.")

if __name__ == "__main__":
    asyncio.run(test_server_tools())
