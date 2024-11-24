from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")# for hashing password, memorize
def hash (password: str) -> str:
    return pwd_context.hash(password)

#verify the password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)