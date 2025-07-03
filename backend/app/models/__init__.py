from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Class:
    def __init__(self, name: str):
        self.name = name
