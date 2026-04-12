# Unix-based operating systems usually include a tool named head.
# It displays the first 10 lines of a file whose name is provided as a command line parameter.
# Write a Python program that provides the same behavior.

# Criteria:
# Use sys.argv to get the file from running
# Input example (correct):
# python3 head.py randomfile.txt

# Output example (correct):
# this is line #1
# this is line #2
# this is line #3
# this is line #4
# this is line #5
# this is line #6
# this is line #7
# this is line #8
# this is line #9
# this is line #10
# Input example (error):
# blanc

# Output example (error):
# Error reading file: "blanc"

import sys
import os


def validateFile(filePath: str) -> bool:
    if not os.path.isfile(filePath):
        return False

    if not os.access(filePath, os.R_OK):
        return False

    return True


def openFile(
    filePath: str,
    fileName: str,
) -> list:
    try:
        with open(filePath, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return [f'Error reading file: "{fileName}"']
    except IndexError:
        return ['Error reading file: ""']
    pass


def main():
    print(sys.argv)

    if len(sys.argv) != 2:
        print("Error reading file")
        return

    fileName = sys.argv[1]
    filePath = os.path.join(os.getcwd(), fileName)

    if not validateFile(filePath):
        print("Error reading file:", fileName)
        return

    fileLines = openFile(filePath, fileName)

    for lineIndex in range(min(10, len(fileLines))):
        print(fileLines[lineIndex])


if __name__ == "__main__":
    main()
