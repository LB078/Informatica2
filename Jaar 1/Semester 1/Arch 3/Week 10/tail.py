# In addition to head (A3W10P1), Unix-based operating systems also typically include a tool named tail.
# It displays the last 10 lines of a file whose name is provided as a command line parameter.
# Write a Python program that provides the same behavior.

# Note:
# There are several different approaches to solving this problem. Implement the three options and experiment with files with large content. Analyse the performance of each option (measure execution time of each solution).

# Options:
# is to load the entire contents of the file into a list and then display the last 10 elements.
# is to read the contents of the file twice, once to count the lines, and a second time to display the last 10 lines.
# Options one and two are not desirable when working with large files. Another solution exists that only requires you to read the file once, and only requires you to store 10 lines from the file at one time.
# Criteria:
# Use sys.argv to get the file from running
# Input example (correct):
# python3 tail.py randomfile.txt

# Output example (correct):
# this is line #91
# this is line #92
# this is line #93
# this is line #94
# this is line #95
# this is line #96
# this is line #97
# this is line #98
# this is line #99
# this is line #100
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
    maxLines: int = 10,
    reverse: bool = False,
) -> list:
    try:
        with open(filePath, "r") as file:
            if reverse:
                return [line.strip() for line in file.readlines()[-maxLines:]]

            return [line.strip() for line in file.readlines()[:maxLines]]

    except FileNotFoundError:
        return [f'Error reading file: "{fileName}"']
    except IndexError:
        return ['Error reading file: ""']


def main():
    if len(sys.argv) != 2:
        print("Error reading file")
        return

    fileName = sys.argv[1]
    filePath = os.path.join(os.getcwd(), fileName)

    if not validateFile(filePath):
        print("Error reading file:", fileName)
        return

    fileLines = openFile(filePath, fileName, reverse=True)

    for lineIndex in range(min(10, len(fileLines))):
        print(fileLines[lineIndex])


if __name__ == "__main__":
    main()
