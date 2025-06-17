from sqlmodel import create_engine

DATABASE_URL = "sqlite:///hr_database.db"
engine = create_engine(DATABASE_URL, echo=True)