from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def compareHash(givenpassword:str, matchingPassword: str):
    return pwd_context.verify(givenpassword, matchingPassword) 
