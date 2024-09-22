import bcrypt

# Generate a hashed password
password = 'Varun@123'
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed_password.decode('utf-8'))  # Store this in the database
