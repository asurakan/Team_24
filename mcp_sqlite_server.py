#!/usr/bin/env python3
"""
Simple MCP Server for SQLite Database Operations
This server provides tools to interact with the employees.db database
"""

import asyncio
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Try to import MCP, fall back to basic implementation if not available
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolRequest,
        CallToolResult,
        ListToolsRequest,
        ListToolsResult,
        Tool,
        TextContent,
    )
    MCP_AVAILABLE = True
except ImportError:
    print("MCP package not available. Creating basic server implementation.")
    MCP_AVAILABLE = False
    
    # Basic fallback classes
    class Server:
        def __init__(self, name):
            self.name = name
            self.list_tools = None
            self.call_tool = None
        
        def get_capabilities(self, notification_options=None, experimental_capabilities=None):
            return {}
    
    class Tool:
        def __init__(self, name, description, inputSchema):
            self.name = name
            self.description = description
            self.inputSchema = inputSchema
    
    class CallToolRequest:
        def __init__(self, name, arguments):
            self.name = name
            self.arguments = arguments
    
    class CallToolResult:
        def __init__(self, content):
            self.content = content
    
    class ListToolsRequest:
        pass
    
    class ListToolsResult:
        def __init__(self, tools):
            self.tools = tools
    
    class TextContent:
        def __init__(self, type, text):
            self.type = type
            self.text = text
    
    class InitializationOptions:
        def __init__(self, server_name, server_version, capabilities):
            self.server_name = server_name
            self.server_version = server_version
            self.capabilities = capabilities
    
    async def stdio_server():
        # Basic stdio server implementation
        return (sys.stdin, sys.stdout)

# Database path
DB_PATH = Path(__file__).parent / "employees.db"

class SQLiteMCPServer:
    def __init__(self):
        self.server = Server("sqlite-employees")
        self.db_path = DB_PATH
        
        # Register handlers
        self.server.list_tools = self.list_tools
        self.server.call_tool = self.call_tool
        
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def execute_modification(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        """Execute INSERT/UPDATE/DELETE query and return result info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
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
    
    async def list_tools(self, request: ListToolsRequest) -> ListToolsResult:
        """List available tools"""
        tools = [
            Tool(
                name="query_employees",
                description="Query employees from the database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL SELECT query to execute on employees table"
                        },
                        "params": {
                            "type": "array",
                            "description": "Parameters for the query",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="query_departments",
                description="Query departments from the database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL SELECT query to execute on departments table"
                        },
                        "params": {
                            "type": "array",
                            "description": "Parameters for the query",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="execute_sql",
                description="Execute any SQL query (SELECT, INSERT, UPDATE, DELETE)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to execute"
                        },
                        "params": {
                            "type": "array",
                            "description": "Parameters for the query",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="get_schema",
                description="Get the database schema information",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="get_table_info",
                description="Get information about a specific table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to get info about"
                        }
                    },
                    "required": ["table_name"]
                }
            )
        ]
        return ListToolsResult(tools=tools)
    
    async def call_tool(self, request: CallToolRequest) -> CallToolResult:
        """Handle tool calls"""
        try:
            if request.name == "query_employees":
                query = request.arguments.get("query", "")
                params = tuple(request.arguments.get("params", []))
                results = self.execute_query(query, params)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(results, indent=2))]
                )
            
            elif request.name == "query_departments":
                query = request.arguments.get("query", "")
                params = tuple(request.arguments.get("params", []))
                results = self.execute_query(query, params)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(results, indent=2))]
                )
            
            elif request.name == "execute_sql":
                query = request.arguments.get("query", "")
                params = tuple(request.arguments.get("params", []))
                
                # Determine if it's a SELECT query or modification
                query_upper = query.strip().upper()
                if query_upper.startswith("SELECT"):
                    results = self.execute_query(query, params)
                    return CallToolResult(
                        content=[TextContent(type="text", text=json.dumps(results, indent=2))]
                    )
                else:
                    result = self.execute_modification(query, params)
                    return CallToolResult(
                        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
                    )
            
            elif request.name == "get_schema":
                schema_query = "SELECT sql FROM sqlite_master WHERE type='table'"
                schema_results = self.execute_query(schema_query)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(schema_results, indent=2))]
                )
            
            elif request.name == "get_table_info":
                table_name = request.arguments.get("table_name", "")
                info_query = f"PRAGMA table_info({table_name})"
                info_results = self.execute_query(info_query)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(info_results, indent=2))]
                )
            
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {request.name}")]
                )
                
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

async def main():
    """Main function to run the MCP server"""
    sqlite_server = SQLiteMCPServer()
    
    if MCP_AVAILABLE:
        # Run the full MCP server
        async with stdio_server() as (read_stream, write_stream):
            await sqlite_server.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="sqlite-employees",
                    server_version="1.0.0",
                    capabilities=sqlite_server.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )
    else:
        # Run basic server for testing
        print("Running in basic mode (MCP package not available)")
        print("Available tools:")
        tools_result = await sqlite_server.list_tools(ListToolsRequest())
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Keep server running for testing
        print("\nServer ready. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    asyncio.run(main())
