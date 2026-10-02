from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from app.models.schemas import UserCreate, UserLogin
from app.services.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.services.db import (
    create_user,
    get_user_by_email,
    get_user_by_id,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_current_user(request: Request):

    token = request.cookies.get(
        "access_token"
    )

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    user_id = decode_access_token(token)

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session."
        )

    user = get_user_by_id(user_id)

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found."
        )

    return user


@router.post("/register")
def register(user: UserCreate):

    existing_user = get_user_by_email(
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email is already registered."
        )

    password_hash = hash_password(
        user.password
    )

    try:

        user_id = create_user(
            username=user.username,
            email=user.email,
            password_hash=password_hash
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=f"Registration failed: {exc}"
        )

    token = create_access_token(
        user_id
    )

    response = JSONResponse(
        content={
            "message": "Registration successful.",
            "user": {
                "id": user_id,
                "username": user.username,
                "email": user.email
            }
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24
    )

    return response


@router.post("/login")
def login(user: UserLogin):

    existing_user = get_user_by_email(
        user.email
    )

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        user.password,
        existing_user["password_hash"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_access_token(
        existing_user["id"]
    )

    response = JSONResponse(
        content={
            "message": "Login successful.",
            "user": {
                "id": existing_user["id"],
                "username": existing_user["username"],
                "email": existing_user["email"]
            }
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24
    )

    return response


@router.post("/logout")
def logout():

    response = JSONResponse(
        content={
            "message": "Logged out successfully."
        }
    )

    response.delete_cookie(
        "access_token"
    )

    return response


@router.get("/session-info")
def session_info(
    request: Request
):

    token = request.cookies.get(
        "access_token"
    )

    if not token:

        return {
            "authenticated": False
        }

    user_id = decode_access_token(
        token
    )

    if not user_id:

        return {
            "authenticated": False
        }

    user = get_user_by_id(
        user_id
    )

    if not user:

        return {
            "authenticated": False
        }

    return {
        "authenticated": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    }


@router.get("/session-data")
def session_data(
    user=Depends(get_current_user)
):

    return {
        "authenticated": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    }