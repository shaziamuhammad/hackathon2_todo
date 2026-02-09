"""
AI Agent for Todo Task Management
Uses OpenRouter Chat Completions API with function calling
"""
from openai import AsyncOpenAI
from typing import Dict, Any, List, Optional
import os
import json
import logging
from app.core.config import settings

# Set up logging
logger = logging.getLogger(__name__)

# Initialize OpenRouter client (OpenAI-compatible API)
client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)
logger.info("OpenRouter client initialized for AI agent")

# Assistant instructions (now used as system message)
SYSTEM_MESSAGE = """You are an AI-powered todo task management assistant. You help users manage their tasks through natural language conversations.

Your capabilities:
- Create new tasks with titles, descriptions, priorities, due dates, tags, and recurrence patterns
- List and filter tasks by completion status, priority, status, or tags
- Update existing tasks (title, description, priority, status, tags, due dates)
- Delete tasks
- Mark tasks as complete or incomplete
- Sort tasks by various fields (created_at, due_date, priority, title)

When users ask to create tasks:
- Extract the task title (required)
- Identify optional details: description, priority (low/medium/high/urgent), due date, tags, recurrence
- For recurring tasks, parse patterns like "weekly", "monthly", "every 2 weeks"
- Always confirm what you're creating before executing

When users ask to list tasks:
- Apply appropriate filters based on their request
- Sort results in a logical way (e.g., by due date for upcoming tasks, by priority for important tasks)
- Present results in a clear, organized format

When users ask to update or delete tasks:
- If multiple tasks match, ask for clarification
- Confirm the action before executing

Be conversational, helpful, and proactive in understanding user intent. If something is unclear, ask clarifying questions.

Priority levels: low, medium, high, urgent
Status values: pending, in-progress, complete
Date format: Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
"""

# MCP tool definitions as OpenAI functions
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user creating the task"
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (required)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Task priority. Default: medium"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of tags"
                    },
                    "recurrence_pattern": {
                        "type": "object",
                        "description": "Optional recurrence pattern (e.g., {\"frequency\": \"weekly\", \"interval\": 1})"
                    }
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for a user with optional filtering and sorting",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "Filter by completion status (true/false/null for all)"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Filter by priority"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in-progress", "complete"],
                        "description": "Filter by status"
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag (tasks containing this tag)"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["created_at", "due_date", "priority", "title"],
                        "description": "Field to sort by. Default: created_at"
                    },
                    "sort_order": {
                        "type": "string",
                        "enum": ["asc", "desc"],
                        "description": "Sort order. Default: desc"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "New priority"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in-progress", "complete"],
                        "description": "New status"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "New tags list"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in ISO format"
                    },
                    "recurrence_pattern": {
                        "type": "object",
                        "description": "New recurrence pattern"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_complete",
            "description": "Mark a task as complete or incomplete",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The UUID of the user"
                    },
                    "task_id": {
                        "type": "string",
                        "description": "The UUID of the task"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "True to mark complete, False to mark incomplete. Default: True"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]


class TodoAssistant:
    """OpenRouter Chat Completions Assistant for Todo Task Management"""

    def __init__(self):
        self.client = client
        self.tool_handlers = None
        self.model = "openai/gpt-3.5-turbo"  # Default model, can be changed
        self.conversations = {}  # Store conversation history per thread_id

    async def initialize(self, tool_handlers: Dict[str, Any]):
        """
        Initialize the assistant with MCP tool handlers

        Args:
            tool_handlers: Dictionary mapping tool names to their handler functions
        """
        self.tool_handlers = tool_handlers
        logger.info(f"TodoAssistant initialized with model: {self.model}")
        return self

    async def create_thread(self) -> str:
        """Create a new conversation thread (generate unique ID)"""
        import uuid
        thread_id = str(uuid.uuid4())
        self.conversations[thread_id] = []
        return thread_id

    async def add_message(self, thread_id: str, content: str) -> Dict[str, Any]:
        """Add a user message to the thread"""
        if thread_id not in self.conversations:
            self.conversations[thread_id] = []

        message = {"role": "user", "content": content}
        self.conversations[thread_id].append(message)
        return message

    async def run_assistant(self, thread_id: str, user_id: str) -> str:
        """
        Run the assistant and handle tool calls

        Args:
            thread_id: The conversation thread ID
            user_id: The user ID for tool execution

        Returns:
            The assistant's response text
        """
        if thread_id not in self.conversations:
            raise Exception(f"Thread {thread_id} not found")

        # Build messages with system message
        messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
        messages.extend(self.conversations[thread_id])

        max_iterations = 10  # Prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            try:
                # Call the chat completion API
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=TOOL_DEFINITIONS,
                    tool_choice="auto"
                )

                assistant_message = response.choices[0].message

                # Check if the assistant wants to call functions
                if assistant_message.tool_calls:
                    # Add assistant message to conversation
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": tc.type,
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })

                    # Execute tool calls
                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        # Add user_id to function args
                        function_args["user_id"] = user_id

                        # Execute the tool
                        if function_name in self.tool_handlers:
                            try:
                                result = await self.tool_handlers[function_name](**function_args)
                                tool_result = json.dumps(result)
                            except Exception as e:
                                tool_result = json.dumps({"error": str(e)})
                        else:
                            tool_result = json.dumps({"error": f"Unknown function: {function_name}"})

                        # Add tool response to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result
                        })

                    # Continue loop to get final response
                    continue

                else:
                    # No more tool calls, we have the final response
                    response_text = assistant_message.content or "I apologize, but I couldn't generate a response."

                    # Add assistant response to conversation history
                    self.conversations[thread_id].append({
                        "role": "assistant",
                        "content": response_text
                    })

                    return response_text

            except Exception as e:
                logger.error(f"Error in run_assistant: {str(e)}")
                raise Exception(f"Failed to get response from AI: {str(e)}")

        # If we hit max iterations
        return "I apologize, but I encountered an issue processing your request. Please try again."


# Import asyncio for sleep
import asyncio


# Singleton instance
_assistant_instance = None


async def get_assistant(tool_handlers: Dict[str, Any]) -> TodoAssistant:
    """Get or create the assistant instance"""
    global _assistant_instance

    if _assistant_instance is None:
        _assistant_instance = TodoAssistant()
        await _assistant_instance.initialize(tool_handlers)

    return _assistant_instance
