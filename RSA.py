import math
import time
import random


# Print the Main Menu
def menu():
    print("---- Public Key Cryptography, RSA ----\n")
    print("1) Extended Euclidean Algorithm.")
    print("2) Fast Modular Exponentiation.")
    print("3) Miller-Rabin Test (True=Composite).")
    print("4) Prime Number Generator.")
    print("5) RSA keys Generator (Public and Private Key).")
    print("6) RSA Encryption.")
    print("7) RSA Decryption.")
    print("8) Test RSA Decryption With and Without CRT.")
    print("9) Quit.\n")
    try:
        choice = int(input("Select a function to run: "))
        if 1 <= choice <= 9:
            return choice
        else:
            print("\nYou must enter a number from 1 to 9\n")
    except ValueError:
        print("\nYou must enter a number from 1 to 9\n")
    input("Press Enter to continue.\n")


# Get input from the user
def get_input(message):
    choice = int(input(message))
    return choice


# Compute the extended euclidean algorithm, returns the GCD and the Bezout Coefficients
def ext_euclid(a, b):
    a, b = abs(a), abs(b)
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


# Compute the Fast modular exponentiation algorithm
def fast_mod_exp(a, exp, n):
    result = 1
    while exp:
        if exp & 1:
            result = result * a % n
        exp >>= 1
        a = a * a % n
    return result


