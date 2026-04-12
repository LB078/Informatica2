# In this exercise you will write a program that determines whether or not the characters in a string represent a valid integer.
# Write a main program that reads a string from the user and reports whether or not it represents an integer.

# Criteria:
# Create a function called is_integer(unchecked: str) -> bool
# You should ignore any leading or trailing white space
# A string represents an integer if its length is at least 1 and it only contains digits
# or if its first character is either + or - and the first character is followed by one or more characters, all of which are digits
# Create a function called remove_non_integer(unchecked: str) -> int
# that if the given string unchecked contains mixed digits and some alphabetic characters, it removes the alphabetic characters and prints the remaining integer.
# Input examples (is_integer):
# 339
# 27AB
# Output examples (is_integer):
# Valid integer
# Invalid integer
# Input examples (remove_non_integer):
# -12R0A89s
# +012R0A89s
# Output examples (remove_non_integer):
# -12089
# 12089

def is_integer(unchecked: str) -> bool:
    if len(unchecked) == 0:
        return False

    for index, char in enumerate(unchecked):
        if not char.isdigit():
            if (char == "+" or char == "-") and index == 0:
                continue
            return False

    return True


def remove_non_integer(unchecked: str) -> int:
    first_result = ""
    second_result = ""

    # Bit scuffed because "a-002m3" is technically negative but the "a" is blocking the negative, so it returns positive

    for index, char in enumerate(unchecked):
        if not char.isdigit():
            if (char == "+" or char == "-"):
                first_result += char
        else:
            first_result += char

    for index, char in enumerate(first_result):
        if not char.isdigit():
            if (char == "+" or char == "-") and index == 0:
                second_result += char
        else:
            second_result += char

    return int(second_result)


def main():
    unchecked = input("Enter a string: ")

    if is_integer(unchecked):
        print("Valid integer")
    else:
        print("Invalid integer")

    print(remove_non_integer(unchecked))


if __name__ == "__main__":
    main()
