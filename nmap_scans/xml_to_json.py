import xmltodict
import os

def read_xml_file_to_dict(file_name):
    with open(file_name, 'r') as f:
        return xmltodict.parse(f.read())

def extract_keys(d, parent_key=''):
    keys = set()
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            keys.update(extract_keys(v, new_key))
        keys.add(new_key)
    return keys

for file_name in os.listdir('.'):

    if not file_name.endswith('.xml'):
        continue
    
    scan_content = read_xml_file_to_dict(file_name)
    print(scan_content)
    scan_keys = extract_keys(scan_content)
    print(file_name)
    for k in sorted(scan_keys, key = lambda x: len(x)):
        if '.' in k:
            print(f" - {k[k.rfind('.')+1:]}")
        else:
            print(f" - {k}")
    print()
    