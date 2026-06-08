from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
DATABASE_URL = "sqlite:///./ayastra.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


#create_engine : connects pyhton to your sqllite database file
#brasssense.db : teh actual database file that will appear in your folder
#sessionlocal : a factory that creates database sessions (like openning a connection)
#base: all ypur tables will inherit from this
#check _same_thread:false  : sqllite specific --allows fastapi to use it properly
