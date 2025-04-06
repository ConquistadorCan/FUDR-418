import time

import libnum
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

from rsa_encryption import generate_key_pair, encrypt_message, decrypt_message

def get_prime_pair(bit_length: int, n: int):
    start = 1 << bit_length - 1
    end = (1 << bit_length) - 1
    total = end - start + 1
    print(f"Finding prime pairs in range: {start} to {end}")

    for p in range(start, end+1):
        # percent = total//100
        # current_percent = (counter/total)*100

        """if percent != 0 and counter % percent == 0:
            print(f"Checked {current_percent:.2f}% of numbers")"""

        if n % p == 0:
            q = n // p
            return (p, q), ((p-start)/total)*100

    raise ValueError("No prime pair found for the given n.")

def generate_d_from_known(prime_pair: tuple, public_key: tuple) -> int:
    p, q = prime_pair
    e, n = public_key
    phi = (p - 1) * (q - 1)
    d = libnum.invmod(e, phi)
    return d

def brute_force_attack(public_key: tuple, cipher_text: list, plain_text: str, bit_length):
    e, n = public_key

    prime_pair, current_percent = get_prime_pair(bit_length, n)

    d = None
    decrypted_message = None

    d = generate_d_from_known(prime_pair, public_key)
    decrypted_message = decrypt_message((d, n), cipher_text)

    if decrypted_message == plain_text:
        return decrypted_message, current_percent

    if d is None or decrypted_message is None:
        raise ValueError("No valid prime pair found for the given n.")

def test_scenario():
    PLAIN_TEXT = "apple"
    NUM_OF_TESTS = 1
    PRIME_BIT_LENGTHS = [4,8,16,32]

    experiments = []
    # for PRIME_BIT_LENGTH in PRIME__BIT_LENGTHS:
    for PRIME_BIT_LENGTH in range(4, 33, 2):
        for _ in range(NUM_OF_TESTS):
            print(f"Testing brute force attack with prime bit length: {PRIME_BIT_LENGTH}")
            
            start = time.time()
            
            public_key, private_key = generate_key_pair(PRIME_BIT_LENGTH)

            cipher_text = encrypt_message(public_key, PLAIN_TEXT)

            print("*"*50)
            
            try:
                decrypted_message, current_percent = brute_force_attack(public_key, cipher_text, PLAIN_TEXT, PRIME_BIT_LENGTH)

                if decrypted_message == PLAIN_TEXT:
                    print(f"Brute Force SUCCESS \nPublic key: {public_key} \nPrivate key: {private_key} \nDecrypted message: {decrypted_message} \nCipher text: {cipher_text}")
                else:
                    print(f"Brute Force FAILED \nPublic key: {public_key} \nPrivate key: {private_key} \nDecrypted message: {decrypted_message} \nCipher text: {cipher_text}")
                    return
            except ValueError as e:
                print(f"Message could not decrypted: {e}")
                return
            
            total_time = time.time() - start
            print(f"Current percent: {current_percent:.2f}%")
            print(f"Time taken: {total_time} seconds")
            print("*"*50)
            worst_case_time = total_time * 100 / current_percent

            experiments.append((PRIME_BIT_LENGTH, total_time, worst_case_time, current_percent))

    return experiments
    
def plot_experiments(experiments):
    x = [exp[0] for exp in experiments]
    y = [exp[1] for exp in experiments]

    plt.plot(x, y, marker="o")
    plt.xlabel("Prime Bit Length")
    plt.ylabel("Time (seconds)")
    plt.title("Brute Force Attack Time vs Prime Bit Length")
    plt.show()

def calculate_worst_case_time(experiments):
    worst_case_times = {}

    for prime_bit_length, _, worst_case_time, _ in experiments:
        if prime_bit_length not in worst_case_times:
            worst_case_times[prime_bit_length] = []
        worst_case_times[prime_bit_length].append(worst_case_time)
    
    avg_worst_case_times = {k: sum(v)/len(v) for k, v in worst_case_times.items()}
    return avg_worst_case_times

def exponential_func(x, a, b):
    return a * (2 ** (b * x))

def estimate_256_bit(experiments):
    avg_worst_case_times = calculate_worst_case_time(experiments)

    popt, _ = curve_fit(exponential_func, list(avg_worst_case_times.keys()), list(avg_worst_case_times.values()), maxfev=10000)
    a, b = popt

    estimated_256 = exponential_func(128, a, b) # 256-bit key is composed of two 128-bit primes
    print(f"Estimated time for 256-bit key: {estimated_256} seconds")
    return estimated_256

if __name__ == "__main__":
    experiments = test_scenario()

    plot_experiments(experiments)

    estimated_time = estimate_256_bit(experiments)

    with open("experiments.txt", "a") as f:
        f.write("Prime Bit Length, Time (seconds), Worst Case Time (seconds), Percentage\n")
        for exp in experiments:
            f.write(f"{exp}\n")
        f.write(f"Estimated time for 256-bit key: {estimated_time} seconds\n")
        print("Experiments saved to experiments.txt")
        