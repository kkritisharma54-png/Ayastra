from passlib.context import CryptContext
from database import SessionLocal
from models import User

db = SessionLocal()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
user = db.query(User).first()
user.password_hash = pwd.hash("ayastra123")
db.commit()
print("Password updated for", user.email)