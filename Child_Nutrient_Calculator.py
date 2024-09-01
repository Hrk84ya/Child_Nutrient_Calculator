class ChildNutritionCalculator:
    def __init__(self, name, age, gender, height_inch, weight_pound):
        """
        Initialize the ChildNutritionCalculator with basic information.
        """
        self.name = name
        self.age = age
        self.gender = gender
        self.height_inch = height_inch
        self.weight_pound = weight_pound

    def calculate_bmi(self):
        """
        Calculate BMI using the formula: (weight / (height^2)) * 703.
        """
        if self.height_inch <= 0:
            raise ValueError("Height must be greater than zero.")
        bmi = (self.weight_pound / (self.height_inch ** 2)) * 703
        return bmi

    def calculate_min_calories(self):
        """
        Determine the minimum daily calorie requirement based on age.
        """
        if 0 <= self.age <= 2:
            return 800
        elif 2 < self.age <= 4:
            return 1400
        elif 4 < self.age <= 8:
            return 1800
        else:
            return 2200  # Example value for children older than 8

    def calculate_daily_calories(self, food_items):
        """
        Calculate total daily calories based on the consumed food items.
        """
        calorie_dict = {"Milk": 100, "Egg": 155, "Rice": 130, "Lentils": 113, "Vegetable": 85, "Meat": 143}
        total_calories = 0
        for food, quantity in food_items.items():
            if food in calorie_dict:
                if quantity < 0:
                    raise ValueError(f"Quantity for {food} cannot be negative.")
                total_calories += (calorie_dict[food] * quantity)
        return total_calories

    def check_nutrition_status(self, daily_calories):
        """
        Determine nutrition status based on BMI.
        """
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

def get_positive_float(prompt):
    """
    Helper function to get a positive float input from the user.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_non_negative_float(prompt):
    """
    Helper function to get a non-negative float input from the user.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    # Taking inputs from the user
    Name = input("Enter the name of the child: ")
    Age = int(get_positive_float("Enter the age of the child (in years): "))
    Gender = input("Enter the gender of the child: ")
    height = get_positive_float("Enter height in inches: ")
    weight = get_positive_float("Enter weight in pounds: ")

    child = ChildNutritionCalculator(Name, Age, Gender, height, weight)

    # Taking consumed food products as input
    milk = get_non_negative_float("Enter amount of milk consumed (in cups): ")
    egg = get_non_negative_float("Enter amount of eggs consumed (in count): ")
    rice = get_non_negative_float("Enter amount of rice consumed (in cups): ")
    lentils = get_non_negative_float("Enter amount of lentils consumed (in cups): ")
    vegetable = get_non_negative_float("Enter amount of vegetables consumed (in cups): ")
    Meat = get_non_negative_float("Enter amount of meat consumed (in ounces): ")

    food_consumption = {"Milk": milk, "Egg": egg, "Rice": rice, "Lentils": lentils, "Vegetable": vegetable, "Meat": Meat}
    Daily_Calories = child.calculate_daily_calories(food_consumption)
    NUTRITION_STATUS = child.check_nutrition_status(Daily_Calories)

    print(f"{child.name} has a BMI of {child.calculate_bmi():.2f}")
    print(f"Minimum daily calorie requirement: {child.calculate_min_calories()} calories")
    print(f"Daily calorie consumption: {Daily_Calories} calories")
    print(f"Nutrition status: {NUTRITION_STATUS}")

if __name__ == "__main__":
    main()
