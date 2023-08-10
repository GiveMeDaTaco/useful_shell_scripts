import os
import re

TAGS = [':open:', ':closed:', ':canceled:', ':pending:']

def parse_tasks(file_path):
    tasks = {tag: [] for tag in TAGS}
    with open(file_path, 'r') as file:
        data = file.readlines()
    current_tag = None
    for tag in TAGS:
        if tag in data[0]:
            current_tag = tag
            break
    if current_tag is None:
        return tasks
    tasks_start = next((i for i, line in enumerate(data) if '== Tasks ==' in line), None)
    if tasks_start is None:
        return tasks
    tasks_end = next((i for i, line in enumerate(data[tasks_start + 1:]) if '==' in line), None)
    if tasks_end is None:
        tasks_data = data[tasks_start:]
    else:
        tasks_data = data[tasks_start:tasks_start + tasks_end + 1]
    tasks[current_tag].extend(tasks_data)
    return tasks

def main(directory):
    tasks = {tag: [] for tag in TAGS}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'project.wiki':
                file_path = os.path.join(root, file)
                project_tasks = parse_tasks(file_path)
                for tag in TAGS:
                    tasks[tag] += project_tasks[tag]
    with open('tasks.wiki', 'w') as file:
        file.write('= Tasks =\n')
        for tag, task_data in tasks.items():
            if task_data:
                file.write(f'== {tag[1:-1].capitalize()} ==\n')
                file.write(''.join(task_data).replace('===', '===='))
                file.write('\n')

if __name__ == "__main__":
    main('/path/to/directory')  # Replace with your directory
