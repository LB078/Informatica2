# Positions on a chess board are identified by a letter and a number.
# Usually, the letter identifies the column, while the number identifies the row.
# Write a program that reads a position from the user.
# The program should determine if the column begins with a black square or a white square.
# Then use modular arithmetic (check if you know this concept) to report the color of the square in that row.

# Criteria:
# Your program may assume that a valid position will always be entered
# Input examples:
# Position: D5
# Position: A1
# Output examples:
# White
# Black

ASCII_START = 96


def main():
    position = input("Position: ").lower()

    horizontal = ord(position[0]) - ASCII_START

    vertical = int(position[1])

    if (vertical % 2 == 0 and horizontal % 2 == 0) or (
        vertical % 2 == 1 and horizontal % 2 == 1
    ):
        print("black")
    else:
        print("white")


if __name__ == "__main__":
    main()