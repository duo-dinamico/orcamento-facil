from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from .base_models import Base, User


class Model:
    def __init__(self) -> None:
        engine = create_engine("sqlite:///of.db")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def add_user(self, username: str, password: str = "") -> bool:
        user = User(username=username, password=password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return True

    def read_user_by_name(self, username: str) -> User | None:
        user = self.session.scalars(select(User).where(User.username == username)).first()
        return user
