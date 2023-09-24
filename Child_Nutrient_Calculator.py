class ChildNutritionCalculator:
    def __init__(self, name, age, gender, height_inch, weight_pound):
        #function used for taking input
        self.name = name
        self.age = age
        self.gender = gender
        self.height_inch = height_inch
        self.weight_pound = weight_pound
         

    def calculate_bmi(self):
        #calculating bmi with the given set of inputs
        bmi = (self.weight_pound / (self.height_inch ** 2)) * 703
        return bmi

    def calculate_min_calories(self):
        #Displaying the minimum calories as mentioned
        if 0 <= self.age <= 2:
            return 800
        elif 2 < self.age <= 4:
            return 1400
        elif 4 < self.age <= 8:
            return 1800
        else:
            return None

    def calculate_daily_calories(self, food_items):
        #calories of food products are mentioned
        calorie_dict = {"Milk": 100,"Egg": 155,"Rice": 130,"Lentils": 113,"Vegetable": 85,"Meat": 143}
        total_calories = 0
        for food, quantity in food_items.items():
            if food in calorie_dict:
                #calculating the total calorie
                total_calories += (calorie_dict[food] * quantity)
        return total_calories
    #return statement does not print any value

    def check_nutrition_status(self, daily_calories):
        #displaying the bmi status
        bmi=child.calculate_bmi()
        if bmi<16:
            return "Severely Underweight"
        elif 16<bmi<=18.5:
            return "Underweight"
        elif 18.5<bmi<=25:
            return"Healthy"
        elif 25<bmi<=30:
            return "Overweight"
        else:
            return "Obese"

#Taking inputs from the user
Name=input("Enter the name of the child: ")
Age=int(input("Enter the age of the child: "))
Gender=input("Enter the gender of the child: ")
height=float(input("Enter height in inches: "))
weight=float(input("Enter weight in pounds: "))
child = ChildNutritionCalculator(Name, Age, Gender, height, weight)

#taking consumed food products as input 
milk=float(input("Enter amount of milk consumed: "))
egg=float(input("Enter amount of eggs consumed: "))
rice=float(input("Enter amount of rice consumed: "))
lentils=float(input("Enter amount of lentils consumed: "))
vegetable=float(input("Enter amount of vegetables consumed: "))
Meat=float(input("Enter amount of meat consumed: "))

food_consumption = {"Milk": milk,"Egg":egg,"Rice": rice,"Lentils": lentils,"Vegetable": vegetable,"Meat": Meat}
Daily_Calories = child.calculate_daily_calories(food_consumption)
NUTRITION_STATUS = child.check_nutrition_status(Daily_Calories)

print(f"{child.name} has a BMI of {child.calculate_bmi():.2f}")
print(f"Minimum daily calorie requirement: {child.calculate_min_calories()} calories")
print(f"Daily calorie consumption: {Daily_Calories} calories")
print(f"Nutrition status: {NUTRITION_STATUS}")
