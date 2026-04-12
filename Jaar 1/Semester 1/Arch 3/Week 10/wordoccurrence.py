# Write a program that displays the word (or words) that occur most and least frequently in a file.

# Extra:
# Your program should begin by reading the name of the file from the user.
# Then it should find the word(s) by splitting each line in the file at each space.
# Finally, any leading or trailing punctuation marks should be removed from each word.
# In addition, your program should ignore capitalization.
# As a result, apple, apple!, Apple and ApPlE should all be treated as the same word.
# Input example (correct):
# randomtext.txt

# Output example (correct):
# Most: ['so']
# Least: ['understood', 'remarkably', 'solicitude', 'mean', 'them', ...]
# Input example (error):
# blanc

# Output example (error):
# Error reading file: "blanc"
import os


def validateFile(filePath: str) -> bool:
    return os.path.isfile(filePath) and os.access(filePath, os.R_OK)


def readFile(filePath: str) -> list:
    if not validateFile(filePath):
        return [f'Error reading file: "{os.path.basename(filePath)}"']

    with open(filePath, "r") as file:
        return [line.strip() for line in file.readlines()]


def main():
    fileName = input("Enter the file name: ")
    filePath = os.path.join(os.getcwd(), fileName)

    fileLines = readFile(filePath)

    words = {}
    for line in fileLines:
        for word in line.split():
            word = word.strip(".,!?").lower()
            if word in words:
                words[word] += 1
            else:
                words[word] = 1

    max_freq = max(words.values())
    min_freq = min(words.values())

    mostFrequent = [word for word, freq in words.items() if freq == max_freq]
    leastFrequent = [word for word, freq in words.items() if freq == min_freq]

    print(f"Most: {mostFrequent}")
    print(f"Least: {leastFrequent}")


if __name__ == "__main__":
    main()
