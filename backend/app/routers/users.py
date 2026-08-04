from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate
from app.auth.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

users = []


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):

    for existing_user in users:
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=400,
                detail="Username already exists."
            )

        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered."
            )

    user_data = user.model_dump()

    user_data["password"] = hash_password(user.password)

    users.append(user_data)

    return {
        "message": "User registered successfully"
    }


@router.get("/")
def get_users():
    return users