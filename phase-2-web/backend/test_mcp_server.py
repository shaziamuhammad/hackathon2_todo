"""
Test script for MCP Server
Verifies all MCP tools are properly exposed and functional
"""
import asyncio
import sys
from datetime import datetime
from typing import Dict, Any


async def test_add_task():
    """Test add_task tool"""
    print("\n=== Testing add_task ===")

    # Import the tool function
    from mcp_server import add_task

    # Test basic task
    result = await add_task(
        user_id="test-user-123",
        title="Test Task",
        description="This is a test task",
        priority="high"
    )

    assert result["status"] == "success", "add_task should return success"
    assert "Test Task" in result["message"], "Response should mention task title"
    assert result["task"]["title"] == "Test Task", "Task should have correct title"
    assert result["task"]["priority"] == "high", "Task should have correct priority"

    print("[PASS] Basic task creation works")

    # Test task with due date and recurrence
    result = await add_task(
        user_id="test-user-123",
        title="Recurring Task",
        priority="medium",
        tags=["work", "important"],
        due_date="2026-02-15T10:00:00",
        recurrence_pattern={"type": "weekly", "interval": 1}
    )

    assert result["status"] == "success", "add_task with recurrence should succeed"
    assert result["task"]["recurrence_pattern"]["type"] == "weekly", "Recurrence pattern should be preserved"
    assert len(result["task"]["tags"]) == 2, "Tags should be preserved"

    print("[PASS] Task with due date and recurrence works")
    print("[PASS] add_task: PASSED")


async def test_delete_task():
    """Test delete_task tool"""
    print("\n=== Testing delete_task ===")

    from mcp_server import delete_task

    result = await delete_task(
        user_id="test-user-123",
        task_id="task-456"
    )

    assert result["status"] == "success", "delete_task should return success"
    assert result["task_id"] == "task-456", "Should return correct task_id"

    print("[PASS] delete_task: PASSED")


async def test_update_task():
    """Test update_task tool"""
    print("\n=== Testing update_task ===")

    from mcp_server import update_task

    # Test updating multiple fields
    result = await update_task(
        user_id="test-user-123",
        task_id="task-789",
        title="Updated Title",
        priority="urgent",
        status="in-progress",
        tags=["updated", "test"]
    )

    assert result["status"] == "success", "update_task should return success"
    assert result["task_id"] == "task-789", "Should return correct task_id"
    assert len(result["updates"]) == 4, "Should have 4 updates"
    assert result["updates"]["priority"] == "urgent", "Priority should be updated"

    print("[PASS] Multiple field updates work")

    # Test updating single field
    result = await update_task(
        user_id="test-user-123",
        task_id="task-789",
        completed=True
    )

    assert result["status"] == "success", "Single field update should succeed"
    assert len(result["updates"]) == 1, "Should have 1 update"

    print("[PASS] Single field update works")
    print("[PASS] update_task: PASSED")


async def test_list_tasks():
    """Test list_tasks tool"""
    print("\n=== Testing list_tasks ===")

    from mcp_server import list_tasks

    # Test basic listing
    result = await list_tasks(
        user_id="test-user-123"
    )

    assert result["status"] == "success", "list_tasks should return success"
    assert "tasks" in result, "Should return tasks array"
    assert "count" in result, "Should return count"

    print("[PASS] Basic listing works")

    # Test with filters
    result = await list_tasks(
        user_id="test-user-123",
        priority="high",
        status="pending",
        tag="work",
        sort_by="due_date",
        order="asc",
        limit=50
    )

    assert result["status"] == "success", "Filtered listing should succeed"
    assert result["filters"]["priority"] == "high", "Priority filter should be preserved"
    assert result["filters"]["status"] == "pending", "Status filter should be preserved"
    assert result["sort_by"] == "due_date", "Sort field should be preserved"
    assert result["order"] == "asc", "Sort order should be preserved"

    print("[PASS] Filtered and sorted listing works")
    print("[PASS] list_tasks: PASSED")


async def test_mark_complete():
    """Test mark_complete tool"""
    print("\n=== Testing mark_complete ===")

    from mcp_server import mark_complete

    result = await mark_complete(
        user_id="test-user-123",
        task_id="task-999"
    )

    assert result["status"] == "success", "mark_complete should return success"
    assert result["task_id"] == "task-999", "Should return correct task_id"
    assert result["completed"] == True, "Should mark as completed"
    assert "completed_at" in result, "Should include completion timestamp"

    # Verify timestamp is valid ISO format
    try:
        datetime.fromisoformat(result["completed_at"])
        print("[PASS] Completion timestamp is valid ISO format")
    except ValueError:
        raise AssertionError("Completion timestamp should be valid ISO format")

    print("[PASS] mark_complete: PASSED")


async def test_search_tasks():
    """Test search_tasks tool"""
    print("\n=== Testing search_tasks ===")

    from mcp_server import search_tasks

    result = await search_tasks(
        user_id="test-user-123",
        query="meeting"
    )

    assert result["status"] == "success", "search_tasks should return success"
    assert result["query"] == "meeting", "Should preserve search query"
    assert "tasks" in result, "Should return tasks array"
    assert "count" in result, "Should return count"

    print("[PASS] search_tasks: PASSED")


async def run_all_tests():
    """Run all MCP server tests"""
    print("=" * 60)
    print("MCP Server Tool Tests")
    print("=" * 60)

    tests = [
        test_add_task,
        test_delete_task,
        test_update_task,
        test_list_tasks,
        test_mark_complete,
        test_search_tasks
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            await test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__}: ERROR - {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print("\n[WARNING] Some tests failed. Please review the errors above.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All MCP server tools are working correctly!")
        sys.exit(0)


if __name__ == "__main__":
    print("\nStarting MCP Server Tool Tests...")
    print("This script tests all 6 MCP tools without requiring a running server.\n")

    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
