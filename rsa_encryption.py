import libnum
import random
from math import gcd

PRIME_BIT_LENGTHS = [4, 8, 16, 32]
PLAIN_TEXTS = ["apple", "banana", "I like apple", "+=-*", "julius caeser"]

def generate_e(phi: int) -> int:
    if phi <= 3:
        raise ValueError("phi must be greater than 3 to find a valid e")

    while True:
        e = random.randrange(3, phi, 2)
        if gcd(e, phi) == 1:
            return e
        
def generate_key_pair(prime_bit_length: int) -> tuple:
    p = libnum.generate_prime(prime_bit_length)
    q = libnum.generate_prime(prime_bit_length)
    while q == p:
        q = libnum.generate_prime(prime_bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_e(phi)
    d = libnum.invmod(e, phi)
    return (e, n), (d, n)

def encrypt_message(public_key: tuple, plain_text: str) -> list:
    e, n = public_key
    cipher_text = []
    for char in plain_text:
        encrypted_char = pow(ord(char), e, n)
        cipher_text.append(encrypted_char)
    return cipher_text

def decrypt_message(private_key: tuple, cipher_text: list) -> str:
    d, n = private_key
    plain_text = ''.join(chr(pow(char, d, n)) for char in cipher_text)
    return plain_text

# Test
def test_scenario():
    NUM_OF_TESTS = 1000
    
    for _ in range(NUM_OF_TESTS):
        prime_bit_length = random.choice(PRIME_BIT_LENGTHS)
        public_key, private_key = generate_key_pair(prime_bit_length)

        plain_text = random.choice(PLAIN_TEXTS)

        cipher_text = encrypt_message(public_key, plain_text)

        decrypted_text = decrypt_message(private_key, cipher_text)
        if plain_text == decrypted_text:
            print(f"Key Bit Length: {prime_bit_length} \nPublic key: {public_key}\nPrivate key: {private_key}\nPlain text: {plain_text}\nCipher text: {cipher_text}\nDecrypted text: {decrypted_text}\n**********")
            continue
        else:
            print(f"Key Bit Length: {prime_bit_length} \nPublic key: {public_key}\nPrivate key: {private_key}\nPlain text: {plain_text}\nCipher text: {cipher_text}\nDecrypted text: {decrypted_text}\n**********")
            print("Decryption failed")
            break
    
    print("All tests passed")


if __name__ == '__main__':
    test_scenario()