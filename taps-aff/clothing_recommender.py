import csv

class ClothingRecommender:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    @staticmethod
    def decide_what_to_wear(temperature):
        return 'jumper' if temperature < 15 else 't-shirt'

    def process_csv(self):
        data = self.read_csv()
        for row in data:
            row['what_to_wear'] = self.decide_what_to_wear(int(row['temperature']))
        self.write_csv(data)

    def read_csv(self):
        with open(self.input_path, mode='r') as infile:
            reader = csv.DictReader(infile)
            return [row for row in reader]

    def write_csv(self, data):
        fieldnames = data[0].keys()
        with open(self.output_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)