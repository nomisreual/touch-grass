from cryptography.fernet import Fernet

# Generate a new Fernet key
key = Fernet.generate_key()

with open(".env", "a") as key_file:
    environmental_variable = f"ENCRYPTION_KEY={key.decode()}"
    key_file.write(environmental_variable)
