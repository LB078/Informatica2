# Implement a program that determines and displays the number of unique characters in a string entered by the user.
# For example, Hello, World! has 10 unique characters while zzz has only 1 unique character.

# Criteria:
# Use only dictionaries to solve this problem (create a function: unique_chars_dict).
# Use only sets to solve this problem (create a function: unique_chars_set).
# Make sure to implement both functions!
# Input example:
# Hello, World!

# Output example:
# Unique characters: 10

def unique_chars_dict(string_input: str) -> int:
    new_dict = dict()
    for char in string_input:
        new_dict[char] = True

    return len(new_dict.keys())


def unique_chars_set(string_input: str) -> int:
    new_set = set()
    for char in string_input:
        new_set.add(char)

    return len(new_set)


def main():
    string_input = input("Enter string: ")

    print(unique_chars_dict(string_input))
    print(unique_chars_set(string_input))


if __name__ == "__main__":
    main()
