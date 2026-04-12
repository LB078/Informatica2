# A triangle can be classified based on the lengths of its sides as equilateral, isosceles or scalene.
# Write a program that reads the lengths of 3 sides of a triangle from the user. Display a message indicating the type of the triangle.

# Criteria:
# Input is given as a comma seperated string: a=5, b=6, c=5
# All 3 sides of an equilateral triangle have the same length.
# An isosceles triangle has two sides that are the same length, and a third side that is a different length.
# If all of the sides have different lengths then the triangle is scalene.
# Input example:
# Sides: a=5, b=6, c=5

# Output example:
# Isosceles triangle


def main():
    sides = input("Sides: ")

    sides = sides.replace("a=", "").replace("b=", "").replace("c=", "")

    first_side, second_side, third_side = map(int, sides.split(", "))

    first_side = first_side[2]
    second_side = second_side[2]
    third_side = third_side[2]

    if (
        first_side == second_side
        and first_side == third_side
        and second_side == third_side
    ):
        print("equilateral triangle")
    elif (
        first_side == second_side
        or first_side == third_side
        or second_side == third_side
    ):
        print("isosceles triangle")
    else:
        print("scalene triangle")


if __name__ == "__main__":
    main()
