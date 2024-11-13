import json
import csv

# Load JSON data
with open('mobile_games.json', 'r') as json_file:
    data = json.load(json_file)

# Convert to CSV
with open('mobile_games.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(data[0].keys())

    # Write rows
    for row in data:
        csv_writer.writerow(row.values())
