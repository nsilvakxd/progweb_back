from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from . import vakinha_service, vakinha_model
from auth.auth_service import get_current_user, require_role
from user.user_model import User

router = APIRouter(prefix="/vakinhas", tags=["Vakinhas"])

@router.post(
    "/", 
    response_model=vakinha_model.VakinhaPublic, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))] # Protegido: Apenas Admin
)
def create_vakinha(
    vakinha: vakinha_model.VakinhaCreate, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_user) # Pega o admin logado
):
    """
    Cria uma nova Vakinha. Apenas administradores.
    """
    return vakinha_service.create_new_vakinha(db=db, vakinha=vakinha, admin_user=admin_user)

@router.get(
    "/open", 
    response_model=List[vakinha_model.VakinhaPublic],
    dependencies=[Depends(get_current_user)] # Protegido: Qualquer usuário logado
)
def list_open_vakinhas(db: Session = Depends(get_db)):
    """
    Lista todas as Vakinhas que ainda estão com status 'open'.
    """
    return vakinha_service.get_open_vakinhas_list(db)

@router.get(
    "/{vakinha_id}", 
    response_model=vakinha_model.VakinhaPublic,
    dependencies=[Depends(get_current_user)] # Protegido: Qualquer usuário logado
)
def get_vakinha_details(vakinha_id: int, db: Session = Depends(get_db)):
    """
    Busca os detalhes de uma Vakinha específica, incluindo todas as contribuições.
    """
    return vakinha_service.get_vakinha_details(db, vakinha_id)

@router.put(
    "/{vakinha_id}/close", 
    response_model=vakinha_model.VakinhaPublic,
    dependencies=[Depends(require_role("admin"))] # Protegido: Apenas Admin
)
def close_vakinha(
    vakinha_id: int,
    close_data: vakinha_model.VakinhaClose,
    db: Session = Depends(get_db)
):
    """
    Fecha uma Vakinha, definindo quanto foi gasto e quanto sobrou.
    """
    return vakinha_service.close_existing_vakinha(db, vakinha_id, close_data)

@router.post(
    "/{vakinha_id}/contribute", 
    response_model=vakinha_model.ContributionPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)] # Protegido: Qualquer usuário logado
)
def add_contribution(
    vakinha_id: int,
    contribution: vakinha_model.ContributionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Pega o usuário logado
):
    """
    Adiciona uma contribuição (pagamento) a uma Vakinha aberta.
    """
    return vakinha_service.add_new_contribution(db, contribution, vakinha_id, current_user)