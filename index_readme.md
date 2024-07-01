# Network Drive Indexer

This Python script indexes a networked drive and saves the directory structure to a JSON file. The index includes nested directories and files.

## Requirements

- Python 3.x

## Installation

1. Clone this repository or download the script file.
2. Ensure you have Python 3.x installed on your system.

## Usage

To index a networked drive and save the index to a JSON file, run the script with the following command-line arguments:

1. `network_drive_path`: The path to the networked drive you want to index.
2. `output_file`: The path to the output JSON file where the index will be saved.

### Command-Line Arguments

- `network_drive_path`: The UNC path of the network drive to index (e.g., `\\server\share`).
- `output_file`: The path to the JSON file where the index will be saved (e.g., `network_drive_index.json`).

### Example

```sh
python index_network_drive.py "\\networked_drive_path" "network_drive_index.json"