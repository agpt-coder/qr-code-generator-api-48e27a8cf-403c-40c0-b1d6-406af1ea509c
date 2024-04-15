from enum import Enum

import prisma
import prisma.enums
import prisma.models
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


class SavePreferencesResponse(BaseModel):
    """
    Contains the outcome of saving the user's QR code generation preferences.
    """

    success: bool
    message: str


async def save_preferences(
    userId: str,
    defaultSize: float,
    defaultErrorCorrectionLevel: prisma.enums.ErrorCorrectionLevel,
    defaultOutputFormat: prisma.enums.OutputFormat,
    defaultColor: str,
    defaultBackgroundColor: str,
) -> SavePreferencesResponse:
    """
    Saves user preferences for QR code generation.

    Args:
        userId (str): The unique identifier of the user saving these preferences.
        defaultSize (float): The default size for the QR code specified by the user.
        defaultErrorCorrectionLevel (prisma.enums.ErrorCorrectionLevel): The desired error correction level, affecting the QR code's resilience to errors.
        defaultOutputFormat (prisma.enums.OutputFormat): The preferred output format of the QR code, like SVG or PNG.
        defaultColor (str): The default color preferred by the user for the QR code.
        defaultBackgroundColor (str): The default background color for the QR code, ensuring it contrasts well with the QR code itself.

    Returns:
        SavePreferencesResponse: Contains the outcome of saving the user's QR code generation preferences.
    """
    try:
        await prisma.models.UserPreferences.prisma().update(
            where={"userId": userId},
            data={
                "defaultSize": defaultSize,
                "defaultErrorCorrectionLevel": defaultErrorCorrectionLevel,
                "defaultOutputFormat": defaultOutputFormat,
                "defaultColor": defaultColor,
                "defaultBackgroundColor": defaultBackgroundColor,
            },
        )
        return SavePreferencesResponse(
            success=True, message="User preferences saved successfully."
        )
    except Exception as error:
        return SavePreferencesResponse(
            success=False, message=f"Failed to save preferences: {error}"
        )
