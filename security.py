import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

# Carrega as variáveis do arquivo .env
load_dotenv()

# --- CONSTANTES DE SEGURANÇA ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- CONFIGURAÇÃO DE SENHA ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- MODELO DE DADOS DO TOKEN ---
class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None # Precisamos da role aqui

# --- FUNÇÕES DE SENHA ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- FUNÇÕES DE TOKEN JWT ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Esta função não é mais necessária aqui, 
# pois auth_service.py tem uma 'get_current_user' mais completa
# que já busca o usuário no banco.