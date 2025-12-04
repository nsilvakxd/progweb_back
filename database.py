import os # Importar 'os'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv # Importar 'load_dotenv'

load_dotenv() # Carregar as variáveis do .env

# 1. Determinar se está em produção ou desenvolvimento
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# 2. Configurar a URL do banco de dados baseado no ambiente
if ENVIRONMENT == "production":
    # URL do banco de dados de produção no Render
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
else:
    # URL do banco de dados local (desenvolvimento)
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
    
    if SQLALCHEMY_DATABASE_URL is None:
        raise ValueError("DATABASE_URL não foi definida no arquivo .env para desenvolvimento")

# 3. Cria a "engine" do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Cria uma fábrica de sessões (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Cria uma classe Base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # Entrega a sessão para quem a chamou
        yield db
    finally:
        # Garante que a sessão será fechada, mesmo se houver erros
        db.close()