from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from schemas import UserIn, UserOut, UserInDB, Token, TokenData, Magazine
import sqlite3

SECRET_KEY = 'KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.include_router(crud.magazine)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(user_in: UserIn):
    return pwd_context.hash(user_in.password)


def get_user(email: str):
    # Database connection
    conn = sqlite3.connect('wisebox_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM USERS WHERE EMAIL=?', (email,))
    user = c.fetchall()
    if user:
        user = user[0]
    conn.close()

    if user:
        return UserInDB(id=user[0], first_name=user[1], last_name=user[2], email=user[3], hashed_password=user[4])


def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


@app.post('/register/')
async def register(user_in: UserIn):
    hashed_password = get_password_hash(user_in)

    # Database connection
    conn = sqlite3.connect('wisebox_database.db')
    c = conn.cursor()
    to_db = f'"{user_in.id}", "{user_in.first_name}", "{user_in.last_name}", "{user_in.email}", "{hashed_password}"'
    c.execute(f'INSERT INTO USERS VALUES ({to_db});')
    conn.commit()
    conn.close()

    return 'Account created!'


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: UserOut = Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.first_name}]


@app.get("/magazines/")
async def show_my_magazines(current_user: UserOut = Depends(get_current_user)):
    # Database connection
    conn = sqlite3.connect('wisebox_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM MAGAZINES WHERE USER_ID=?', (current_user.id,))
    magazines = c.fetchall()
    conn.commit()
    conn.close()

    list_of_magazines = []
    for magazine in magazines:
        list_of_magazines.append(Magazine(id=magazine[1], name=magazine[2], description=magazine[3], avatar=magazine[4],
                                          location=magazine[5], date_of_creation=magazine[6]))
    return list_of_magazines
