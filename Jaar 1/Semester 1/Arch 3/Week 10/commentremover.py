# In this exercise, you will create a program that removes all of the comments from a Python source file.

# Extra:
# Python uses the # character to mark the beginning of a comment.
# The comment ends at the end of the line containing the # character.
# Check each line in the file to determine if a # character is present. If it is then your program should remove all of the characters from the # character to the end of the line (we’ll ignore the situation where the comment character occurs inside of a string).
# The user will also enter the name of the input file.
# Save the modified file using a new name that will be entered by the user.
# Input example (correct):
# File to read: functiontest.txt
# File to save: cleaned-functiontest.txt

# Output example (correct):
# No output should be given

# Input example (error):
# blanc

# Output example (error):
# Error reading file: "blanc"

import os


def read_file(filePath: str) -> list[str]:
    if not os.path.isfile(filePath) or not os.access(filePath, os.R_OK):
        return f'Error reading file: "{os.path.basename(filePath)}"'

    with open(filePath, "r") as file:
        return file.readlines()


def write_file(filePath: str, lines: list[str]) -> bool:
    # if not os.access(filePath, os.W_OK):
    #     return False
    try:
        with open(filePath, "w") as file:
            file.writelines(lines)
    except PermissionError:
        return False

    return True


def main():
    existing_file_name = input("File to read: ")
    file_path = os.path.join(os.getcwd(), existing_file_name)

    new_file_name = input("File to save: ")
    new_file_path = os.path.join(os.getcwd(), new_file_name)

    file_lines = read_file(file_path)

    cleaned_lines = [line for line in file_lines if "#" not in line]

    write_was_successful = write_file(new_file_path, cleaned_lines)
    if write_was_successful:
        print("File cleaned successfully!")
    else:
        print("Error writing file!")


if __name__ == "__main__":
    main()
