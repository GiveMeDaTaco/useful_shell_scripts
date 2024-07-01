import os
import json
import sys
import argparse

def index_directory(directory):
    index = {'directories': {}, 'files': []}
    total_files = 0
    total_dirs = 0
    
    for root, dirs, files in os.walk(directory):
        # Create a nested dictionary structure
        path_parts = os.path.relpath(root, directory).split(os.sep)
        current_dict = index['directories']
        for part in path_parts:
            if part == '.':
                continue
            if part not in current_dict:
                current_dict[part] = {'directories': {}, 'files': []}
            current_dict = current_dict[part]['directories']
        
        for d in dirs:
            current_dict[d] = {'directories': {}, 'files': []}
        
        for f in files:
            current_dict['files'].append(f)
        
        total_dirs += len(dirs)
        total_files += len(files)
        
        # Update counter in CMD window
        sys.stdout.write(f'\rDirectories indexed: {total_dirs}, Files indexed: {total_files}')
        sys.stdout.flush()
    
    return index

def save_index_to_json(index, output_file):
    with open(output_file, 'w') as f:
        json.dump(index, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Index a networked drive and save the structure to a JSON file.")
    parser.add_argument("network_drive_path", help="The path to the networked drive to index.")
    parser.add_argument("output_file", help="The output JSON file to save the index.")
    
    args = parser.parse_args()
    
    # Create an index of the network drive
    index = index_directory(args.network_drive_path)
    # Save the index to a JSON file
    save_index_to_json(index, args.output_file)

    print(f'\nIndex saved to {args.output_file}')

if __name__ == '__main__':
    main()