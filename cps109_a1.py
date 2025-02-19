# Fitness Tracker
# Problem: Freshman 15 is a real thing! Many students forget their physical health when entering University.
# This program will help students track their progress at the gym and record their food intake.
import os
def clear_terminal():
    os.system("cls" if os.name =="nt" else "clear")

def log_workout(workouts):
    exercise = input("Enter the exercise name: ")
    
    while True:
        try:
            duration = float(input("Enter the duration in minutes: "))
            calories_burned = float(input("Enter the calories burned: "))
            if duration < 0 or calories_burned < 0:
                print("Duration and calories burned must be positive numbers. ")
                continue
            workouts.append((exercise, duration, calories_burned))  # This appends workout details as a tuple
            print("Workout logged successfully!")
            break  # Exits the loop if everything is valid
        except ValueError:
            print("Please enter a valid numeric value for duration and calories.")

def log_meal(meals):
    """Logs a meal including the meal name, category, and calories consumed."""
    valid_categories = ["breakfast", "lunch", "dinner", "snack"]  # Categories in lowercase
    
    while True:
        category = input("Enter the meal category (e.g., breakfast, lunch, dinner, snack): ").lower()
        if category not in valid_categories:
            print(f"Invalid category. Please choose from: {', '.join(valid_categories)}.")
            continue  # Prompt user to enter a valid category
        
        meal = input("Enter the meal name: ")
        if len(meal) < 1:
            print("Meal name cannot be empty. Please try again.")
            continue  # Prompt user to enter a valid meal name
        
        while True:
            try:
                protein = float(input("Enter the protein in grams: "))
                carbs = float(input("Enter the carbs in grams: "))
                fats = float(input("Enter the fats in grams: "))
                calories = float(input("Enter the calories in the meal: "))
                
                if protein < 0 or carbs < 0 or fats < 0 or calories < 0:
                    print("Nutritional values must be positive numbers. Please try again.")
                    continue
                
                meals.append((category, meal, protein, carbs, fats, calories))  # Append meal details as a tuple
                print("Meal logged successfully!")
                break  # Exit the loop if input is valid
            except ValueError:
                print("Please enter valid numeric values for protein, carbs, fats, and calories.")
        
        # After logging the meal, return to main options
        return  # Return to the main menu after logging

def calculate_net_calories(workouts, meals):
    """Calculates net calories by subtracting burned calories from consumed calories."""
    
    total_burned = sum(calories for _, _, calories in workouts)
    total_consumed = sum(calories for _, _, _, _, _, calories in meals)
    
    net_calories = total_consumed - total_burned
    return total_burned, total_consumed, net_calories

def suggest_goal_feedback(net_calories, maintenance_calories):
    """Provides feedback based on net calories relative to maintenance calories."""
    if net_calories < maintenance_calories:
        return "You're in a caloric deficit, which is good for cutting!"
    elif net_calories > maintenance_calories:
        return "You're in a caloric surplus, which is good for bulking!"
    else:
        return "You're at maintenance level. You are neither bulking nor cutting."

def display_summary(workouts, meals, protein_goal):
    """Displays a summary of workouts, meals, and remaining protein goal."""
    print("\n--- Workouts Logged ---")
    for exercise, duration, calories in workouts:
        print(f"Exercise: {exercise}, Duration: {duration} mins, Calories Burned: {calories}")
    
    print("\n--- Meals Logged ---")
    total_protein = 0
    for category, meal, protein, carbs, fats, calories in meals:
        print(f"Category: {category}, Meal: {meal}, Protein: {protein}g, Carbs: {carbs}g, Fats: {fats}g, Calories: {calories}")
        total_protein += protein
    
    print("\n--- Summary ---")
    print(f"Total Protein Consumed: {total_protein}g")
    remaining_protein = max(0, protein_goal - total_protein)
    print(f"You need {remaining_protein}g more protein for optimal results.")

    # Write summary to a file
    with open("fitness_summary.txt", "w") as f:
        f.write("--- Workouts Logged ---\n")
        for exercise, duration, calories in workouts:
            f.write(f"Exercise: {exercise}, Duration: {duration} mins, Calories Burned: {calories}\n")
        
        f.write("\n--- Meals Logged ---\n")
        for category, meal, protein, carbs, fats, calories in meals:
            f.write(f"Category: {category}, Meal: {meal}, Protein: {protein}g, Carbs: {carbs}g, Fats: {fats}g, Calories: {calories}\n")
        
        f.write("\n--- Summary ---\n")
        f.write(f"Total Protein Consumed: {total_protein}g\n")
        f.write(f"You need {remaining_protein}g more protein for optimal results.\n")

def read_input_file(filename, workouts, meals):
    """Reads workouts and meals from a given file."""
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split(',')
                if data[0].lower() == "workout":
                    workouts.append((data[1], float(data[2]), float(data[3])))  # (exercise, duration, calories)
                elif data[0].lower() == "meal":
                    meals.append((data[1], data[2], float(data[3]), float(data[4]), float(data[5]), float(data[6])))  # (category, meal, protein, carbs, fats, calories)
    except FileNotFoundError:
        print("Input file not found. Starting with an empty log.")

def main():
    """Main function to run the fitness tracker program."""
    # User input for weight and maintenance calculation
    clear_terminal()

    weight = float(input("Enter your body weight in pounds: "))
    protein_goal = weight  # 1 gram of protein per pound of body weight
    maintenance_calories = weight * 15  # Approximate maintenance calories
    print(f"Your protein needs: {protein_goal} grams.")
    print(f"Estimated maintenance calories: {maintenance_calories} calories.")
    
    workouts = []  # List to store workout details
    meals = []     # List to store meal details

    # Read workouts and meals from a file
    read_input_file("fitness_summary.txt", workouts, meals)

    while True:
        # Menu for user to log workouts or meals or exit
        print("\nFitness Tracker Menu:")
        print("1. Log Workout")
        print("2. Log Meal")
        print("3. View Summary")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        clear_terminal()

        if choice == '1':
            log_workout(workouts)  # Log a workout
        elif choice == '2':
            log_meal(meals)  # Log a meal
        elif choice == '3':
            # Calculate net calories and display summary
            total_burned, total_consumed, net_calories = calculate_net_calories(workouts, meals)
            display_summary(workouts, meals, protein_goal)
            
            print("\n--- Calories Summary ---")
            print(f"Total Calories Burned: {total_burned}")
            print(f"Total Calories Consumed: {total_consumed}")
            print(f"Net Calories: {net_calories}")
            print(suggest_goal_feedback(net_calories, maintenance_calories))  # Provide feedback
            
        elif choice == '4':
            break  # Exit the program
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

