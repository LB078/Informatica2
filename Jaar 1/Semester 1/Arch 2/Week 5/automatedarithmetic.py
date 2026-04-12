# A primary school teacher needs to automate basic arithmetic (summation, multiplication table, subtraction) exercises for her students. You are asked to implement a program that asks what type of the arithmetic the user needs to practice. Then, the program will generate exercises and the user should give the result.

# Criteria:
# For each arithmetic operation keep the total number of the exercises 10
# The program must be interactive (generate random numbers for each operation, use random module)
# Your program must be implemented with a function arithmetic_operation(arithmetic_type)
# The artihmetic_type can be (summation, multiplication, subtraction)
# Numbers for summation, subtractions and multiplications will be between 1 and 100
# Collect all the mistakes from the user and print them at the end
# Input example:
# Arethmetic operation: summation
# 1 + 4 = 4
# 3 + 3 = 6
# 6 + 2 = 8
# 5 + 1 = 7
# 3 + 8 = 8
# 5 + 4 = 9
# 8 + 3 = 10
# 1 + 6 = 7
# 3 + 9 = 11


# Output example:


# You had 4 correct and 6 incorrect answers in "summation"
import random


def arithmetic_operation(arithmetic_type):
    first_random_number = random.randint(1, 100)
    second_random_number = random.randint(1, 100)
    if arithmetic_type == "summation":
        return f"{first_random_number} + {second_random_number}",  first_random_number + second_random_number

    if arithmetic_type == "multiplication":
        return f"{first_random_number} * {second_random_number}",  first_random_number * second_random_number

    if arithmetic_type == "subtraction":
        return f"{first_random_number} - {second_random_number}",  first_random_number - second_random_number


def main():
    type_input = input("Arethmetic operation: ")

    if type_input not in ["summation", "multiplication", "subtraction"]:
        print("Invalid input")
        return

    correct = 0
    incorrect = 0

    for _ in range(10):
        question, answer = arithmetic_operation(type_input)

        user_answer = int(input(f"{question} = "))

        if user_answer == answer:
            correct += 1
        else:
            incorrect += 1

    print(f'''You had {correct} correct and {
          incorrect} incorrect answers in "{type_input}"''')


if __name__ == "__main__":
    main()
