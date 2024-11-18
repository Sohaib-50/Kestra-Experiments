import json
import os
from collections import defaultdict

# Function to recursively extract all keys and their types
def extract_keys(data, parent_key=''):
    keys = []
    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            keys.append((full_key, type(v).__name__))
            keys.extend(extract_keys(v, full_key))
    elif isinstance(data, list):
        for item in data:
            keys.extend(extract_keys(item, parent_key))
    return keys

# Aggregate keys across all JSON files
def analyze_json_files(directory):
    key_count = defaultdict(int)
    key_type_variability = defaultdict(set)
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                try:
                    data = json.load(file)
                    keys = extract_keys(data)
                    for key, key_type in keys:
                        key_count[key] += 1
                        key_type_variability[key].add(key_type)
                except json.JSONDecodeError:
                    print(f"Could not parse {filename}")
    return key_count, key_type_variability

# Directory containing JSON scan results
directory = "."
key_count, key_type_variability = analyze_json_files(directory)

# Reporting common keys and type variability
for key, count in key_count.items():
    print(f"Key: {key}, Occurrences: {count}, Types: {key_type_variability[key]}")
