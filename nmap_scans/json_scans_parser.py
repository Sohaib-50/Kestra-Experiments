import json
import os

SCAN_DIRECTORY = '.'

def parse_nmap_json(file_path):

    with open(file_path, 'r') as f:
        nmap_scan_data = json.load(f)
    
    extracted_data = {
        'scan': {},
        'os_guesses': [],
        'ports': [],
    }
    
    nmaprun = nmap_scan_data.get('nmaprun', {})

    # extracted_data['raw'] = nmaprun

    extracted_data['scan']['scan_args'] = nmaprun.get('args').strip()
    extracted_data['scan']['nmap_version'] = nmaprun.get('version')
    extracted_data['scan']['requested_ip_address'] = extracted_data['scan']['scan_args'].split(" ")[-1]  # TODO: replace with dynamic requsted IP

    runstats = nmaprun.get('runstats', {})

    finished_stats = runstats.get('finished', {})
    extracted_data['scan']['scan_finished_timestamp'] = finished_stats.get('time')
    extracted_data['scan']['scan_summary'] = finished_stats.get('summary')

    hosts = runstats.get('hosts', {})
    extracted_data['scan']['hosts_scanned'] = hosts.get('total')
    extracted_data['scan']['hosts_up'] = hosts.get('up')
    extracted_data['scan']['hosts_down'] = hosts.get('down')
    
    host = nmaprun.get('host')
    if host:
        extracted_data['scan']['host_status'] = host.get('status', {}).get('state')
        
        address_info = host.get('address', {})
        extracted_data['scan']['scan_address'] = address_info.get('addr')
        extracted_data['scan']['scan_address_type'] = address_info.get('addrtype')
 
        extracted_data['scan']['hostname'] = host.get('hostnames', {}).get('hostname', {}).get('name')

        def extract_os_info(os_match: dict) -> dict:
            return {
                "name": os_match.get("name"),
                "accuracy": os_match.get("accuracy"),
            }
        os_matches = host.get('os', {}).get('osmatch')
        if isinstance(os_matches, dict):  # a single OS match
            extracted_data['os_guesses'].append(extract_os_info(os_match=os_matches))
        elif isinstance(os_matches, list):  # a list of OS matches
            for os_match in os_matches:
                if isinstance(os_match, dict):
                    extracted_data['os_guesses'].append(extract_os_info(os_match))
        
        def extract_port_info(port: dict) -> dict:
            return {
                'id': port.get('portid'),
                'protocol': port.get('protocol'),
                'state': port.get('state', {}).get('state'),
                'service_name': port.get('service', {}).get('name'),
                'service_product': port.get('service', {}).get('product'),
                'service_version': port.get('service', {}).get('version'),
            }
        ports_info = host.get('ports', {}).get('port')
        print(type(ports_info))
        if isinstance(ports_info, dict):  # single port
            extracted_data['ports'].append(extract_port_info(ports_info))
        elif isinstance(ports_info, list):  # multiple ports
            for port_info in ports_info:
                if isinstance(port_info, dict):
                    extracted_data['ports'].append(extract_port_info(port_info))
    
    return extracted_data


def parse_all_scans(scan_directory):
    all_results = []
    for file_name in os.listdir(scan_directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(scan_directory, file_name)
            print(f"Parsing {file_path}")
            scan_result = parse_nmap_json(file_path)
            all_results.append(scan_result)
    return all_results


if __name__ == "__main__":
    results = parse_all_scans(SCAN_DIRECTORY)
    for idx, result in enumerate(results, start=1):
        print(f"--- Scan Result {idx} ---")
        print(json.dumps(result, indent=2))
