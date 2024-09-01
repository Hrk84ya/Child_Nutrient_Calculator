import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ChildNutritionCalculator:
    def __init__(self, name, age, gender, height_inch, weight_pound):
        self.name = name
        self.age = age
        self.gender = gender
        self.height_inch = height_inch
        self.weight_pound = weight_pound

    def calculate_bmi(self):
        if self.height_inch <= 0:
            raise ValueError("Height must be greater than zero.")
        bmi = (self.weight_pound / (self.height_inch ** 2)) * 703
        return bmi

    def calculate_min_calories(self):
        if 0 <= self.age <= 2:
            return 800
        elif 2 < self.age <= 4:
            return 1400
        elif 4 < self.age <= 8:
            return 1800
        else:
            return 2200

    def calculate_daily_calories(self, food_items):
        calorie_dict = {"Milk": 100, "Egg": 155, "Rice": 130, "Lentils": 113, "Vegetable": 85, "Meat": 143}
        total_calories = 0
        for food, quantity in food_items.items():
            if food in calorie_dict:
                if quantity < 0:
                    raise ValueError(f"Quantity for {food} cannot be negative.")
                total_calories += (calorie_dict[food] * quantity)
        return total_calories

    def check_nutrition_status(self, daily_calories):
        bmi = self.calculate_bmi()
        if bmi < 16:
            return "Severely Underweight"
        elif 16 < bmi <= 18.5:
            return "Underweight"
        elif 18.5 < bmi <= 25:
            return "Healthy"
        elif 25 < bmi <= 30:
            return "Overweight"
        else:
            return "Obese"

class NutritionApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Child Nutrition Calculator")
        self.geometry("600x700")

        # Create a frame for the canvas and scrollbar
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Create a canvas widget
        self.canvas = tk.Canvas(self.container)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a frame inside the canvas for the scrollable content
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create a window on the canvas and add the scrollable frame to it
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.scrollable_frame, text="Child Nutrition Calculator", font=("Arial", 16)).pack(pady=10)

        self.entries = {}
        labels = ["Name", "Age", "Gender", "Height (inches)", "Weight (pounds)", "Milk (cups)", "Eggs (count)", "Rice (cups)", "Lentils (cups)", "Vegetables (cups)", "Meat (ounces)"]
        for label in labels:
            ttk.Label(self.scrollable_frame, text=label).pack(pady=5)
            entry = ttk.Entry(self.scrollable_frame)
            entry.pack(pady=5)
            self.entries[label] = entry

        ttk.Button(self.scrollable_frame, text="Calculate", command=self.calculate).pack(pady=20)

        self.result_text = tk.Text(self.scrollable_frame, height=10, width=50)
        self.result_text.pack(pady=10)

    def calculate(self):
        try:
            name = self.entries["Name"].get()
            age = int(self.entries["Age"].get())
            gender = self.entries["Gender"].get()
            height = float(self.entries["Height (inches)"].get())
            weight = float(self.entries["Weight (pounds)"].get())
            
            milk = float(self.entries["Milk (cups)"].get())
            egg = float(self.entries["Eggs (count)"].get())
            rice = float(self.entries["Rice (cups)"].get())
            lentils = float(self.entries["Lentils (cups)"].get())
            vegetable = float(self.entries["Vegetables (cups)"].get())
            meat = float(self.entries["Meat (ounces)"].get())

            child = ChildNutritionCalculator(name, age, gender, height, weight)
            food_consumption = {"Milk": milk, "Egg": egg, "Rice": rice, "Lentils": lentils, "Vegetable": vegetable, "Meat": meat}
            daily_calories = child.calculate_daily_calories(food_consumption)
            nutrition_status = child.check_nutrition_status(daily_calories)
            min_calories = child.calculate_min_calories()
            bmi = child.calculate_bmi()

            result = (f"{name} has a BMI of {bmi:.2f}\n"
                      f"Minimum daily calorie requirement: {min_calories} calories\n"
                      f"Daily calorie consumption: {daily_calories} calories\n"
                      f"Nutrition status: {nutrition_status}")

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

if __name__ == "__main__":
    app = NutritionApp()
    app.mainloop()
