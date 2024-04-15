from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Provides feedback on the login process, including authentication status, and, upon success, a session token for subsequent requests.
    """

    status: str
    session_token: str
    error_message: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "YOUR_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def user_login(email: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user and returns a session token.

    Args:
    email (str): User's email address used for account registration.
    password (str): User's password for account access. Will be hashed server-side for comparison.

    Returns:
    UserLoginResponse: Provides feedback on the login process, including authentication status, and, upon success, a session token for subsequent requests.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        return UserLoginResponse(
            status="failed", session_token="", error_message="User not found"
        )
    if not verify_password(password, user.hashedPassword):
        return UserLoginResponse(
            status="failed", session_token="", error_message="Incorrect password"
        )
    token = create_access_token(data={"sub": user.email})
    return UserLoginResponse(status="success", session_token=token)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against its hashed version.

    Args:
    plain_password (str): Plain text password to verify.
    hashed_password (str): Hashed version of the password for comparison.

    Returns:
    bool: True if the password matches its hashed version, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Generates a JWT token based on provided data.

    Args:
    data (dict): Data to encode into the JWT token, typically the user identifier.

    Returns:
    str: A JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
