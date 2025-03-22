import libnum
import random
from math import gcd

KEY_BIT_LENGTH = 4
PLAIN_TEXT = None

def generate_prime(bit_length: int) -> int:
    return libnum.generate_prime(bit_length)

def generate_e(phi: int) -> int:
    if phi <= 3:
        raise ValueError("phi must be greater than 3 to find a valid e")

    while True:
        e = random.randrange(3, phi, 2)
        if gcd(e, phi) == 1:
            return e
        
def generate_key_pair(bit_length: int) -> tuple:
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    while q == p:
        q = generate_prime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_e(phi)
    d = libnum.invmod(e, phi)
    return (e, n), (d, n)

def create_plaintext(n: int) -> int:
    if n <= 1:
        raise ValueError("n must be greater than 1")

    return random.randint(1, n - 1)

def encrypt(public_key: tuple, plain_text: int) -> int:
    e, n = public_key
    
    if plain_text < 0 or plain_text >= n:
        raise ValueError("plain_text must be greater than 0 and less than n")
    
    cipher_text = pow(plain_text, e, n)
    return cipher_text

def decrypt(private_key: tuple, cipher_text: int) -> int:
    d, n = private_key

    if cipher_text < 0 or cipher_text >= n:
        raise ValueError("cipher_text must be greater than 0 and less than n")
    
    plain_text = pow(cipher_text, d, n)
    return plain_text

# Test
def test_scenario():
    num_of_tests = 1000
    for _ in range(num_of_tests):
        public_key, private_key = generate_key_pair(KEY_BIT_LENGTH)

        plain_text = PLAIN_TEXT
        if plain_text is None:            
            plain_text = create_plaintext(public_key[1])

        cipher_text = encrypt(public_key, plain_text)

        decrypted_text = decrypt(private_key, cipher_text)
        if plain_text == decrypted_text:
            print(f"Public key: {public_key}\nPrivate key: {private_key}\nPlain text: {plain_text}\nCipher text: {cipher_text}\nDecrypted text: {decrypted_text}\n**********")
            continue
        else:
            print(f"Public key: {public_key}\nPrivate key: {private_key}\nPlain text: {plain_text}\nCipher text: {cipher_text}\nDecrypted text: {decrypted_text}\n**********")
            print("Decryption failed")
            break
    
    print("All tests passed")


if __name__ == '__main__':
    test_scenario()