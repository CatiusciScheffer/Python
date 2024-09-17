from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash('1')
print(f'senha:{hashed_password}')