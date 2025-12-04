from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from database import Base
from roles.role_model import RolePublic

if TYPE_CHECKING:
    from vakinha.vakinha_model import Contribution

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, index=True, nullable=True)
    profile_image_url = Column(String, nullable=True)
    profile_image_base64 = Column(String, nullable=True)
    
    # Chave estrangeira que aponta para a tabela 'roles'
    role_id = Column(Integer, ForeignKey("roles.id"))
    # Cria a relação para que possamos acessar o objeto Role a partir de um User
    role = relationship("Role")

    # --- NOVA RELAÇÃO (Essencial para a Vakinha) ---
    # Um usuário pode ter muitas contribuições
    contributions: Mapped[List["Contribution"]] = relationship("Contribution", back_populates="user")
    # --- FIM DA NOVA RELAÇÃO ---

    # NOTA: O método @validates foi removido propositalmente para permitir
    # URLs externas (como Pinterest) sem tentar fazer download e causar erro.

# ==================================
# SCHEMAS (Pydantic)
# ==================================
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = Field(default=None, min_length=3)
    profile_image_url: str | None = None
    profile_image_base64 : Optional[str] = None
    role_id: int = Field(description="ID do role a ser associado ao usuário")

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3)
    profile_image_url: str | None = None
    profile_image_base64 : Optional[str] = None

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None = None
    profile_image_url: str | None = None
    profile_image_base64 : Optional[str] = None
    role: RolePublic # O perfil agora é um objeto aninhado