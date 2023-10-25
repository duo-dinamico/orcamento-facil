from modules.db_models import User

from modules.db_database import SessionLocal


def create_user(db: SessionLocal, user_name: str, user_password: str) -> User:
    db_user = User(username=user_name, password=user_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"create_user will return: {db_user}")
    return db_user
