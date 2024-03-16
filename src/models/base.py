from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    def fill(self, **data) -> "BaseModel":
        for key, value in data.items():
            setattr(self, key, value)
        return self

