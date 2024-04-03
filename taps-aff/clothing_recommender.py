import csv

class ClothingRecommender:
    """
    A class for recommending clothing based on temperature.

    Attributes:
        input_path (str): The file path to the input CSV file containing location and temperature data.
        output_path (str): The file path to the output CSV file where recommendations will be saved.
        fahrenheit_cities (list): A list of cities that use Fahrenheit for temperature measurement.
    """

    def __init__(self, input_path, output_path):
        """
        Initializes the ClothingRecommender with paths to input and output files and loads the list of Fahrenheit cities.

        Args:
            input_path (str): The file path to the input CSV file.
            output_path (str): The file path to the output CSV file.
        """
        self.input_path = input_path
        self.output_path = output_path
        # Load the list of cities using Fahrenheit from a text file.
        with open('fahrenheit_cities.txt', 'r') as file:
            self.fahrenheit_cities = file.read().splitlines()

    @staticmethod
    def decide_what_to_wear(temperature):
        """
        Decides whether to wear a jumper or a t-shirt based on the given temperature.

        Args:
            temperature (int): The temperature in Celsius.

        Returns:
            str: 'jumper' if temperature is below 15 degrees Celsius, otherwise 't-shirt'.
        """
        return 'jumper' if temperature < 15 else 't-shirt'

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        """
        Converts Fahrenheit to Celsius.

        Args:
            fahrenheit (float): The temperature in Fahrenheit.

        Returns:
            float: The temperature converted to Celsius.
        """
        return (fahrenheit - 32) * 5 / 9

    def using_fahrenheit(self, location):
        """
        Determines if the given location uses Fahrenheit.

        Args:
            location (str): The name of the location.

        Returns:
            bool: True if the location uses Fahrenheit, False otherwise.
        """
        return location in self.fahrenheit_cities

    def process_csv(self):
        """
        Processes the input CSV file, converting temperatures to Celsius if necessary, deciding on what to wear,
        and writing the recommendations to the output CSV file.
        """
        data = self.read_csv()
        for row in data:
            temperature = int(row['temperature'])
            # Convert to Celsius if the location uses Fahrenheit.
            if self.using_fahrenheit(row['location']):
                temperature = self.fahrenheit_to_celsius(temperature)
            # Decide what to wear based on the temperature.
            row['what_to_wear'] = self.decide_what_to_wear(temperature)
        # Write the recommendations to the output CSV.
        self.write_csv(data)

    def read_csv(self):
        """
        Reads the input CSV file.

        Returns:
            list: A list of dictionaries, each representing a row from the input CSV file.
        """
        with open(self.input_path, mode='r') as infile:
            reader = csv.DictReader(infile)
            return [row for row in reader]

    def write_csv(self, data):
        """
        Writes data to the output CSV file.

        Args:
            data (list): A list of dictionaries, each representing a row to be written to the output CSV file.
        """
        fieldnames = data[0].keys()
        with open(self.output_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
