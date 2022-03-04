from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


#take raw password and it will be hashed first and it will be compared to the hashed pw in the database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)