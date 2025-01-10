import json
import os
import sys
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        content = file.read().strip()
        return json.loads(content) if content else []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    new_task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f'Task added successfully (ID: {task_id})')

def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task {task_id} updated successfully')
            return
    print(f'Task {task_id} not found')

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f'Task {task_id} deleted successfully')

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task {task_id} marked as {status}')
            return
    print(f'Task {task_id} not found')

def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, CreatedAt: {task['createdAt']}, UpdatedAt: {task['updatedAt']}")

def main():
    if len(sys.argv) < 2:
        print('Usage: task-cli <command> [<args>]')
        return

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 3:
            print('Usage: task-cli add <description>')
            return
        description = ' '.join(sys.argv[2:])
        add_task(description)

    elif command == 'update':
        if len(sys.argv) < 4:
            print('Usage: task-cli update <id> <description>')
            return
        task_id = int(sys.argv[2])
        description = ' '.join(sys.argv[3:])
        update_task(task_id, description)

    elif command == 'delete':
        if len(sys.argv) < 3:
            print('Usage: task-cli delete <id>')
            return
        task_id = int(sys.argv[2])
        delete_task(task_id)

    elif command == 'mark-in-progress':
        if len(sys.argv) < 3:
            print('Usage: task-cli mark-in-progress <id>')
            return
        task_id = int(sys.argv[2])
        mark_task(task_id, 'in-progress')

    elif command == 'mark-done':
        if len(sys.argv) < 3:
            print('Usage: task-cli mark-done <id>')
            return
        task_id = int(sys.argv[2])
        mark_task(task_id, 'done')

    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)

    else:
        print('Unknown command')

if __name__ == '__main__':
    main()
