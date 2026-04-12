# In an application a valid password must be a combination of digits, uppercase and lowercase letters  and only four symbols * @ ! ?.
# Implement a Python program that asks the password of the user and checks if it is a valid password.

# Criteria:
# The length of the password must not be less than 8 characters and must not be more than 20 characters.
# In case the password is not valid, the user can try maximum three times to validate the password.
# Print Valid on a validated password and Invalid on a unvalidated password.
# Use sets and set operations to solve this problem.
# Input example:
# Password: B4s3c4p

# Output example:
# Password is invalid

upper_caracter_set = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
lower_caracter_set = set("abcdefghijklmnopqrstuvwxyz")
digit_set = set("0123456789")
symbol_set = set("*@!?")


def main():

    for _ in range(3):
        password = input("Password: ")
        if len(password) < 8 or len(password) > 20:
            print("Password is invalid")
        else:
            password_set = set(password)

            password_set.difference_update(upper_caracter_set)
            password_set.difference_update(lower_caracter_set)
            password_set.difference_update(digit_set)
            password_set.difference_update(symbol_set)

            if len(password_set) == 0:
                print("Password is valid")
                break
            else:
                print("Password is invalid")


if __name__ == "__main__":
    main()
