from sqlalchemy import Column, String
from app.database import Base
from pydantic import BaseModel, EmailStr


class User(Base):
    __tablename__ = "users"

    email = Column(String(255), primary_key=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    comissao = Column(String(50), nullable=True) #A debater se fica assim ou se é criada uma tabela

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    #Se for mantido este atributo é necessário alterar os UIs também
    comissao: Optional[str] = Field(
        None,
        max_length=50,
        description="Nome da comissão/zona universitária (ex: 'Tomar')",
        example="Tomar")

class UserInDB(BaseModel):
    email: EmailStr
    comissao: Optional[str] = None  # Opcional na resposta também

    class Config:
        orm_mode = True
