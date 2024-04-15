from enum import Enum

import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class ErrorCorrectionLevel(Enum):
    """
    Enum detailing the supported error correction levels: L (Low), M (Medium), Q (Quartile), H (High).
    """

    level: str


class OutputFormat(Enum):
    """
    Enum detailing the supported output formats for generated QR codes.
    """

    format: str


class UserPreferencesResponse(BaseModel):
    """
    Provides a detailed view of the user's stored preferences, including size, color, error correction level, and preferred output format.
    """

    defaultSize: float
    defaultErrorCorrectionLevel: ErrorCorrectionLevel
    defaultOutputFormat: OutputFormat
    defaultColor: str = black  # TODO(autogpt): F821 Undefined name `black`
    defaultBackgroundColor: str = white  # TODO(autogpt): F821 Undefined name `white`


async def retrieve_preferences(userId: str) -> UserPreferencesResponse:
    """
    Retrieves saved user preferences.

    Args:
        userId (str): The unique identifier of the user whose preferences are to be retrieved.

    Returns:
        UserPreferencesResponse: Provides a detailed view of the user's stored preferences, including size, color, error correction level, and preferred output format.
    """
    user_preferences = await prisma.models.UserPreferences.prisma().find_unique(
        where={"userId": userId}
    )
    if not user_preferences:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return UserPreferencesResponse(
        defaultSize=user_preferences.defaultSize,
        defaultErrorCorrectionLevel=ErrorCorrectionLevel(
            user_preferences.defaultErrorCorrectionLevel
        ),
        defaultOutputFormat=OutputFormat(user_preferences.defaultOutputFormat),
        defaultColor="black",
        defaultBackgroundColor="white",
    )
