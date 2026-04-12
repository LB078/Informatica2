# In this exercise you will create a Python program that identifies the longest word(s) in a file.

# Extra:
# Treat any group of non-white space characters as a word, even if it includes numbers or punctuation marks.

# Input example (correct):
# randomtext.txt

# Output example (correct):
# Length of longest word(s) is [11] chars
# These are all the words of that length:
# discovered., continuing., everything., interested., favourable., themselves., solicitude
# Input example (error):
# blanc

# Output example (error):
# Error reading file: "blanc"
import os


def validateFile(filePath: str) -> bool:
    return os.path.isfile(filePath) and os.access(filePath, os.R_OK)


def openFile(filePath: str) -> list:
    try:
        with open(filePath, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return [f'Error reading file: "{os.path.basename(filePath)}"']
    except IndexError:
        return ['Error reading file: ""']


def main():
    fileName = input("Enter the file name: ")
    filePath = os.path.join(os.getcwd(), fileName)

    if not validateFile(filePath):
        print("Error reading file:", fileName)
        return

    fileLines = openFile(filePath)

    longestWord = max(
        (len(word) for line in fileLines for word in line.split()), default=0
    )
    longestWords = [
        word for line in fileLines for word in line.split() if len(word) == longestWord
    ]

    print(f"Length of longest word(s) is [{longestWord}] chars")
    print("These are all the words of that length:")
    print(", ".join(longestWords))


if __name__ == "__main__":
    main()
