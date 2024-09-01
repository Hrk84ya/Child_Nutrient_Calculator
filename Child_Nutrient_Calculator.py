import tkinter as tk
from tkinter import ttk, messagebox

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
            return 2200  # Example value for children older than 8

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

class NutritionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Child Nutrition Calculator")
        
        # Set the size of the window
        self.root.geometry("500x700")  # Set width to 900 and height to 700

        # Main frame with a scrollbar
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas for scrolling content
        self.scroll_y = tk.Scrollbar(self.main_frame, orient="vertical")
        self.scroll_y.pack(side="right", fill="y")
        
        self.canvas = tk.Canvas(self.main_frame, yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.config(command=self.canvas.yview)

        # Inner frame inside the canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Update scrollbar when the frame size changes
        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        # Create and place widgets
        self.create_widgets()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_widgets(self):
        # Title Label
        self.title_label = ttk.Label(self.inner_frame, text="BMI Calculator", font=('Arial', 16, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Labels and Entries with adjusted sizes
        labels = [
            "Name:", "Age (years):", "Gender:", "Height (inches):", "Weight (pounds):",
            "Milk (cups):", "Eggs (count):", "Rice (cups):", "Lentils (cups):",
            "Vegetables (cups):", "Meat (ounces):"
        ]
        
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(self.inner_frame, text=label, font=('Arial', 12)).grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(self.inner_frame, width=30)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            self.entries[label] = entry

        # Calculate Button with increased padding
        self.calculate_button = ttk.Button(self.inner_frame, text="Calculate", command=self.calculate_nutrition)
        self.calculate_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, padx=10)
        self.calculate_button.config(padding=(10, 5))  # Increase padding

        # Result Text Box with adjusted size
        self.result_text = tk.Text(self.inner_frame, wrap="word", height=15, width=60)
        self.result_text.grid(row=len(labels)+2, column=0, columnspan=2, padx=10, pady=10)

    def calculate_nutrition(self):
        try:
            name = self.entries["Name:"].get()
            age = int(self.entries["Age (years):"].get())
            gender = self.entries["Gender:"].get()
            height = float(self.entries["Height (inches):"].get())
            weight = float(self.entries["Weight (pounds):"].get())

            milk = float(self.entries["Milk (cups):"].get())
            egg = float(self.entries["Eggs (count):"].get())
            rice = float(self.entries["Rice (cups):"].get())
            lentils = float(self.entries["Lentils (cups):"].get())
            vegetable = float(self.entries["Vegetables (cups):"].get())
            meat = float(self.entries["Meat (ounces):"].get())

            child = ChildNutritionCalculator(name, age, gender, height, weight)

            daily_calories = child.calculate_daily_calories({
                "Milk": milk,
                "Egg": egg,
                "Rice": rice,
                "Lentils": lentils,
                "Vegetable": vegetable,
                "Meat": meat
            })
            nutrition_status = child.check_nutrition_status(daily_calories)

            result = (
                f"{name} has a BMI of {child.calculate_bmi():.2f}\n"
                f"Minimum daily calorie requirement: {child.calculate_min_calories()} calories\n"
                f"Daily calorie consumption: {daily_calories} calories\n"
                f"Nutrition status: {nutrition_status}"
            )
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

def main():
    root = tk.Tk()
    app = NutritionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
