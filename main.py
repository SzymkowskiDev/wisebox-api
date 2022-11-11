from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from schemas import UserIn, UserOut, UserInDB, Token, TokenData, Magazine
from database import engine

SECRET_KEY = 'KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def taken_email(user_in: UserIn):
    with engine.connect() as conn:
        emails = conn.execute('SELECT EMAIL FROM USERS').fetchall()
    if emails:
        emails = [x[0] for x in emails]
    if user_in.email in emails:
        return True


def get_password_hash(user_in: UserIn):
    return pwd_context.hash(user_in.password)


def get_user(email: str):
    with engine.connect() as conn:
        user = conn.execute('SELECT * FROM USERS WHERE EMAIL=?', (email,)).fetchall()
    if user:
        user = user[0]
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


@app.post('/register/', status_code=201)
async def register(user_in: UserIn):
    if taken_email(user_in):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email address is already used, please choose another one!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = get_password_hash(user_in)
    with engine.connect() as conn:
        conn.execute(f'INSERT INTO USERS(FIRST_NAME, LAST_NAME, EMAIL, HASH_PASSWORD) VALUES (?, ?, ?, ?)',
                     (user_in.first_name, user_in.last_name, user_in.email, hashed_password))
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
    with engine.connect() as conn:
        magazines = conn.execute('SELECT * FROM MAGAZINES WHERE USER_ID=?', (current_user.id,)).fetchall()
    list_of_magazines = []
    for magazine in magazines:
        list_of_magazines.append(Magazine(id=magazine[1], name=magazine[2], description=magazine[3], avatar=magazine[4],
                                          location=magazine[5], date_of_creation=magazine[6]))
    return list_of_magazines