# Compute the Miller-Rabin for a number given the number of rounds, return True if the number is composite
def miller_rabin_test(n, rounds=40):
    if n == 2 or n == 3:
        return False
    if n < 2 or n % 2 == 0:
        return True
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = fast_mod_exp(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = fast_mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            return True
    return False


# Generate a random k-bit prime number
def generate_prime(k, rounds=40):
    if k < 2:
        return None
    while True:
        number = random.randrange(pow(2, k - 1) + 1, pow(2, k), 2)
        if not miller_rabin_test(number, rounds):
            return number


# Generates a k-bit RSA public and private key pair
def rsa_keys(k, crt=False, rounds=40):
    if k < 5:
        return None
    k1 = int(math.ceil(k / 2))
    k2 = int(math.floor(k / 2))
    p = q = 0
    while p == q:
        p = generate_prime(k1, rounds)
        q = generate_prime(k2, rounds)
    if crt and q > p:
        p, q = q, p
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2, phi // 2)
        g, d, _ = ext_euclid(e, phi)
        if g == 1:
            public_key = (e, n)
            d = d % phi
            if d < 0:
                d += phi
            if crt:
                dp, dq, qinv = crt_pre_computation(p, q, d)
                private_key = (p, q, dp, dq, qinv)
            else:
                private_key = (d, n)
            return public_key, private_key


# Pre-computation for RSA with CRT
def crt_pre_computation(p, q, d):
    _, qinv, _ = ext_euclid(q, p)
    return d % (p - 1), d % (q - 1), qinv % p


# RSA encryption
def rsa_encryption(m, public_key):
    return fast_mod_exp(m, public_key[0], public_key[1])


# RSA decryption
def rsa_decryption(c, private_key, crt=False):
    if not crt:
        return rsa_encryption(c, private_key)
    else:
        m1 = fast_mod_exp(c, private_key[2], private_key[0])
        m2 = fast_mod_exp(c, private_key[3], private_key[1])
        h = (private_key[4] * (m1 - m2)) % private_key[0]
        return m2 + h * private_key[1]


# Tests Extended Euclidean Algorithm.
def test_ext_euclid():
    a = get_input("\nInsert the first integer: ")
    b = get_input("Insert the second integer: ")
    gcd, x, y, = ext_euclid(a, b)
    print("\nGreatest Common Divisor (GCD):", gcd)
    print("Bezout Coefficients (x, y):", "(", x, ",", y, ")\n")


# Tests Fast Modular Exponentiation
def test_fast_mod_exp():
    a = get_input("\nInsert the base: ")
    exp = get_input("Insert the exponent: ")
    n = get_input("Insert the modulo: ")
    print("\nModular Exponentiation:", fast_mod_exp(a, exp, n), "\n")


# Tests Miller-Rabin Test (True=Composite)
def test_miller_rabin():
    n = get_input("\nInsert an integer: ")
    rounds = get_input("Insert the number of rounds to execute (default=40): ")
    print("\nTest Miller-Rabin:", miller_rabin_test(n, rounds), "\n")


# Tests Prime Number Generator
def test_generate_prime():
    k = get_input("\nInsert number of bits (k>1): ")
    rounds = get_input("Insert the number of rounds for Miller-Rabin Test (default=40): ")
    print("\nGenerated Prime Number:", generate_prime(k, rounds), "\n")


# Tests RSA keys Generator (Public and Private Key)
def test_rsa_keys():
    k = get_input("\nInsert the number of bits for the module n: ")
    crt = input("Do you want to use CRT optimization? (Y or N): ")
    if crt.upper() == 'Y':
        crt = True
    else:
        crt = False
    rounds = get_input("Insert the number of rounds for Miller-Rabin Test(default=40): ")
    public_key, private_key = rsa_keys(k, crt, rounds)
    print("\nPublic Key (e, n):", public_key)
    if crt:
        print("Private Key (p, q, dp, dq, qinv):", private_key, "\n")
    else:
        print("Private Key (d, n):", private_key, "\n")


# Tests RSA Encryption
def test_rsa_encryption():
    m = get_input("\nInsert the message m: ")
    e = get_input("Insert the exponent e of the public key: ")
    n = get_input("Insert the modulo n of the public key: ")
    print("\nGenerated ciphertext c:", rsa_encryption(m, (e, n)), "\n")


# Tests RSA Decryption
def test_rsa_decryption():
    c = get_input("\nInsert the ciphertext c: ")
    d = get_input("Insert the exponent d of the private key: ")
    n = get_input("Insert the modulo n of the private key: ")
    print("\nOriginal message m:", rsa_decryption(c, (d, n)), "\n")


# Test RSA Decryption With and Without CRT (Total Execution Time on 100 random ciphertext)
def test_rsa_crt():
    p = get_input("\nInsert the first prime number p: ")
    q = get_input("Insert the second prime number q: ")
    d = get_input("Insert the exponent d of the private key: ")
    if q > p:
        p, q = q, p
    n = p * q
    private_key = (d, n)
    dp, dq, qinv = crt_pre_computation(p, q, d)
    crt_private_key = (p, q, dp, dq, qinv)
    print("\nRSA without CRT - Private Key (d, n):", private_key)
    print("RSA with CRT - Private Key (p, q, dp, dq, qinv):", crt_private_key, "\n")

    k = get_input("Insert the size of ciphertext to be randomly generated (number of bits): ")
    iteration = get_input("Insert the number of ciphertext to be tested: ")
    input("\nPress Enter to begin the test.\n")

    # Begin the test
    decryption_exec_time = 0
    crt_decryption_exec_time = 0
    print("Test is Started.")
    for i in range(iteration):
        ciphertext = random.getrandbits(k)

        # RSA Decryption without CRT
        start = time.perf_counter()
        rsa_decryption(ciphertext, private_key)
        end = time.perf_counter()
        decryption_exec_time += end - start

        # RSA Decryption with CRT
        start = time.perf_counter()
        rsa_decryption(ciphertext, crt_private_key, True)
        end = time.perf_counter()
        crt_decryption_exec_time += end - start

        print("\rCurrently Tested Ciphertexts:", i+1, end="", flush=True)

    print("\nTest is completed.\n")

    print("- RSA Decryption without CRT -")
    print("Total Execution Time on 100 Random Ciphertext:", decryption_exec_time, "seconds")
    print("\n- RSA Decryption with CRT -")
    print("Total Execution Time on 100 Random Ciphertext:", crt_decryption_exec_time, "seconds\n")


def main():
    while True:
        # Ask the user what function wants to run
        choice = menu()

        # Execute the function requested by the user
        try:
            if choice == 1:
                test_ext_euclid()
            elif choice == 2:
                test_fast_mod_exp()
            elif choice == 3:
                test_miller_rabin()
            elif choice == 4:
                test_generate_prime()
            elif choice == 5:
                test_rsa_keys()
            elif choice == 6:
                test_rsa_encryption()
            elif choice == 7:
                test_rsa_decryption()
            elif choice == 8:
                test_rsa_crt()
            elif choice == 9:
                exit(0)
        except ValueError:
            print("\nYou must enter an integer\n")
        input("Press Enter to continue.\n")


if __name__ == '__main__':
    main()
