import sympy
import re

t, s = sympy.symbols('t s')

lookup_dict = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26
}

def L(f):
    return sympy.laplace_transform(f, t, s, noconds=True)

def invL(f):
    return sympy.inverse_laplace_transform(f, s, t)

def fact(n):
    return sympy.factorial(n)

def to_num(char):
    return lookup_dict[char]

def to_char(num):
    return list(lookup_dict.keys())[list(lookup_dict.values()).index(num)]

def create_func(coeffs):
    func = ""
    for i in range(len(coeffs)):
        func += str(coeffs[i]) + "*((2**" + str(2*i) + ")*t**(" + str(2*i) + "+ 2))/" + str(fact(2*i)) + " + "
    return func.rstrip(" + ")

def create_inverse_func(nums):
    func = ""
    for i in range(len(nums)):
        func += str(nums[i]) + "/s**" + str(2*i + 3) + " + "
    return func.rstrip(" + ")

def read_encrypted(string):
    string = string.lower()
    length = to_num(string[0])
    keys_list = string.split('y', length + 1)
    keys = []
    for key in keys_list:
        key = string.split('z', length)
        string = key[-1]
        key = 'z'.join(key[:-1])
        key = list(map(to_num, key))

        new_list = []
        temp_sublist = []
        for num in key:
            if num == 25:
                if temp_sublist:
                    new_list.append(int(''.join(map(str, temp_sublist))))
                    temp_sublist = []
            else:
                temp_sublist.append(num)
        if temp_sublist:
            new_list.append(int(''.join(map(str, temp_sublist))))

        key = new_list
        keys.append(key)

    string = keys_list[-1]
    return string, keys

def create_encrypted(string, keys):
    string = string.lower()
    length = len(string)

    key_str = ""
    for key in keys:
        for num in key:
            print(num)
            chars = list(str(num))
            for char in chars:
                key_str += to_char(int(char))
            key_str += 'z'
        key_str += 'y'

    encrypted_str = to_char(length) + key_str + string
    return encrypted_str

def encrypt(string):
    length = len(string)
    string = string.lower()

    coeffs = list(map(to_num, list(string)))

    f = create_func(coeffs)
    terms = str(L(f)).split('+')

    nums = []
    for term in terms:
        num = term.split('/')[0].strip()
        nums.append(int(num))
    nums = [x + length for x in nums]

    key = [x // 26 for x in nums]
    string = ''.join(list(map(to_char, [x % 26 for x in nums])))

    return string, key

def decrypt(string, key):
    length = len(string)
    string = string.lower()

    nums = [x * 26 for x in key]
    for i in range(length):
        nums[i] += to_num(string[i])
    nums = [x - length for x in nums]

    f = create_inverse_func(nums)
    terms = str(invL(f)).split('+')
    nums = [x.split('*')[0] for x in terms]
    nums = [int(x) for x in nums]
    nums = list(reversed(nums))

    denoms = []
    for x in terms:
        temp = x.split('/')
        if len(temp) > 1:
            denoms.append(temp[1])
        else:
            denoms.append(1)
    denoms = [int(x) for x in denoms]
    denoms = list(reversed(denoms))

    coeffs = []
    for i in range(length):
        coeffs.append( (nums[i] * fact(2*i)) // (denoms[i] * 2**(2*i)) )

    string = ''.join(list(map(to_char, coeffs)))

    return string

to_do = int(input("Enter 1 to encrypt or 2 to decrypt: "))

if to_do == 1:
    to_encrypt_word = input("Enter word to encrypt: ")
    print("Encrypted: ", encrypt(to_encrypt_word))
if to_do == 2:
    to_decrypt_word = input("Enter word to decrypt: ")
    to_decrypt_key_length = int(input("Enter length of key: "))
    to_decrypt_key = []
    for i in range(to_decrypt_key_length):
        to_decrypt_key.append(int(input(f"Enter {i} th element of key: ")))
    print("Decrypted: ", decrypt(to_decrypt_word, to_decrypt_key))
