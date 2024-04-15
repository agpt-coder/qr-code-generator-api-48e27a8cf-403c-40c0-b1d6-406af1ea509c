from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Provides feedback on the outcome of the user account creation attempt.
    """

    success: bool
    message: str
    user_id: Optional[str] = None


async def create_user(email: str, password: str) -> CreateUserResponse:
    """
    Registers a new user account.

    This function hashes the user's password for secure storage, validates the email uniqueness,
    and creates a new user entry in the database.

    Args:
        email (str): The email address for the user account, which must be unique.
        password (str): The user's password, which will be hashed before storage for security.

    Returns:
        CreateUserResponse: Provides feedback on the outcome of the user account creation attempt,
                            including success status, message, and optionally the user ID.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    try:
        user = await prisma.models.User.prisma().create(
            {"email": email, "hashedPassword": hashed_password}
        )
        return CreateUserResponse(
            success=True, message="User created successfully.", user_id=user.id
        )
    except Exception as e:
        if "Unique constraint failed on the fields: (`email`)" in str(e):
            return CreateUserResponse(success=False, message="Email already exists.")
        else:
            return CreateUserResponse(
                success=False, message=f"An unexpected error occurred: {str(e)}"
            )
