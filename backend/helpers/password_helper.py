import bcrypt

# Generate a hashed password

def generate_default_password():
    try:
                
        password = 'Password@123'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')
    except Exception as e:
        print("Error in generating default password - ",e)
        return 