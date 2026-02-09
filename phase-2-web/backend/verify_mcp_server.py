"""
MCP Server Verification Script
Verifies that the MCP server is properly configured and all tools are registered
"""
import sys


def verify_mcp_server():
    """Verify MCP server configuration and tool registration"""
    print("=" * 60)
    print("MCP Server Verification")
    print("=" * 60)

    try:
        # Import the MCP server
        print("\n[1/3] Importing MCP server module...")
        from mcp_server import mcp
        print("[PASS] MCP server module imported successfully")

        # Check if server is initialized
        print("\n[2/3] Checking server initialization...")
        if mcp is None:
            print("[FAIL] MCP server is not initialized")
            return False
        print(f"[PASS] MCP server initialized: {mcp.name}")

        # List all registered tools
        print("\n[3/3] Checking registered tools...")

        expected_tools = [
            "add_task",
            "delete_task",
            "update_task",
            "list_tasks",
            "mark_complete",
            "search_tasks"
        ]

        # Get registered tools from the MCP server
        registered_tools = []
        if hasattr(mcp, '_tools'):
            registered_tools = list(mcp._tools.keys())
        elif hasattr(mcp, 'tools'):
            registered_tools = list(mcp.tools.keys())

        print(f"\nExpected tools: {len(expected_tools)}")
        print(f"Registered tools: {len(registered_tools)}")

        if len(registered_tools) > 0:
            print("\nRegistered tools:")
            for tool_name in registered_tools:
                status = "[PASS]" if tool_name in expected_tools else "[WARN]"
                print(f"  {status} {tool_name}")

        # Check if all expected tools are registered
        missing_tools = [t for t in expected_tools if t not in registered_tools]
        extra_tools = [t for t in registered_tools if t not in expected_tools]

        if missing_tools:
            print(f"\n[FAIL] Missing tools: {', '.join(missing_tools)}")
            return False

        if extra_tools:
            print(f"\n[WARN] Extra tools found: {', '.join(extra_tools)}")

        print("\n" + "=" * 60)
        print("[SUCCESS] MCP Server Verification Complete")
        print("=" * 60)
        print("\nAll 6 expected tools are properly registered:")
        for tool in expected_tools:
            print(f"  - {tool}")

        print("\nTo start the MCP server, run:")
        print("  python mcp_server.py")
        print("\nThe server will run on port 8001 by default.")

        return True

    except ImportError as e:
        print(f"[FAIL] Failed to import MCP server: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\nVerifying MCP Server Configuration...\n")

    success = verify_mcp_server()

    if success:
        sys.exit(0)
    else:
        print("\n[FAIL] MCP server verification failed")
        sys.exit(1)
