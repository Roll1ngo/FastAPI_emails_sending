import secrets

# Generate a random 64-bit key
random_key = secrets.token_hex(32)
print(random_key)
