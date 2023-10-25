from sqlalchemy import select

from modules.db_models import User

from modules.db_database import SessionLocal


def create_user(db: SessionLocal, user_name: str, user_password: str) -> User:
    exist = db.scalars(select(User).where(User.username == user_name)).first()
    print(exist)
    if exist:
        print("User already exist.")
        return False

    db_user = User(username=user_name, password=user_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"create_user will return: {db_user}")
    return True


def read_user(db: SessionLocal, user_name: str, user_password: str) -> User:
    return db.scalars(
        select(User).where(User.username == user_name, User.password == user_password)
    ).first()
