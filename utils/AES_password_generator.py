import secrets

def generate_aes_256_key():
    return secrets.token_bytes(32)

# Generate the key
aes_256_key = generate_aes_256_key()
print(aes_256_key.hex())
