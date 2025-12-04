from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, Mapped
from pydantic import BaseModel, ConfigDict, Field
from database import Base
from user.user_model import User, UserPublic  # Importar User e UserPublic
from datetime import datetime
from typing import List, Optional
import enum

# --- Enum para Status ---
class VakinhaStatus(str, enum.Enum):
    open = "open"
    closed = "closed"

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================

class Vakinha(Base):
    __tablename__ = "vakinhas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, default="Vakinha do Lanche")
    created_at = Column(DateTime, default=datetime.now)
    
    # Chave estrangeira para o admin que criou
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_by: Mapped[User] = relationship("User", foreign_keys=[created_by_id])
    
    # Informações de quem busca
    fetcher_name = Column(String, nullable=False)
    fetcher_phone = Column(String, nullable=False)
    
    # Status
    status = Column(Enum(VakinhaStatus), default=VakinhaStatus.open)
    closed_at = Column(DateTime, nullable=True)
    
    # Informações de fechamento
    amount_spent = Column(Float, nullable=True)
    amount_leftover = Column(Float, nullable=True)
    
    # Relacionamento: Uma vakinha tem muitas contribuições
    contributions: Mapped[List["Contribution"]] = relationship("Contribution", back_populates="vakinha")

class Contribution(Base):
    __tablename__ = "contributions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Prova de pagamento (Base64)
    proof_base64 = Column(Text, nullable=True)
    
    # Chave estrangeira para a vakinha
    vakinha_id = Column(Integer, ForeignKey("vakinhas.id"))
    vakinha: Mapped[Vakinha] = relationship("Vakinha", back_populates="contributions")
    
    # Chave estrangeira para o usuário que pagou
    user_id = Column(Integer, ForeignKey("users.id"))
    user: Mapped[User] = relationship("User", back_populates="contributions")

# ==================================
# SCHEMAS (Pydantic)
# ==================================

# --- Contribution Schemas ---

class ContributionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    proof_base64: Optional[str] = None # Base64 da imagem/pdf

class ContributionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    amount: float
    created_at: datetime
    proof_base64: Optional[str] = None
    user: UserPublic # Aninhado: mostra quem pagou

# --- Vakinha Schemas ---

class VakinhaCreate(BaseModel):
    name: Optional[str] = "Vakinha do Lanche"
    fetcher_name: str
    fetcher_phone: str

class VakinhaClose(BaseModel):
    amount_spent: float = Field(..., ge=0)
    amount_leftover: float = Field(..., ge=0)

class VakinhaPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    created_at: datetime
    status: VakinhaStatus
    fetcher_name: str
    fetcher_phone: str
    created_by: UserPublic # Aninhado: mostra quem criou
    
    # Campos de fechamento (opcionais)
    closed_at: Optional[datetime] = None
    amount_spent: Optional[float] = None
    amount_leftover: Optional[float] = None
    
    # Lista de contribuições aninhada
    contributions: List[ContributionPublic] = []