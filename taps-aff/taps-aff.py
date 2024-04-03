import csv

input_csv_path = 'input.csv'
output_csv_path = 'output.csv'

def decide_what_to_wear(temperature):
    if temperature < 15:
        return 'jumper'
    else:
        return 't-shirt'

with open(input_csv_path, mode='r') as infile:
    reader = csv.DictReader(infile)
    data = []
    for row in reader:
        temperature = int(row['temperature'])
        row['what_to_wear'] = decide_what_to_wear(temperature)
        data.append(row)

fieldnames = reader.fieldnames + ['what_to_wear']

with open(output_csv_path, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("Processing complete. Output file generated.")
