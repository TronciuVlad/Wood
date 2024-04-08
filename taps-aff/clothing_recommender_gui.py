import tkinter as tk
from tkinter import ttk, messagebox
from clothing_recommender import ClothingRecommender
import csv
import re

class RecommendationViewer:
    """
    A GUI application for viewing, adding, and deleting clothing recommendations based on temperature.
    
    Attributes:
        master (tk.Tk): The root window of the Tkinter application.
        recommender (ClothingRecommender): An instance of the ClothingRecommender class for processing recommendations.
    """

    def __init__(self, master, recommender):
        """
        Initializes the RecommendationViewer GUI application.
        
        Args:
            master (tk.Tk): The root window of the Tkinter application.
            recommender (ClothingRecommender): An instance of the ClothingRecommender class.
        """
        self.master = master
        self.recommender = recommender
        master.title("Clothing Recommendations")

        self.setup_widgets()
        self.load_data()

    def setup_widgets(self):
        """
        Sets up the GUI widgets including Treeview for recommendations, input fields for adding new cities, and control buttons.
        """
        # Setup Treeview
        self.tree = ttk.Treeview(self.master)
        self.tree['columns'] = ('location', 'temperature', 'what_to_wear')
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("location", anchor=tk.W, width=120)
        self.tree.column("temperature", anchor=tk.CENTER, width=100)
        self.tree.column("what_to_wear", anchor=tk.W, width=120)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("location", text="City", anchor=tk.W)
        self.tree.heading("temperature", text="Temperature", anchor=tk.CENTER)
        self.tree.heading("what_to_wear", text="What to Wear", anchor=tk.W)

        self.tree.pack(side=tk.TOP, fill=tk.X)
        
        # Add city form
        self.form_frame = tk.Frame(self.master)
        self.form_frame.pack(side=tk.TOP, fill=tk.X)

        self.city_label = tk.Label(self.form_frame, text="City:")
        self.city_label.pack(side=tk.LEFT)
        self.city_entry = tk.Entry(self.form_frame)
        self.city_entry.pack(side=tk.LEFT)

        self.temperature_label = tk.Label(self.form_frame, text="Temperature:")
        self.temperature_label.pack(side=tk.LEFT)
        self.temperature_entry = tk.Entry(self.form_frame)
        self.temperature_entry.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.form_frame, text="Add City", command=self.add_city)
        self.add_button.pack(side=tk.LEFT)

        # Refresh button
        self.refresh_button = tk.Button(self.master, text="Refresh", command=self.load_data)
        self.refresh_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Delete button
        self.delete_button = tk.Button(self.master, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(side=tk.BOTTOM, fill=tk.X)

    def add_city(self):
        """
        Adds a new city and its temperature to the input CSV file, recalculates recommendations, and refreshes the display.
        Validates the temperature input and checks for duplicate city entries before adding.
        """
        city = self.city_entry.get().strip()
        temperature_str = self.temperature_entry.get().strip()
        try:
            temperature = int(temperature_str)

            # Check if the location already exists in the input CSV
            if self.location_exists(city):
                messagebox.showerror("Error", f"The location '{city}' already exists. Please enter a different location.")
                return

            with open(self.recommender.input_path, mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([city, temperature])
            
            self.recommender.process_csv()
            self.load_data()

            self.city_entry.delete(0, tk.END)
            self.temperature_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid temperature. Please enter a numeric value.")

    def location_exists(self, city):
        """
        Checks if the specified city already exists in the input CSV file.
        
        Args:
            city (str): The name of the city to check.
            
        Returns:
            bool: True if the city already exists, False otherwise.
        """
        with open(self.recommender.input_path, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].strip().lower() == city.lower():
                    return True
        return False

    def load_data(self):
        """
        Loads and displays the clothing recommendations from the output CSV file.
        Updates the Treeview with the latest recommendations, including temperature units.
        """
        for i in self.tree.get_children():
            self.tree.delete(i)
        with open(self.recommender.output_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location = row['location']
                temperature = row['temperature']
                unit = "F" if self.recommender.using_fahrenheit(location) else "C" # Determine temperature unit
                temperature_with_unit = f"{temperature} {unit}"
                self.tree.insert("", tk.END, values=(location, temperature_with_unit, row['what_to_wear']))

    def delete_selected(self):
        """
        Deletes the selected recommendation from the input CSV file, recalculates the output, and refreshes the display.
        Confirms deletion with the user before proceeding.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected item?")
        if confirm:
            location = self.tree.item(selected_item)["values"][0]
            temperature_with_unit = self.tree.item(selected_item)["values"][1]
            temperature = re.match(r"\d+", temperature_with_unit).group()
            self.tree.delete(selected_item)
            self.update_input_csv(location, temperature)
            self.recommender.process_csv()
            self.load_data()

    def update_input_csv(self, location, temperature):
        """
        Updates the input CSV file by removing the specified entry.
        
        Args:
            location (str): The location of the entry to remove.
            temperature (str): The temperature of the entry to remove, used to ensure accurate identification.
        """
        temp_entries = []
        with open(self.recommender.input_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['location'] != location or str(row['temperature']) != str(temperature):
                    temp_entries.append(row)

    
        # Rewrite the input CSV without the deleted entry
        with open(self.recommender.input_path, mode='w', newline='') as csvfile:
            fieldnames = ['location', 'temperature']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in temp_entries:
                writer.writerow(row)

if __name__ == "__main__":
    root = tk.Tk()
    recommender = ClothingRecommender('input.csv', 'output.csv')
    app = RecommendationViewer(root, recommender)
    root.mainloop()
