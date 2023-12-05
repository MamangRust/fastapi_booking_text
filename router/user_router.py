from fastapi import APIRouter, HTTPException
from repository.user_repository import TextUsersRepository
from service.user_service import UsersService
from dto.user import User


users_repository = TextUsersRepository("users.txt")
users_service = UsersService(users_repository)
user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/create")
def create_user(user: User):
    users_service.create_user(user.name, user.email, user.password)
    return {"message": "User created successfully"}


@user_router.get("/")
def get_all_user():
    users = users_service.get_all_users()

    return {"users": users}


@user_router.get("/{email}")
def find_by_email(email: str):
    return users_service.find_by_email(email=email)


@user_router.put("/{user_id}")
def update_user(user_id: int, user: User):
    users_service.update_user(
        user_id=user_id, name=user.name, email=user.email, password=user.password
    )

    return {"message": f"User with ID {user_id} updated successfully"}


@user_router.delete("/users/{user_id}")
def delete_user(user_id: int):
    users_service.delete_user(user_id)
    return {"message": f"User with ID {user_id} deleted successfully"}
