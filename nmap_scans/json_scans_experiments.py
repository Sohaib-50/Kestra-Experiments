import json

scans = []
for i in range(5):
    with open(f'scan{i}.json') as f:
        scans.append(eval(f.read().strip()))

# print([type(x) for x in scans])
for scan in scans:
    print((scan['nmaprun']['args']))
    print(type(scan['nmaprun']['host']))
    print()