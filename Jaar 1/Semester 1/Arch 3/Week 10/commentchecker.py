# When you write a function, it is a good idea to include a comment that outlines the function’s purpose, its parameters and its return value. However, sometimes comments are forgotten, or left out by well-intentioned programmers that plan to write them later but then never get around to it.


# Create a python program that reads one or more Python source files and identifies functions that are not immediately preceded by a comment.

# Extra:
# For the purposes of this exercise, assume that any line that begins with def, followed by a space, is the beginning of a function definition.
# Assume that the comment character, #, will be the first character on the previous line when the function has a comment.
# Display the names of all of the functions that do not have a comment, along with the file name and line number where the function definition is located.
# The user will provide the names of one or more Python files as command line parameters (comma separated).
# Input example (correct):
# functiontest.txt

# Output example (correct):
# File: functiontest.txt contains a function [function_name_here()] on line [1] without a preceding comment.
# File: functiontest.txt contains a function [another_function_name_here()] on line [15] without a preceding comment.
# Input example (error):
# functiontest.txt, blanc

# Output example (error):
# File: functiontest.txt contains a function [function_name_here()] on line [1] without a preceding comment.
# File: functiontest.txt contains a function [another_function_name_here()] on line [15] without a preceding comment.
# Error reading file: "blanc"
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
        return [line.strip() for line in file.readlines()]


def main():
    existing_files = input("File to read: ").split(",")

    for existing_file_name in existing_files:

        file_path = os.path.join(os.getcwd(), existing_file_name.strip())
        file_lines = read_file(file_path)

        for i, line in enumerate(file_lines):
            if line.startswith("def ") and not file_lines[i - 1].startswith("#"):
                function_name = line.split()[1].split("(")[0]
                print(
                    f"""File: {existing_file_name.strip()} contains a function [{function_name
                    }()] on line [{i + 1}] without a preceding comment."""
                )


if __name__ == "__main__":
    main()
