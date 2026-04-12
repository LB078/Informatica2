# Write a program that determines the name of a shape from its number of sides.
# Read the number of sides from the user and then report the appropriate name as part of a meaningful message.

# Criteria:
# Your program should support shapes with anywhere from 3 up to (and including) 10 sides.
# If a number of sides outside of this range is entered then your program should display the error message: Amount of sides is out of range.
# Input examples:
# Sides: 3
# Sides: 4
# Output examples:
# Triangle
# Square


def main():
    sides = int(input("Sides: "))

    if sides < 3 or sides > 10:
        print("Enter a number between 3 and 10")
        return

    shapes = {
        3: "Triangle",
        4: "Square",
        5: "Pentagon",
        6: "Hexagon",
        7: "Heptagon",
        8: "Octagon",
        9: "Nonagon",
        10: "Decagon",
    }

    if shapes[sides]:
        print(shapes[sides])


if __name__ == "__main__":
    main()
