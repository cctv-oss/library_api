from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://输入你的MySQL账号:你的MySQL密码@localhost:3306/library"

engine = create_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()