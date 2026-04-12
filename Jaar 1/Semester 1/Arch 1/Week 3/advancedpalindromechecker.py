# A string is a palindrome if it is identical forward and backward.
# For example “anna”, “civic”, “level” and “hannah” are all examples of palindromic words.
# Write a program that reads a string from the user and uses a loop to determines whether or not it is a palindrome.
# Display the result, including a meaningful output message.

# Extra (additional challenge):
# Extend your solution so that is also ignores punctuation marks (like , . ? ! ;)
# Extend your solution so that it treats uppercase and lowercase letters as equivalent.
# Input example:
# String: anna
# String: hannah
# String: lepels
# Output example:
# "anna" is a palindrome
# "hannah" is a palindrome
# "lepels" is not a palindrome


def replaceText(value: str, replacements) -> str:
    for replacement in replacements:
        value = value.replace(replacement, "")

    return value


def main():
    palindrome_input = input("Input palindrome: ").lower()

    palindrome_input = replaceText(palindrome_input, (",", ".", "?", "!", ";", " "))

    palindrome_length = len(palindrome_input)

    if palindrome_length % 2 == 1:
        palindrome_length -= 1

    part_length = int(palindrome_length / 2)

    succeeded = True

    for index in range(part_length):
        if not palindrome_input[index] == palindrome_input[-(index + 1)]:
            succeeded = False
            break

    if succeeded:
        print(f"{palindrome_input} is a palindrome")
    else:
        print(f"{palindrome_input} is not a palindrome")


if __name__ == "__main__":
    main()

# first_part = palindrome_input[:part_length]
# second_part = palindrome_input[-part_length:]


# if first_part == reverse(second_part):
#     print(f"{palindrome_input} is a palindrome")
# else:
#     print(f"{palindrome_input} is not a palindrome")
