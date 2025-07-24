import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class FoodItem:
    name: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float = 0.0
    calcium_mg: float = 0.0
    iron_mg: float = 0.0
    vitamin_a_iu: float = 0.0
    vitamin_c_mg: float = 0.0

class ChildNutritionCalculator:
    # Food database with macronutrients and micronutrients per standard serving
    FOOD_DB = {
        'Milk': FoodItem('Milk', 103, 8, 12, 2.4, 0, 300, 0.1, 500, 0),
        'Egg': FoodItem('Egg', 155, 13, 1.1, 11, 0, 56, 1.8, 600, 0),
        'Rice': FoodItem('Rice', 130, 2.7, 28, 0.3, 0.4, 10, 0.2, 0, 0),
        'Lentils': FoodItem('Lentils', 113, 9, 20, 0.4, 8, 19, 3.3, 8, 1.5),
        'Vegetable': FoodItem('Vegetable', 85, 2, 20, 0.2, 6, 25, 0.5, 5000, 28),
        'Meat': FoodItem('Meat', 143, 26, 0, 3.5, 0, 12, 2.7, 40, 0)
    }

    # Daily Recommended Intakes by age group (simplified)
    DAILY_NUTRIENT_NEEDS = {
        '1-3': {'calories': 1000, 'protein_g': 13, 'carbs_g': 130, 'fiber_g': 19, 'calcium_mg': 700, 'iron_mg': 7, 'vitamin_a_iu': 1000, 'vitamin_c_mg': 15},
        '4-8': {'calories': 1400, 'protein_g': 19, 'carbs_g': 130, 'fiber_g': 25, 'calcium_mg': 1000, 'iron_mg': 10, 'vitamin_a_iu': 1333, 'vitamin_c_mg': 25},
        '9-13': {'calories': 1800, 'protein_g': 34, 'carbs_g': 130, 'fiber_g': 31, 'calcium_mg': 1300, 'iron_mg': 8, 'vitamin_a_iu': 2000, 'vitamin_c_mg': 45}
    }

    def __init__(self, name, age, gender, height_inch, weight_pound):
        self.name = name
        self.age = age
        self.gender = gender
        self.height_inch = height_inch
        self.weight_pound = weight_pound
        self.food_intake = {}
        self.nutrition_totals = {
            'calories': 0,
            'protein_g': 0,
            'carbs_g': 0,
            'fat_g': 0,
            'fiber_g': 0,
            'calcium_mg': 0,
            'iron_mg': 0,
            'vitamin_a_iu': 0,
            'vitamin_c_mg': 0
        }

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

    def calculate_nutrition(self, food_items):
        """Calculate total nutrition from food items consumed."""
        # Reset nutrition totals
        self.nutrition_totals = {k: 0 for k in self.nutrition_totals}
        self.food_intake = food_items
        
        for food, quantity in food_items.items():
            if food in self.FOOD_DB and quantity > 0:
                food_item = self.FOOD_DB[food]
                self.nutrition_totals['calories'] += food_item.calories * quantity
                self.nutrition_totals['protein_g'] += food_item.protein_g * quantity
                self.nutrition_totals['carbs_g'] += food_item.carbs_g * quantity
                self.nutrition_totals['fat_g'] += food_item.fat_g * quantity
                self.nutrition_totals['fiber_g'] += food_item.fiber_g * quantity
                self.nutrition_totals['calcium_mg'] += food_item.calcium_mg * quantity
                self.nutrition_totals['iron_mg'] += food_item.iron_mg * quantity
                self.nutrition_totals['vitamin_a_iu'] += food_item.vitamin_a_iu * quantity
                self.nutrition_totals['vitamin_c_mg'] += food_item.vitamin_c_mg * quantity
        
        return self.nutrition_totals
    
    def get_daily_recommendations(self) -> dict:
        """Get daily recommended nutrient intakes based on age group."""
        if 1 <= self.age <= 3:
            return self.DAILY_NUTRIENT_NEEDS['1-3']
        elif 4 <= self.age <= 8:
            return self.DAILY_NUTRIENT_NEEDS['4-8']
        else:  # 9-13
            return self.DAILY_NUTRIENT_NEEDS['9-13']
    
    def get_nutrition_status(self) -> Dict[str, str]:
        """Get status of each nutrient (deficient, adequate, excessive)."""
        status = {}
        recommendations = self.get_daily_recommendations()
        
        for nutrient, value in self.nutrition_totals.items():
            if nutrient in recommendations:
                rec = recommendations[nutrient]
                if value < rec * 0.7:  # Below 70% of recommended
                    status[nutrient] = "Low"
                elif value > rec * 1.3:  # Above 130% of recommended
                    status[nutrient] = "High"
                else:
                    status[nutrient] = "Adequate"
        
        return status
    
    def generate_meal_plan(self) -> List[Dict]:
        """Generate a simple meal plan based on nutritional needs."""
        recommendations = self.get_daily_recommendations()
        current_intake = self.nutrition_totals
        
        meal_plan = []
        
        # Simple logic to suggest foods based on deficiencies
        if current_intake['protein_g'] < recommendations['protein_g'] * 0.8:
            meal_plan.append({
                'suggestion': 'Add protein source',
                'foods': ['Eggs', 'Meat', 'Lentils'],
                'reason': f'Current protein intake ({current_intake["protein_g"]:.1f}g) is below recommended ({recommendations["protein_g"]}g)'
            })
            
        if current_intake['fiber_g'] < recommendations['fiber_g'] * 0.7:
            meal_plan.append({
                'suggestion': 'Add fiber-rich foods',
                'foods': ['Lentils', 'Vegetables', 'Whole grains'],
                'reason': f'Current fiber intake ({current_intake["fiber_g"]:.1f}g) is below recommended ({recommendations["fiber_g"]}g)'
            })
            
        if current_intake['calcium_mg'] < recommendations['calcium_mg'] * 0.7:
            meal_plan.append({
                'suggestion': 'Add calcium source',
                'foods': ['Milk', 'Cheese', 'Yogurt'],
                'reason': f'Current calcium intake ({current_intake["calcium_mg"]:.1f}mg) is below recommended ({recommendations["calcium_mg"]}mg)'
            })
            
        return meal_plan

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
        self.title_label = ttk.Label(self.inner_frame, text="Child Nutrition Calculator", font=('Arial', 16, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Personal Information Section
        ttk.Label(self.inner_frame, text="Personal Information", font=('Arial', 12, 'bold')).grid(row=1, column=0, columnspan=2, pady=5, sticky="w")
        
        # Labels and Entries with adjusted sizes
        personal_info = [
            "Name:", "Age (years):", "Gender:", "Height (inches):", "Weight (pounds):"
        ]
        
        self.entries = {}
        for i, label in enumerate(personal_info, start=2):  # Start from row 2
            ttk.Label(self.inner_frame, text=label, font=('Arial', 10)).grid(row=i, column=0, sticky="w", padx=10, pady=2)
            entry = ttk.Entry(self.inner_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=2)
            self.entries[label.split(':')[0]] = entry
        
        # Food Intake Section
        ttk.Label(self.inner_frame, text="\nDaily Food Intake", font=('Arial', 12, 'bold')).grid(row=7, column=0, columnspan=2, pady=5, sticky="w")
        
        food_items = [
            "Milk (cups):", "Eggs (count):", "Rice (cups):", 
            "Lentils (cups):", "Vegetables (cups):", "Meat (ounces):"
        ]
        
        for i, label in enumerate(food_items, start=8):  # Start from row 8
            ttk.Label(self.inner_frame, text=label, font=('Arial', 10)).grid(row=i, column=0, sticky="w", padx=10, pady=2)
            entry = ttk.Entry(self.inner_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=2)
            self.entries[label.split(' (')[0]] = entry

        # Buttons
        button_frame = ttk.Frame(self.inner_frame)
        button_frame.grid(row=15, column=0, columnspan=2, pady=(10, 0))
        
        self.calculate_button = ttk.Button(button_frame, text="Calculate Nutrition", command=self.calculate)
        self.calculate_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_form)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Create Notebook for multiple tabs
        self.notebook = ttk.Notebook(self.inner_frame)
        self.notebook.grid(row=16, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        # Nutrition Summary Tab
        self.summary_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.summary_frame, text='Nutrition Summary')
        
        # Detailed Nutrition Tab
        self.details_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.details_frame, text='Detailed Nutrition')
        
        # Meal Plan Tab
        self.meal_plan_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.meal_plan_frame, text='Meal Plan')
        
        # Initialize text widgets for each tab
        self.summary_text = tk.Text(self.summary_frame, height=10, width=60, wrap=tk.WORD)
        self.summary_text.pack(expand=True, fill='both')
        
        self.details_text = tk.Text(self.details_frame, height=15, width=60, wrap=tk.WORD)
        self.details_text.pack(expand=True, fill='both')
        
        self.meal_plan_text = tk.Text(self.meal_plan_frame, height=10, width=60, wrap=tk.WORD)
        self.meal_plan_text.pack(expand=True, fill='both')

    def clear_form(self):
        """Clear all input fields."""
        for entry in self.entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
        self.summary_text.delete(1.0, tk.END)
        self.details_text.delete(1.0, tk.END)
        self.meal_plan_text.delete(1.0, tk.END)

    def calculate(self):
        try:
            # Get user inputs
            name = self.entries["Name"].get()
            age = int(self.entries["Age (years)"].get() or 0)
            gender = self.entries["Gender"].get()
            height = float(self.entries["Height (inches)"].get() or 0)
            weight = float(self.entries["Weight (pounds)"].get() or 0)
            
            # Validate inputs
            if not all([name, age > 0, height > 0, weight > 0]):
                raise ValueError("Please fill in all required fields with valid values.")
            
            # Get food quantities
            food_items = {
                "Milk": float(self.entries["Milk"].get() or 0),
                "Egg": float(self.entries["Eggs"].get() or 0),
                "Rice": float(self.entries["Rice"].get() or 0),
                "Lentils": float(self.entries["Lentils"].get() or 0),
                "Vegetable": float(self.entries["Vegetables"].get() or 0),
                "Meat": float(self.entries["Meat"].get() or 0)
            }
            
            # Create calculator instance and calculate
            calculator = ChildNutritionCalculator(name, age, gender, height, weight)
            bmi = calculator.calculate_bmi()
            min_calories = calculator.calculate_min_calories()
            nutrition = calculator.calculate_nutrition(food_items)
            status = calculator.check_nutrition_status(nutrition['calories'])
            meal_plan = calculator.generate_meal_plan()
            
            # Display summary
            self.show_summary(name, bmi, min_calories, nutrition, status)
            
            # Display detailed nutrition
            self.show_detailed_nutrition(nutrition, calculator)
            
            # Display meal plan
            self.show_meal_plan(meal_plan)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
    
    def show_summary(self, name, bmi, min_calories, nutrition, status):
        """Display nutrition summary in the summary tab."""
        summary = f"{name}'s Nutrition Summary\n"
        summary += "=" * 50 + "\n"
        summary += f"BMI: {bmi:.1f} - {status}\n"
        summary += f"Minimum daily calories needed: {min_calories}\n"
        summary += f"Total calories consumed: {nutrition['calories']:.0f} "
        
        # Add calorie status
        if nutrition['calories'] < min_calories * 0.9:
            summary += "(Below recommended)\n"
        elif nutrition['calories'] > min_calories * 1.1:
            summary += "(Above recommended)\n"
        else:
            summary += "(Adequate)\n"
            
        # Add macronutrient summary
        summary += "\nMacronutrients:\n"
        summary += f"- Protein: {nutrition['protein_g']:.1f}g\n"
        summary += f"- Carbohydrates: {nutrition['carbs_g']:.1f}g\n"
        summary += f"- Fats: {nutrition['fat_g']:.1f}g\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)
    
    def show_detailed_nutrition(self, nutrition, calculator):
        """Display detailed nutrition information."""
        details = "Detailed Nutrition Information\n"
        # Get recommendations and status
        recommendations = calculator.get_daily_recommendations()
        status = calculator.get_nutrition_status()
        
        # Macronutrients
        details += "\nMacronutrients:\n"
        details += "-" * 30 + "\n"
        for nutrient in ['protein_g', 'carbs_g', 'fat_g', 'fiber_g']:
            rec = recommendations.get(nutrient, 0)
            nutr_value = nutrition.get(nutrient, 0)
            nutr_name = nutrient.replace('_g', '').title()
            details += f"{nutr_name}: {nutr_value:.1f}g (Recommended: {rec}g) - {status.get(nutrient, 'N/A')}\n"
        
        # Micronutrients
        details += "\nMicronutrients:\n"
        details += "-" * 30 + "\n"
        for nutrient, name in [
            ('calcium_mg', 'Calcium (mg)'),
            ('iron_mg', 'Iron (mg)'),
            ('vitamin_a_iu', 'Vitamin A (IU)'),
            ('vitamin_c_mg', 'Vitamin C (mg)')
        ]:
            rec = recommendations.get(nutrient, 0)
            nutr_value = nutrition.get(nutrient, 0)
            details += f"{name}: {nutr_value:.1f} (Recommended: {rec}) - {status.get(nutrient, 'N/A')}\n"
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)
    
    def show_meal_plan(self, meal_plan):
        """Display personalized meal plan suggestions."""
        if not meal_plan:
            self.meal_plan_text.delete(1.0, tk.END)
            self.meal_plan_text.insert(tk.END, "Your current diet meets the basic nutritional recommendations.\n\n"
                                      "For optimal health, consider eating a variety of foods from all food groups.")
            return
            
        plan = "Personalized Meal Plan Suggestions\n"
        plan += "=" * 50 + "\n\n"
        
        for i, suggestion in enumerate(meal_plan, 1):
            plan += f"{i}. {suggestion['suggestion']}\n"
            plan += f"   Recommended foods: {', '.join(suggestion['foods'])}\n"
            plan += f"   Reason: {suggestion['reason']}\n\n"
        
        plan += "\nGeneral Tips:\n"
        plan += "- Include a variety of colorful fruits and vegetables in your diet\n"
        plan += "- Choose whole grains over refined grains when possible\n"
        plan += "- Stay hydrated by drinking plenty of water\n"
        plan += "- Limit added sugars and processed foods\n"
        
        self.meal_plan_text.delete(1.0, tk.END)
        self.meal_plan_text.insert(tk.END, plan)

def main():
    root = tk.Tk()
    app = NutritionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
