# users/user_controller.py
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import get_db
from . import user_service, user_model

# --- IMPORTAÇÃO NOVA ---
from auth.auth_service import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])


# --- NOVO ENDPOINT /me ---
# É importante que este endpoint venha ANTES de "/{user_id}"
@router.get("/me", response_model=user_model.UserPublic)
def read_users_me(current_user: user_model.User = Depends(get_current_user)):
    """Busca os dados do usuário autenticado atual."""
    # A dependência 'get_current_user' já faz a validação do token
    # e busca o usuário no banco de dados.
    return current_user
# --- FIM DO NOVO ENDPOINT ---


@router.post("/", response_model=user_model.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: user_model.UserCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo usuário."""
    return user_service.create_new_user(db=db, user=user)


@router.get("/", response_model=List[user_model.UserPublic],
            dependencies=[Depends(require_role("admin"))]) # <-- PROTEÇÃO ADICIONADA
def read_users(db: Session = Depends(get_db)):
    """Endpoint para listar todos os usuários (agora protegido para admins)."""
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=user_model.UserPublic,
            dependencies=[Depends(require_role("admin"))]) # <-- PROTEÇÃO ADICIONADA
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar um usuário pelo ID (agora protegido para admins)."""
    return user_service.get_user_by_id(db, user_id=user_id)


@router.put("/{user_id}", response_model=user_model.UserPublic,
            dependencies=[Depends(require_role("admin"))]) # <-- PROTEÇÃO ADICIONADA
def update_user(user_id: int, user: user_model.UserUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um usuário (agora protegido para admins)."""
    return user_service.update_existing_user(db=db, user_id=user_id, user_in=user)


@router.delete("/{user_id}", response_model=user_model.UserPublic,
              dependencies=[Depends(require_role("admin"))]) # <-- PROTEÇÃO ADICIONADA
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um usuário (agora protegido para admins)."""
    return user_service.delete_user_by_id(db=db, user_id=user_id)