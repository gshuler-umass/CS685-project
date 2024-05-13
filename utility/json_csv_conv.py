import json
import csv


def json_to_csv(json_input_filepath: str, csv_output_filepath: str):
    with open(json_input_filepath, 'r') as file:
        data = json.load(file)

    # Extract the headers from the first entry
    headers = list(data[0].keys())

    # Open the CSV file in write mode
    with open(csv_output_filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the headers to the CSV file
        writer.writeheader()

        # Write each entry as a row in the CSV file
        for entry in data:
            writer.writerow(entry)

    print(f"Conversion complete. CSV file saved as {csv_output_filepath}")


# Change these filepaths accordingly
json_input_file = 'data_sampled.json'  # input filepath
csv_output_file = 'data_sampled.csv'  # output filepath

if __name__ == "__main__":
    json_to_csv(json_input_file, csv_output_file)
