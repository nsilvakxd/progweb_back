# generate_hash.py
from passlib.context import CryptContext

# Esta é a mesma configuração do seu arquivo security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# --- Gere os hashes para suas senhas ---
hash_admin = get_password_hash("admin123")
hash_nathan = get_password_hash("nathan123")

print("\n--- HASHES GERADOS (COPIE CUIDADOSAMENTE) ---\n")
print(f"Para admin@example.com (senha: admin123):")
print(f"{hash_admin}")
print("\n-------------------------------------------------\n")
print(f"Para nathan@gmail.com (senha: nathan123):")
print(f"{hash_nathan}")
print("\n-------------------------------------------------\n")