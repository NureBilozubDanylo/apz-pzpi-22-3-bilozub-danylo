from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.models.user_in_shop import UserInShop
from app.models.employee import Employee

SECRET_KEY = "zooshop"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        role=user.role,
        email=user.email,
        mobile_number=user.mobile_number,
        age=user.age,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_employee = Employee(user_id=db_user.user_id, position="Cashier", salary_without_percent=500,shop_id = None)
    db.add(db_employee)
    db.commit()

    return db_user

def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_users_by_shop_id(db: Session, shop_id: int):
    return db.query(User).join(UserInShop).filter(UserInShop.shop_id == shop_id).all()
