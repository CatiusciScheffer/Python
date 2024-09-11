from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash('gera hash')
print(f'senha:{hashed_password}')