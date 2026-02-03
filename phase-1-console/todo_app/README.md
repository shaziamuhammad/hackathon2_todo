# Phase I: In-Memory Python Console Todo App

This is a simple command-line Todo application.
All tasks are stored in memory and are lost when the program exits.

## How to Run

Open terminal and go to the project directory:

cd phase-1-console/todo_app

## Usage Commands

Add a task:
python -m src.cli.main add "Task Title" -d "Task Description"

List all tasks:
python -m src.cli.main list

Update a task:
python -m src.cli.main update <task-id> --title "New Title" --description "New Description"

Delete a task:
python -m src.cli.main delete <task-id>

Mark task as complete:
python -m src.cli.main complete <task-id>

Mark task as incomplete:
python -m src.cli.main incomplete <task-id>

## Project Structure

src/models/task.py  
Contains the Task data model.

src/services/todo_service.py  
Contains business logic for managing tasks.

src/cli/main.py  
Handles command-line input and output.
