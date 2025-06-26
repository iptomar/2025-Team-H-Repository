from sqlalchemy.orm import DeclarativeBase  

class Class:
    def __init__(self, name: str):
        self.name = name

class Base(DeclarativeBase):
    pass
