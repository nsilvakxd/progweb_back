from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import vakinha_repository, vakinha_model
from user.user_model import User

# --- Serviços da Vakinha ---

def create_new_vakinha(db: Session, vakinha: vakinha_model.VakinhaCreate, admin_user: User) -> vakinha_model.Vakinha:
    # A verificação de 'admin' é feita no controller com require_role
    return vakinha_repository.create_vakinha(db, vakinha, admin_user)

def get_open_vakinhas_list(db: Session) -> list[vakinha_model.Vakinha]:
    return vakinha_repository.get_open_vakinhas(db)

def get_vakinha_details(db: Session, vakinha_id: int) -> vakinha_model.Vakinha:
    db_vakinha = vakinha_repository.get_vakinha_by_id(db, vakinha_id)
    if not db_vakinha:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vakinha not found")
    return db_vakinha

def close_existing_vakinha(db: Session, vakinha_id: int, close_data: vakinha_model.VakinhaClose) -> vakinha_model.Vakinha:
    db_vakinha = get_vakinha_details(db, vakinha_id)
    
    if db_vakinha.status == vakinha_model.VakinhaStatus.closed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vakinha already closed")
        
    return vakinha_repository.close_vakinha(db, db_vakinha, close_data)

# --- Serviços de Contribuição ---

def add_new_contribution(db: Session, contribution: vakinha_model.ContributionCreate, vakinha_id: int, user: User) -> vakinha_model.Contribution:
    db_vakinha = get_vakinha_details(db, vakinha_id)
    
    if db_vakinha.status == vakinha_model.VakinhaStatus.closed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot contribute to a closed vakinha")
        
    return vakinha_repository.create_contribution(db, contribution, vakinha_id, user)