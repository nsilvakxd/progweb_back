from sqlalchemy.orm import Session, joinedload
from . import vakinha_model
from user.user_model import User
from datetime import datetime

# --- Funções da Vakinha ---

def create_vakinha(db: Session, vakinha: vakinha_model.VakinhaCreate, admin_user: User) -> vakinha_model.Vakinha:
    db_vakinha = vakinha_model.Vakinha(
        **vakinha.model_dump(),
        created_by_id=admin_user.id,
        status=vakinha_model.VakinhaStatus.open
    )
    db.add(db_vakinha)
    db.commit()
    db.refresh(db_vakinha)
    return db_vakinha

def get_open_vakinhas(db: Session) -> list[vakinha_model.Vakinha]:
    """Busca vakinhas abertas, carregando quem criou."""
    return (
        db.query(vakinha_model.Vakinha)
        .options(joinedload(vakinha_model.Vakinha.created_by))
        .filter(vakinha_model.Vakinha.status == vakinha_model.VakinhaStatus.open)
        .order_by(vakinha_model.Vakinha.created_at.desc())
        .all()
    )

def get_vakinha_by_id(db: Session, vakinha_id: int) -> vakinha_model.Vakinha | None:
    """Busca uma vakinha e todas as suas contribuições e usuários associados."""
    return (
        db.query(vakinha_model.Vakinha)
        .options(
            joinedload(vakinha_model.Vakinha.created_by),
            joinedload(vakinha_model.Vakinha.contributions)
            .joinedload(vakinha_model.Contribution.user)
        )
        .filter(vakinha_model.Vakinha.id == vakinha_id)
        .first()
    )

def close_vakinha(db: Session, db_vakinha: vakinha_model.Vakinha, close_data: vakinha_model.VakinhaClose) -> vakinha_model.Vakinha:
    db_vakinha.status = vakinha_model.VakinhaStatus.closed
    db_vakinha.closed_at = datetime.now()
    db_vakinha.amount_spent = close_data.amount_spent
    db_vakinha.amount_leftover = close_data.amount_leftover
    
    db.add(db_vakinha)
    db.commit()
    db.refresh(db_vakinha)
    return db_vakinha

# --- Funções de Contribuição ---

def create_contribution(db: Session, contribution: vakinha_model.ContributionCreate, vakinha_id: int, user: User) -> vakinha_model.Contribution:
    db_contribution = vakinha_model.Contribution(
        **contribution.model_dump(),
        vakinha_id=vakinha_id,
        user_id=user.id
    )
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution