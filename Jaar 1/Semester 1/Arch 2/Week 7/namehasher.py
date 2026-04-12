dict_key_value = {}


def translate_string(data: str, key_set: dict[str, str]) -> str | None:
    translated_message = ""

    for char in data:
        translated_character = key_set.get(char, None)
        if not translated_character:
            translated_message += char
            continue

        translated_message += f"{translated_character}"

    return translated_message


def encode_string(data: str, key: str = None) -> str:
    current_key_dict = {}

    if key:
        if len(key) % 2 != 0:
            print("Invalid hashvalue input")
            return

        for char in range(0, len(key), 2):
            current_key_dict[key[char]] = key[char + 1]
    else:
        current_key_dict = dict_key_value

    encoded_message = translate_string(data, current_key_dict)

    return encoded_message


def decode_string(data: str, key: str = None) -> str:
    current_key_dict = {}

    if key:
        if len(key) % 2 != 0:
            print("Invalid hashvalue input")
            return

        for char in range(0, len(key), 2):
            current_key_dict[key[char]] = key[char + 1]
    else:
        current_key_dict = {value: key for key, value in dict_key_value.items()}

    decoded_message = translate_string(data, current_key_dict)

    return decoded_message


def encode_list(data: list, key: str = None) -> list:
    return [encode_string(x, key) for x in data]


def decode_list(data: list, key: str = None) -> list:
    return [decode_string(x, key) for x in data]


def validate_values(encoded: str, decoded: str, key: str = None) -> bool:
    return encoded == encode_string(decoded, key)


def set_dict_key(key: str) -> None:
    if len(key) % 2 != 0:
        print("Invalid hashvalue input")
        return

    key_list = list(key)  # Not really needed but sempgrep is complaining about it

    for char in range(0, len(key_list), 2):
        dict_key_value[key_list[char]] = key_list[char + 1]


def get_input(
    prompt: str,
    validation_function=None,
    input_error: str = "Input error",
    repeat_on_error: bool = True,
) -> str | None:
    while True:
        input_value = input(prompt)

        if validation_function is not None:
            if not validation_function(input_value):
                print(input_error)
                if not repeat_on_error:
                    return None

        return input_value


def main():
    key = get_input(
        "Key? ",
        lambda x: len(x) % 2 == 0,
        input_error="Invalid hashvalue input",
        repeat_on_error=False,
    )

    if key:
        set_dict_key(key)
    else:
        return

    while True:

        print(
            """
[E] Encode value to hashed value
[D] Decode hashed value to normal value
[P] Print all encoded/decoded values
[V] Validate 2 values against eachother
[Q] Quit program
    """
        )
        choice = get_input(
            "Pick option: ", lambda x: x.lower() in ["e", "d", "p", "v", "q"]
        ).lower()

        if choice == "e":
            message_input = get_input("Message to encode?").split(", ")

            if len(message_input) > 0:
                [print(encoded_value) for encoded_value in encode_list(message_input)]
            else:
                print(encode_string(message_input[0]))

        elif choice == "d":
            message_input = get_input("Message to decode?").split(", ")

            if len(message_input) > 0:
                [print(decoded_value) for decoded_value in decode_list(message_input)]
            else:
                print(decode_string(message_input))
        elif choice == "q":
            break


if __name__ == "__main__":
    main()
