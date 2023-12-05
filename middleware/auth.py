from datetime import datetime, timedelta
from jwt import PyJWTError, decode
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    return create_access_token(
        data, expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer "},
            )

        with open("users.txt", "r") as file:
            users = file.readlines()
            for user_info in users:
                info = user_info.strip().split(", ")
                if email == info[1].split(": ")[1]:
                    return {
                        "name": info[0].split(": ")[1],
                        "email": info[1].split(": ")[1],
                        "password": info[2].split(": ")[1],
                    }

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer "},
        )

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
            headers={"WWW-Authenticate": "Bearer "},
        )


def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
