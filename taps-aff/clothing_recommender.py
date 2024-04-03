import csv

class ClothingRecommender:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        # List of cities using Fahrenheit
        with open('fahrenheit_cities.txt', 'r') as file:
            self.fahrenheit_cities = file.read().splitlines()

    @staticmethod
    def decide_what_to_wear(temperature):
        return 'jumper' if temperature < 15 else 't-shirt'

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        return (fahrenheit - 32) * 5 / 9

    def using_fahrenheit(self, location):
        return location in self.fahrenheit_cities

    def process_csv(self):
        data = self.read_csv()
        for row in data:
            temperature = int(row['temperature'])
            # Use using_fahrenheit to check if the location uses Fahrenheit
            if self.using_fahrenheit(row['location']):
                temperature = self.fahrenheit_to_celsius(temperature)
            row['what_to_wear'] = self.decide_what_to_wear(temperature)
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
