import secrets

# Generate a 24-character secure random string
SECRET_KEY = secrets.token_hex(24)
print(SECRET_KEY)
