import logging
from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

security = HTTPBearer()



SECRET_KEY = "mysecretkey123"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 28



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



fake_users_db = {}



# Pydantic models

class User(BaseModel):

    username: str

    email: EmailStr

    password: str



class LoginUser(BaseModel):

    username: str

    password: str



class Token(BaseModel):

    access_token: str

    token_type: str



# Password hashing and verification

def hash_password(password: str):

    return pwd_context.hash(password)



def verify_password(plain: str, hashed: str):

    return pwd_context.verify(plain, hashed)



# JWT token creation and decoding

def create_token(data: dict):

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data.update({"exp": expire})

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)



def decode_token(token: str):

    try:

        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:

        raise HTTPException(status_code=401, detail="Invalid token")



# Dependency

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    payload = decode_token(credentials.credentials)

    username = payload.get("sub")

    role = payload.get("role", "user")

    if not username:

        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = fake_users_db.get(username)

    if not user:

        raise HTTPException(status_code=401, detail="User not found")

    return {"username": username, "role": role}



# Routes

@app.get("/")

def read_root():

    return {"message": "Welcome to SecureBankAPI"}



@app.post("/register")

def register(user: User):

    if user.username in fake_users_db:

        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    fake_users_db[user.username] = {

        "username": user.username,

        "email": user.email,

        "hashed_password": hashed_password,

        "role": "user"

    }

    return {"message": f"User {user.username} registered successfully"}



@app.post("/login", response_model=Token)

@limiter.limit("4/minute")

def login(request: Request, username: str = Form(...), password: str = Form(...)):

    user = fake_users_db.get(username)

    if not user or not verify_password(password, user["hashed_password"]):

        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {

        "sub": username,

        "role": user.get("role", "user")

    }

    token = create_token(payload)

    return {"access_token": token, "token_type": "bearer"}



@app.get("/secure")

def secure_route(current_user: dict = Depends(get_current_user)):

    return {"message": f"Welcome, {current_user['username']}. You are authorized!"}



@app.get("/admin", include_in_schema=False)

@limiter.limit("3/minute")

def admin_route(request: Request, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":

        raise HTTPException(status_code=403, detail="Access denied")

    return {"message": f"Welcome Admin {current_user['username']}, You are authorized!"}


@app.exception_handler(RateLimitExceeded)
async def rate_Limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Limit exceeded, Please try again later."}
    )
