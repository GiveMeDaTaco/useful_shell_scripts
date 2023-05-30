import os
import re
from datetime import datetime

date_provided = "2023-05-30"  # update this as per the requirement
date_provided = datetime.strptime(date_provided, '%Y-%m-%d')
tags_to_include = {"tag1", "tag2"}  # update this set with tags to include

def get_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.md'):
                yield os.path.join(root, file)

def parse_file(file_path):
    with open(file_path, 'r') as file:
        contents = file.readlines()

    offer_name = re.search(r'# (.*) :', contents[0]).group(1)
    project_number = re.search(r': (.*) :', contents[0]).group(1)
    tags = re.findall(r':(.*?):', contents[0])
    
    if not any(tag in tags_to_include for tag in tags):
        return None

    details_start = contents.index('## Details\n')
    mdug_start = contents.index('### MDUG\n')
    data_start = contents.index('### Data\n')
    coding_start = contents.index('### Coding\n')
    file_delivery_start = contents.index('### File Delivery\n')
    documentation_start = contents.index('### Documentation\n')
    sections = [mdug_start, data_start, coding_start, file_delivery_start, documentation_start, len(contents)]
    
    parsed_content = {}
    for i in range(len(sections)-1):
        start, end = sections[i], sections[i+1]
        tasks = []
        for line in contents[start:end]:
            task = re.search(r'- \[(.*)\] (.*?)(?:@ (.*?))?(?:\|\| (.*))?$', line)
            if task:
                task_status, task_description, date_completed, date_due = task.groups()
                if task_status and (not date_due or datetime.strptime(date_due, '%Y-%m-%d') < date_provided):
                    tasks.append({'status': task_status, 'description': task_description, 'date_completed': date_completed, 'date_due': date_due})
        parsed_content[contents[start].strip('# \n')] = tasks
    
    return {'offer_name': offer_name, 'project_number': project_number, 'details': parsed_content}

def create_summary(file_path, parsed_files):
    with open(file_path, 'w') as file:
        for parsed in parsed_files:
            if parsed is not None:
                file.write(f"# {parsed['offer_name']} : {parsed['project_number']}\n")
                file.write('## Details\n')
                for section, tasks in parsed['details'].items():
                    file.write(f"### {section}\n")
                    for task in tasks:
                        file.write(f"- [{task['status']}] {task['description']}")
                        if task['date_completed']:
                            file.write(f" @ {task['date_completed']}")
                        if task['date_due']:
                            file.write(f" || {task['date_due']}")
                        file.write('\n')

parsed_files = []
for file_path in get_files('campaign'):  # use the root directory path here
    parsed_files.append(parse_file(file_path))

create_summary('summary.md', parsed_files)

