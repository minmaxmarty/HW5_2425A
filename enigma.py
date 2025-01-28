
import json
#----------------------Consts-------------------------#
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
#----------------------out exception------------------------#
class JSONFileException(Exception):
    def __init__(self, message = LOAD_FILE_ERROR):
        Exception.__init__(self, message)
#---------------------key finder based on value------------------------#
def find_key(my_dict, value):
    for k, v in my_dict.items():
        if v == value:
            return k
#----------------------change wheels helper functions------------------------#
def calculate_wheel_value(wheel_list, number):
    w1, w2, w3 = wheel_list[0], wheel_list[1], wheel_list[2]
    return ((W1_COEFFICIENT * w1) - w2 + w3) % MOD_VALUE

def change_based_on_wheel_value(wheel_list, number, coefficient):
    number_to_add = calculate_wheel_value(wheel_list, number)
    if number_to_add != 0:
        return (number + coefficient * number_to_add) % MOD_VALUE
    else:
        return (number + coefficient) % MOD_VALUE
#----------------------mod helper functions-------------------------#
def is_even(number):
    return number % DIVISIBLE_BY_TWO == 0

def divisible_by_ten(number):
    return number % DIVISIBLE_BY_TEN == 0

def divisible_by_three(number):
    return number % DIVISIBLE_BY_THREE == 0
#----------------------wheel helper functions-------------------------#
def change_w1(wheel_list):
    w1 = wheel_list[0]
    if w1 <= W1_UPPER_LIMIT:
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
    match idx:
        case 0:
            change_w1(wheel_list)
        case 1:
            change_w2(wheel_list, counter)
        case 2:
            change_w3(wheel_list, counter)
#----------------------encryption helper function-------------------------#
def encryption_algorithm(self, wheels_list, str_list, c, c_idx):
    i = self.hash_map[c]
    i = change_based_on_wheel_value(wheels_list, i, ADD)
    c1 = find_key(self.hash_map, i)
    c2 = self.reflector_map[c1]
    i = self.hash_map[c2]
    i = change_based_on_wheel_value(wheels_list, i, SUBTRACT)
    c3 = find_key(self.hash_map, i)
    str_list[c_idx] = c3
    return
#----------------------class--------------------------#
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
                encrypted_counter += 1
            # change wheel values
            for w_idx, _ in enumerate(wheels_list):
                change_wheels(wheels_list, w_idx, encrypted_counter)
        return ''.join(str_list) # return encrypted message


#------------------------file loader-------------------------#
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
#-----------------------------------------------------#