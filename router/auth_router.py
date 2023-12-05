from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from middleware.auth import (
    create_access_token,
    get_current_user,
    verify_token,
    create_refresh_token,
)
from repository.user_repository import TextUsersRepository
from service.user_service import UsersService
from password.hashing import Hashing
from dto.user import User, RefreshToken


users_repository = TextUsersRepository("users.txt")
users_service = UsersService(users_repository)
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
):
    auth_email = users_service.find_by_email(email=request.username)

    if not auth_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials "
        )

    if not Hashing.verify(auth_email["Password"], request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password"
        )

    access_token = create_access_token(data={"sub": auth_email["Email"]})
    refresh_token = create_refresh_token(data={"sub": auth_email["Email"]})
    response = {
        "name": auth_email["Name"],
        "email": auth_email["Email"],
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    return response


@auth_router.post("/refresh-token")
async def refresh_access_token(
    refresh_token: RefreshToken,
    current_user=Depends(get_current_user),
):
    try:
        user = verify_token(token=refresh_token.refresh_token)

        if user:
            access_token = create_access_token(data={"sub": user["email"]})

            return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid refresh token")


@auth_router.post("/register")
def create_user(
    request: User,
):
    try:
        passwordhash = Hashing.bcrypt(password=request.password)

        user = users_service.create_user(
            name=request.name, email=request.email, password=passwordhash
        )
        return Response(content="Register successfully", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
