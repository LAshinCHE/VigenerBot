def vigenere_encrypt(plaintext, key):
    encrypted = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            offset = 65 if plaintext[i].isupper() else 97
            key_offset = 65 if key[i % key_length].isupper() else 97
            value = (ord(plaintext[i]) - offset + ord(key[i % key_length]) - key_offset) % 26
            encrypted.append(chr(value + offset))
        else:
            encrypted.append(plaintext[i])
    return ''.join(encrypted)

def vigenere_decrypt(ciphertext, key):
    decrypted = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            offset = 65 if ciphertext[i].isupper() else 97
            key_offset = 65 if key[i % key_length].isupper() else 97
            value = (ord(ciphertext[i]) - offset - (ord(key[i % key_length]) - key_offset)) % 26
            decrypted.append(chr(value + offset))
        else:
            decrypted.append(ciphertext[i])
    return ''.join(decrypted)

