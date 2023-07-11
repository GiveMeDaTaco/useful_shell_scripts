import os
import re

def convert_header(line):
    count = line.count('#')
    return '=' * count + line.replace('#', '').strip() + '=' * count

def convert_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip().startswith('#'):
                file.write(convert_header(line) + '\n')
            else:
                file.write(line)

def convert_directory(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.md'):
                convert_file(os.path.join(root, file))

if __name__ == "__main__":
    convert_directory('/path/to/your/directory')  # replace with your directory
