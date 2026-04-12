MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ",": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
}


def message_to_morse(message: str) -> str | None:
    message = message.upper().strip("\"'")
    morse_message = ""
    incorrect_chars = []

    for char in message:
        if char == " ":
            morse_message += "   "
            continue

        morse_character = MORSE_CODE_DICT.get(char, None)
        if not morse_character:
            if char not in incorrect_chars:
                incorrect_chars.append(char)
            continue

        morse_message += f"{morse_character} "

    if incorrect_chars:
        print(f"Can't convert char [{','.join(incorrect_chars)}]")
        return

    return morse_message


def morse_to_message(message: str) -> str:
    words = message.split("    ")

    translated_message = ""

    for word in words:
        characters = word.split(" ")
        for char in characters:
            # https://stackoverflow.com/questions/3231250/python-list-comprehension-for-dictionaries-in-dictionaries
            alphabet_character = [
                key for key, value in MORSE_CODE_DICT.items() if value == char
            ][0]

            translated_message += alphabet_character

        translated_message += " "

    return translated_message


def translate_text(message: str) -> str | None:
    message_set = set(message)

    if len(message_set.difference(" .-")) == 0:
        return morse_to_message(message)

    return message_to_morse(message)


def main():
    message_input = input("Message? ")

    print(message_to_morse(message_input))


if __name__ == "__main__":
    main()
