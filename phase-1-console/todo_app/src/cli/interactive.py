"""
Interactive menu-based CLI for the Todo application.
"""

from ..services.todo_service import TodoService


class InteractiveTodoCLI:
    def __init__(self):
        self.service = TodoService()

    def run(self):
        while True:
            print("\n=== Todo Application (Interactive) ===")
            print("1. Add task")
            print("2. List tasks")
            print("3. Update task")
            print("4. Delete task")
            print("5. Mark task complete/incomplete")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.list_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.mark_task()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

    def add_task(self):
        title = input("Title: ").strip()
        description = input("Description: ").strip()
        task = self.service.add_task(title, description)
        print(f"Added task {task.id}")

    def list_tasks(self):
        tasks = self.service.view_tasks()
        if not tasks:
            print("No tasks found.")
            return
        for t in tasks:
            status = "✓" if t.completed else "○"
            print(f"[{status}] {t.id} | {t.title}")

    def update_task(self):
        task_id = input("Task ID: ").strip()
        title = input("New title (Enter to skip): ").strip()
        description = input("New description (Enter to skip): ").strip()
        self.service.update_task(task_id, title or None, description or None)

    def delete_task(self):
        task_id = input("Task ID: ").strip()
        self.service.delete_task(task_id)

    def mark_task(self):
        task_id = input("Task ID: ").strip()
        choice = input("1 = Complete, 2 = Incomplete: ").strip()
        if choice == "1":
            self.service.mark_task_complete(task_id)
        elif choice == "2":
            self.service.mark_task_incomplete(task_id)


def main():
    cli = InteractiveTodoCLI()
    cli.run()


if __name__ == "__main__":
    main()

