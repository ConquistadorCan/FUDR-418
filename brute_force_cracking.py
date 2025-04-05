import time

import libnum

from rsa_encryption import generate_key_pair, encrypt_message, decrypt_message

def get_prime_pair(bit_length: int, n: int) -> tuple:
    start = 1 << bit_length - 1
    end = (1 << bit_length) - 1
    total = end - start + 1
    print(f"Finding prime pairs in range: {start} to {end}")

    for counter, p in enumerate(range(start, end+1)):
        percent = total//100

        if percent != 0 and counter % percent == 0:
            print(f"Checked {(counter/total)*100:.2f}% of numbers")

        if n % p == 0:
            q = n // p
            return p, q

    raise ValueError("No prime pair found for the given n.")

def generate_d_from_known(prime_pair: tuple, public_key: tuple) -> int:
    p, q = prime_pair
    e, n = public_key
    phi = (p - 1) * (q - 1)
    d = libnum.invmod(e, phi)
    return d

def brute_force_attack(public_key: tuple, cipher_text: list, plain_text: str, bit_length):
    e, n = public_key

    prime_pair = get_prime_pair(bit_length, n)

    d = None
    decrypted_message = None

    d = generate_d_from_known(prime_pair, public_key)
    decrypted_message = decrypt_message((d, n), cipher_text)

    if decrypted_message == plain_text:
        return decrypted_message

    if d is None or decrypted_message is None:
        raise ValueError("No valid prime pair found for the given n.")

def test_scenario():
    PRIME_BIT_LENGTH = 30
    PLAIN_TEXT = "apple"
    NUM_OF_TESTS = 1

    start = time.time()
    print(f"Testing brute force attack with prime bit length: {PRIME_BIT_LENGTH}")

    for _ in range(NUM_OF_TESTS):
        public_key, private_key = generate_key_pair(PRIME_BIT_LENGTH)

        cipher_text = encrypt_message(public_key, PLAIN_TEXT)

        print("*"*50)
        
        try:
            decrypted_message = brute_force_attack(public_key, cipher_text, PLAIN_TEXT, PRIME_BIT_LENGTH)

            if decrypted_message == PLAIN_TEXT:
                print(f"Brute Force SUCCESS \nPublic key: {public_key} \nPrivate key: {private_key} \nDecrypted message: {decrypted_message} \nCipher text: {cipher_text}")
            else:
                print(f"Brute Force FAILED \nPublic key: {public_key} \nPrivate key: {private_key} \nDecrypted message: {decrypted_message} \nCipher text: {cipher_text}")
                return
        except ValueError as e:
            print(f"Message could not decrypted: {e}")
            return
        
    print(f"Time taken: {time.time() - start} seconds")
    print("*"*50)

if __name__ == "__main__":
    test_scenario()