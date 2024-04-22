import json
import csv

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract the headers from the first entry
    headers = list(data[0].keys())

    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the headers to the CSV file
        writer.writeheader()

        # Write each entry as a row in the CSV file
        for entry in data:
            writer.writerow(entry)

    print(f"Conversion complete. CSV file saved as {csv_file}")

# Example usage
json_file = 'data_sampled.json'
csv_file = 'data_sampled.csv'
json_to_csv(json_file, csv_file)