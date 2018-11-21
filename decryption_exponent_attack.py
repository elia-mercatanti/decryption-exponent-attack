import math
import random
import time
import RSA


# Print the Main Menu
def menu():
    print("---- Decryption Exponent Attack ----\n")
    print("1) Execute Decryption Exponent Attack.")
    print("2) Test Decryption Exponent Attack.")
    print("3) Quit.\n")
    try:
        choice = int(input("Select a function to run: "))
        if 1 <= choice <= 3:
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


# Implement the decryption exponent attack, return a non trivial factor of n and the total number of iterations
def decryptionexp(n, d, e):
    m, iteration = e*d - 1, 0
    while m % 2 == 0:
        m //= 2
    while True:
        iteration += 1
        x = random.randint(1, n-1)
        if math.gcd(x, n) != 1:
            return x
        v = pow(x, m, n)
        if v == 1:
            continue
        while v != 1:
            v0, v = v, pow(v, 2, n)
        if v0 != -1 and v0 != n-1:
            return math.gcd(v0 + 1, n), iteration


def test_decryptionexp():
    n = get_input("\nInsert the modulo n: ")
    d = get_input("Insert the exponent d of the private key: ")
    e = get_input("Insert the exponent e of the public key: ")
    factor, iteration = decryptionexp(n, d, e)
    print("\nNon Trivial Factor of n:", factor)
    print("Total Algorithm Iterations:", iteration, "\n")


def test_random_modules():
    k = get_input("\nInsert the size of modules to be randomly generated (number of bits): ")
    iteration = get_input("Insert the total number of random modules to be tested: ")
    # Begin the test
    iteration_sum = 0
    decryptionexp_exec_time = []
    input("\nPress Enter to begin the test.\n")
    print("Test is Started.")
    for i in range(iteration):
        public_key, private_key = RSA.rsa_keys(k)

        start = time.perf_counter()
        _, alg_iterations = decryptionexp(public_key[1], private_key[0], public_key[0])
        end = time.perf_counter()
        decryptionexp_exec_time.append(end - start)

        iteration_sum += alg_iterations
        print("\rCurrently Tested Modules:", i + 1, end="", flush=True)
    print("\nTest is completed.\n")

    # Calculate and display average algorithm iterations, average execution time and time variance
    avg_exec_time = sum(decryptionexp_exec_time) / iteration
    var_exec_time = sum(map(lambda x: (x - avg_exec_time) ** 2, decryptionexp_exec_time)) / iteration
    print("- Test Results -")
    print("Average Algorithm Iterations:", iteration_sum / iteration)
    print("Average Execution Time:", avg_exec_time, "seconds")
    print("Variance of Execution Time:", var_exec_time, "seconds^2\n")


def main():
    while True:
        # Ask the user what function wants to run
        choice = menu()

        # Execute the function requested by the user
        try:
            if choice == 1:
                test_decryptionexp()
            elif choice == 2:
                test_random_modules()
            elif choice == 3:
                exit(0)
        except ValueError:
            print("\nYou must enter an integer\n")
        input("Press Enter to continue.\n")


if __name__ == '__main__':
    main()
