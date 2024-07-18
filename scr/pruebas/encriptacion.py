import bcrypt

def encriptar_contrasena(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

contrasena = "098"
contrasena_encriptada = encriptar_contrasena(contrasena)

print(contrasena_encriptada)