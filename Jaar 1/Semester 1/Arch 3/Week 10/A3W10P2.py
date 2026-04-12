import os
import sys


def tail_option_one(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            print("".join(lines[-11:]))
    except FileNotFoundError:
        print(f'Error reading file: "{file_name}"')


def tail_option_two(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            total_lines = len(lines)
            print("".join(lines[total_lines - 11:]))

    except FileNotFoundError:
        print(f'Error reading file: "{file_name}"')


def tail_option_three(file_name):
    try:
        with open(os.path.join(sys.path[0],  file_name), 'r') as file:
            lines = []
            for line in file:
                lines.append(line)
                if len(lines) > 10:
                    lines.pop(0)
            print("".join(lines))

    except FileNotFoundError:
        print(f'Error reading file: "{file_name}"')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tail.py <filename>")
    else:
        tail_option_three(sys.argv[1])
