import sys
import csv
import json

with open(sys.argv[-2], 'r') as f:
    data = json.load(f)

header = []

for entry in data:
    for key in entry.keys():
        if not key in header: header.append(key)

with open(sys.argv[-1], 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    for entry in data:  
        row = []
        for key in header:
            val = entry.get(key, '')
            if type(val) == bool:
                if val: row.append(1)
                else: row.append(0)
            else: row.append(val)
        writer.writerow(row)

print(len(data))