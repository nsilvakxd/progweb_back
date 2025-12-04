import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# CORREÇÃO: importando de 'user' (singular) em vez de 'users'
from user import user_controller
from roles import role_controller
from auth import auth_controller
# --- NOVO ---
from vakinha import vakinha_controller
# ------------
from database import engine, Base

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Gestão de Gastos", version="0.2.0")

# Bloco de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://app-front-vakinha.onrender.com",  # URL do front-end em produção
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas dos controllers
app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)
# --- NOVO ---
app.include_router(vakinha_controller.router)
# ------------

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)