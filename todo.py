import orm_sqlite
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

class TodoItem(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)

    task = orm_sqlite.StringField()
    date = orm_sqlite.IntegerField()
    due_date = orm_sqlite.IntegerField()
    completed = orm_sqlite.IntegerField(default=0)

class TodoManager:
    def create_todo_item(task, date, due_date):
        todo_item = TodoItem(task=task, date=date, due_date=due_date, completed=0)
        todo_item.save()
        return todo_item

    def update_todo_item(todo_item_id, task=None, date=None, completed=None):
        todo_item = TodoItem.objects.get(pk=todo_item_id)
        if task:
            todo_item["task"] = task
        if date:
            todo_item["date"] = date
        if completed is not None:
            todo_item["completed"] = 1 if completed else 0
        todo_item.update()
        return todo_item

    def get_todo_items():
        return TodoItem.objects.all()
    
def create_task_list_table(title, tasks, incomplete_only=False, completed_only=False):
    table = Table(title=title)

    table.add_column("ID", justify="center")
    table.add_column("Task", justify="left")
    table.add_column("Created", justify="left")
    table.add_column("Due Date", justify="left")
    table.add_column("Completed", justify="center")

    for task in tasks:
        if incomplete_only and task["completed"] == 1:
            continue
        if completed_only and task["completed"] != 1:
            continue

        table.add_row(str(task["id"]), task["task"], str(task["date"]), str(task["due_date"]), "✅" if task["completed"] == 1 else " ")

    return table

# Initialize DB
db = orm_sqlite.Database('todo.db')
TodoItem.objects.backend = db

os.system('cls||clear')

# Initialize Rich Console
console = Console()

while True:
    console.print("Welcome to the Todo List App!\n", style="bold underline green")

    console.print("Select a choice:", style="bold")
    console.print("1. View All Tasks.")
    console.print("2. View Completed Tasks.")
    console.print("3. View Pending Tasks.")
    console.print("4. Add Task.")
    console.print("5. Update Task.")
    console.print("6. Delete Task.")
    console.print("7. Exit.", end="\n\n")

    console.print("Your choice: ", end="")
    choice = input()

    if choice == "1":
        console.print("\nAll Tasks", style="bold underline red")

        tasks = TodoManager.get_todo_items()

        table = create_task_list_table("Tasks", tasks)
        console.print(table)

    elif choice == "2":
        console.print("\nCompleted Tasks", style="bold underline red")
        completed_tasks = TodoManager.get_todo_items()

        table = create_task_list_table("Completed Tasks", completed_tasks, completed_only=True)
        console.print(table)

    elif choice == "3":
        console.print("\nPending Tasks", style="bold underline red")

        pending_tasks = TodoManager.get_todo_items()

        table = create_task_list_table("Pending Tasks", pending_tasks, incomplete_only=True)
        console.print(table)

    elif choice == "4":
        console.print("\nNew Task", end="\n\n", style="bold underline red")

        console.print("Enter task name: ", end="")
        task = input()

        console.print("Enter task due date: ", end="")
        due_date = input()

        TodoManager.create_todo_item(task, int(datetime.now().timestamp()), due_date)
        console.print("✅ Task added successfully!", style="bold green")

    elif choice == "5":
        console.print("\nUpdate Task", style="bold underline red")

        tasks = TodoManager.get_todo_items()

        table = create_task_list_table("Tasks", tasks)
        console.print(table)

        console.print("Enter task ID to update: ", end="")
        todo_item_id = int(input())

        console.print("Enter new task name (leave blank to skip): ", end="")
        task = input()

        console.print("Enter new task due date (leave blank to skip): ", end="")
        date = input()

        console.print("Is the task completed? (yes/no): ", end="")
        completed_input = input()

        completed = True if completed_input.lower() == "yes" else False if completed_input.lower() == "no" else None
        TodoManager.update_todo_item(todo_item_id, task, date, completed)
        console.print("✅ Task updated successfully!", style="bold green")

    elif choice == "6":
        console.print("\nDelete Task", style="bold underline red")

        tasks = TodoManager.get_todo_items()

        table = create_task_list_table("Tasks", tasks)
        console.print(table)

        console.print("Enter task ID to delete: ", end="")
        todo_item_id = int(input())

        todo_item = TodoItem.objects.get(pk=todo_item_id)
        todo_item.delete()
        console.print("✅ Task deleted successfully!", style="bold green")

    elif choice == "7":
        TodoItem.objects.backend.close()
        break

    else:
        os.system('cls||clear')
        console.print("Invalid choice. Please try again.", end="\n\n", style="bold red")
        continue

    console.print("\nPress [bold red]enter[/bold red] to go back to menu.")

    input()
    os.system('cls||clear')

    continue