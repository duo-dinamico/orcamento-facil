from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# relative path
engine = create_engine("sqlite:///of.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
