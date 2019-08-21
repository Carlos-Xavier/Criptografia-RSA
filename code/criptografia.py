from math import sqrt, ceil

# create a list with the alphabet
alfa = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ']


def main():
    while True:
        print(' -----------------------------------')
        print('| Choose an options:                |')
        print('|    1 - Generate public key.       |')
        print('|    2 - Encrypt.                   |')
        print('|    3 - Decrypt.                   |')
        print(' -----------------------------------')
        n_case = int(input('Your choice : '))

        if n_case == 1:
            f_key()
        elif n_case == 2:
            f_encrypt()
        elif n_case == 3:
            f_decrypt()
        else:
            break


def f_key():
    while True:
        print('\nEnter two prime numbers to generate a public key:\n')
        while True:
            p = int(input('Number p: '))

            if prime(p):
                break
            print('Number p is not prime, please type other number.')

        while True:
            q = int(input('Number q: '))

            if prime(q):
                break
            print('Number q is not prime, please type other number.')

        if p * q > 28:
            break
        print(f'The multiplication of primes {q} and {p} is not greater than the character set(27).')

    set_size = p * q
    fi = (p - 1) * (q - 1)

    print('\nEnter a co-prime number of φ (n) greater than 1:\n')
    while True:
        coPrime = int(input('Number (e): '))

        if f_mdc(fi, coPrime, -1) == 1 and coPrime < fi:
            break
        print('Number invalid. Please try other number\n')

    # create a file with a public key
    add_public_key(set_size, coPrime)

    print('\nPublic key created\n\n')


def f_encrypt():
    data_items = []
    array      = []
    
    # create a list with all capital letters
    string = str(input('\nType a sentence you want to encrypt: '))
    string = string.upper()

    print('\nPlease enter the public key values.')

    # verify data to continue encryption
    data(data_items)

    size = len(string)

    # Transform text into number, with the co-prime (e), using the fast modular exponentiation
    for i in range(0, size):
        index = f_index((string[i]))
        array.append(f_expmod(index, data_items[1], data_items[0]))

    # create a file with a encrypted sequence
    add_encrypted_sequence(array, size)

    print('\n\nSuccessfully encrypted sequence!!\n\n')


def f_decrypt():
    quotients = []
    new_quotients = []

    # Data
    while True:
        print()
        p = int(input('Number p: '))
        q = int(input('Number q: '))
        e = int(input('Number e: '))

        print(f'\np: {p} -- q: {q} -- e: {e}\n')
        continue_ = str(input('Do you wish to continue (Y/N)? '))

        if (continue_ == 'Y' or continue_ == 'y'):
            break

    set_size = p * q
    fi = (p - 1) * (q - 1)

    # Save quotients between fi and co-prime (e) in a list
    size_values = f_euclides(e, fi, quotients)

    ''' calculating the modular inverse '''
    f_new_quotients(quotients, new_quotients, size_values, 0)

    d = reverse(new_quotients, size_values)
    d = check(d, fi)

    # clear list
    del new_quotients[0:size_values]

    # read txt
    array = readtxt()
    size = len(array)

    # Transform numbers into text again, with the modular inverse, using the fast modular exponentiation
    for i in range(0, size):
        new_quotients.append(f_expmod(int(array[i]), int(d), set_size))

    # create a file with a decrypted sequence
    add_decrypted_sequence(new_quotients, size)

    print('\n\nSuccessfully decrypted sequence!!\n\n')


def f_new_quotients(values, new_values, size, i):
    n = 1
    while size > 0:
        if i == 0:
            new_values.append(values[size - 1] * n)
        else:
            new_values.append(values[size - 1] * new_values[i - 1] + n)
            n = new_values[i - 1]
        size -= 1
        i += 1


def reverse(new_values, size_values):
    if size_values % 2 == 0:
        value_one = new_values[size_values - 2] * -1
        value_two = new_values[size_values - 1]
    if size_values % 2 != 0:
        value_one = new_values[size_values - 2]
        value_two = new_values[size_values - 1] * -1
    if abs(value_one) >= abs(value_two):
        return int(value_one)
    else:
        return int(value_two)


def check(d, fi):
    if d < 0:
        return d + fi
    elif d > fi:
        return fi - d
    else:
        return d


def f_euclides(coPrime, fi, values):
    while coPrime != 0:
        n = fi % coPrime
        r = fi // coPrime
        fi = coPrime
        coPrime = n
        values.append(r)

    if len(values) == 2:
        aux = values[0]
        values[0] = 0
        values[1] = aux
        return len(values)
    else:
        return len(values) - 1


def readtxt():
    while True:
        name = str(input('\nEnter a filename with the string to decrypt: '))
        try:
            archive = open(f'{name}.txt', 'r')
            break
        except (FileNotFoundError, NameError):
            print("File not found, please try again")

    for linha in archive:
        aux = linha
        aux = aux.split()

    archive.close()
    return aux


def add_public_key(set_size, coPrime):
    archive = open('PublicKey.txt', 'w')

    archive.write('Public Key:\n')
    archive.write(f'coPrime (e): {coPrime}\nn: {set_size}')
    archive.close()


def data(data_items):
    set_aux = int(input("\nPlease enter the value of 'n': "))
    prime_aux = int(input("Please enter the value of 'e': "))

    data_items.append(set_aux)
    data_items.append(prime_aux)


def add_encrypted_sequence(array, size):
    name = str(input('\nEnter a name for the file: '))
    archive = open(f'{name}.txt', 'w')

    for i in range(0, size):
        archive.write(f'{array[i]} ')
    archive.close()


def add_decrypted_sequence(array, size):
    archive = open('DecryptedSentence.txt', 'w')

    for i in range(0, size):
        n = array[i]
        letter = alfa[n]
        archive.write(f'{letter}')
    archive.close()


def f_index(index):
    for i in range(0, 27):
        if alfa[i] == index:
            break
    return i


def f_expmod(index, coPrime, set_size):
    aux = 1
    while coPrime > 0:
        if coPrime % 2 == 0:
            index = (index * index) % set_size
            coPrime = coPrime/2
        else:
            aux = (index * aux) % set_size
            coPrime = coPrime - 1
    return aux


def f_mdc(fi, coPrime, rest):
    while rest != 0:
        rest = fi % coPrime
        fi = coPrime
        coPrime = rest
    return fi


def prime(n):
    i = 3
    if n % 2 == 0 and n != 2:
        return False
    else:
        while i <= ceil(sqrt(n)):
            if n % i == 0:
                return False
            i += 2
        return True


main()
