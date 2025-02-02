import json
import sys
# ----------------------Consts-------------------------#
ADD = 1
SUBTRACT = -1
DIVISIBLE_BY_TWO = 2
DIVISIBLE_BY_THREE = 3
DIVISIBLE_BY_TEN = 10
FIRST_W3_VALUE = 10
SECOND_W3_VALUE = 5
THIRD_W3_VALUE = 0
W1_COEFFICIENT = 2
W2_MULTIPLIER = 2
MOD_VALUE = 26
W1_UPPER_LIMIT = 8
LOAD_FILE_ERROR = "Failed to Read JSON File"


# ----------------------out exception------------------------ #
class JSONFileException(Exception):
    def __init__(self, message=LOAD_FILE_ERROR):
        Exception.__init__(self, message)


# ---------------------key finder based on value------------------------ #
def find_key(my_dict, value):
    for k, v in my_dict.items():
        if v == value:
            return k


# ----------------------change wheels helper functions------------------------ #
def calculate_wheel_value(wheel_list):
    w1, w2, w3 = wheel_list[0], wheel_list[1], wheel_list[2]
    return ((W1_COEFFICIENT * w1) - w2 + w3) % MOD_VALUE


def change_based_on_wheel_value(wheel_list, number, coefficient):
    number_to_add = calculate_wheel_value(wheel_list)
    if number_to_add != 0:
        return (number + coefficient * number_to_add) % MOD_VALUE
    else:
        return (number + coefficient) % MOD_VALUE


# ----------------------mod helper functions------------------------- #
def is_even(number):
    return number % DIVISIBLE_BY_TWO == 0


def divisible_by_ten(number):
    return number % DIVISIBLE_BY_TEN == 0


def divisible_by_three(number):
    return number % DIVISIBLE_BY_THREE == 0


# ----------------------wheel helper functions------------------------- #
def change_w1(wheel_list):
    w1 = wheel_list[0]
    if w1 < W1_UPPER_LIMIT:
        wheel_list[0] += 1
    else:
        wheel_list[0] = 1


def change_w2(wheel_list, counter):
    if is_even(counter):
        wheel_list[1] *= W2_MULTIPLIER
    else:
        wheel_list[1] -= 1


def change_w3(wheel_list, counter):
    if divisible_by_ten(counter):
        wheel_list[2] = 10
    elif divisible_by_three(counter):
        wheel_list[2] = 5
    else:
        wheel_list[2] = 0


def change_wheels(wheel_list, idx, counter):
    if idx == 0:
        change_w1(wheel_list)
    elif idx == 1:
        change_w2(wheel_list, counter)
    elif idx == 2:
        change_w3(wheel_list, counter)


# ----------------------encryption helper function------------------------- #
def encryption_algorithm(enigma, wheels_list, str_list, c, c_idx):
    i = enigma.hash_map[c]
    i = change_based_on_wheel_value(wheels_list, i, ADD)
    c1 = find_key(enigma.hash_map, i)
    c2 = enigma.reflector_map[c1]
    i = enigma.hash_map[c2]
    i = change_based_on_wheel_value(wheels_list, i, SUBTRACT)
    c3 = find_key(enigma.hash_map, i)
    str_list[c_idx] = c3
    return


# ----------------------class-------------------------- #
class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheels = wheels
        self.reflector_map = reflector_map

    def encrypt(self, message):
        str_list = [c for c in message]
        wheels_list = [num for num in self.wheels]
        encrypted_counter = 0
        for c_idx, c in enumerate(str_list):
            # encrypt
            if c.isalpha() and c.islower():
                encryption_algorithm(self, wheels_list, str_list, c, c_idx)
                encrypted_counter += 1 #non empty cases
            # change wheel values
            for w_idx, _ in enumerate(wheels_list):
                change_wheels(wheels_list, w_idx, encrypted_counter)
        return ''.join(str_list)  # return encrypted message


# ------------------------file loader------------------------- #
def load_enigma_from_path(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except IOError:
        raise JSONFileException()
    try:
        hash_map = data['hash_map']
        wheels = data['wheels']
        reflector_map = data['reflector_map']
    except KeyError:
        raise JSONFileException()

    return Enigma(hash_map, wheels, reflector_map)
# ---------------------------------------------------- #
#  ---------------------- Main ----------------------
# ---------------------------------------------------- #
def main():
    # For testing
    # test_index = 4
    # sys.argv = ["enigma.py", "-c", "config_file.json", "-i", f"tests/test{test_index}.in", "-o", f"output{test_index}.out"]
    # Ensure we have at least the required flags
    if len(sys.argv) < 5: # at least script name, the first two flags -c and -i and their files
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>")
        sys.exit(1)

    # Dictionary to store argument values
    flags_to_paths = {"-c": None, "-i": None, "-o": None}

    # Parse command-line arguments manually
    for i in range(1, len(sys.argv) - 1, 2):
        flag = sys.argv[i]
        if flag in flags_to_paths:
            flags_to_paths[flag] = sys.argv[i + 1]
        else:
            print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>")
            sys.exit(1)

    if flags_to_paths["-c"] is None or flags_to_paths["-i"] is None:
        # missing non optional flags
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>")
        sys.exit(1)

    config_path = flags_to_paths["-c"]
    input_path = flags_to_paths["-i"]
    output_path = flags_to_paths["-o"]  # can be None, print to std if non

    try:
        enigma = load_enigma_from_path(config_path)
    except JSONFileException as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        with open(input_path, 'r') as f:
            input_lines = f.readlines() ## need to read line by line
    except IOError as e:
        print("The enigma script has encountered an error")
        sys.exit(1)

    encrypted_lines = [enigma.encrypt(line) for line in input_lines]

    # Print or write to file based on the -o flag
    if output_path: # if not none
        try:
            with open(output_path, 'w') as f:
                for line in encrypted_lines:
                    f.writelines(line)
        except IOError:
            print("The enigma script has encountered an error")
            sys.exit(1)
    else:
        # If no output file, print to standard output
        for line in encrypted_lines:
            print(line)



if __name__ == "__main__":
    main()