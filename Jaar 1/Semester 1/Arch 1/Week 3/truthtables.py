# Do some research regarding truth tables.
# Use iterative programming to solve this problem to print the truth tables for and and or.
# Implement a program that prints these two truth tables.

# Criteria:
# Use 4 states: True + True, True + False, False + True, False + False
# Input example:
# No input is given

# Output example:
# AND
# True + True = True
# ...

# OR
# ...

truth_tables = [
    {"a": True, "b": True},
    {"a": True, "b": False},
    {"a": False, "b": True},
    {"a": False, "b": False},
]


def main():
    print("AND")
    for truth_table in truth_tables:
        print(
            f"{truth_table['a']} + {truth_table['b']} = { truth_table['a'] and truth_table['b']}"
        )

    print("OR")
    for truth_table in truth_tables:
        print(
            f"{truth_table['a']} + {truth_table['b']} = { truth_table['a'] or truth_table['b']}"
        )


if __name__ == "__main__":
    main()
