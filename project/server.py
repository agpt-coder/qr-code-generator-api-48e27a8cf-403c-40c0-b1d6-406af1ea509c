import logging
from contextlib import asynccontextmanager

import project.create_qr_code_service
import project.create_user_service
import project.retrieve_preferences_service
import project.save_preferences_service
import project.user_login_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="QR Code Generator API 4",
    lifespan=lifespan,
    description="Given the information gathered from the user, the application's primary functionality centers around generating QR codes based on user-provided data, which encompasses URLs, textual content, or contact information. To cater to the user's preferences and requirements, the application will allow for customization of the QR code's physical attributes, including its size, with a minimum specification of 2 x 2 cm to ensure clarity and ease of scanning, and color, emphasizing a high contrast between the QR code and its background for optimal readability across various devices and scanning conditions, traditionally adopting a black-on-white configuration. Moreover, the user specifies a medium error correction level to balance data density and integrity effectively, making it adaptable across diverse applications while maintaining a satisfactory level of error correction. Lastly, the user has a preference for the QR code's output format to be in SVG, catering to scalability and high-resolution requirements. The tech stack chosen for implementing this functionality includes Python as the programming language, FastAPI for the API framework to handle requests efficiently, PostgreSQL for the database to store user preferences and generated codes, and Prisma as the ORM for seamless database integration and operations.",
)


@app.post(
    "/preferences",
    response_model=project.save_preferences_service.SavePreferencesResponse,
)
async def api_post_save_preferences(
    userId: str,
    defaultSize: float,
    defaultErrorCorrectionLevel: project.save_preferences_service.ErrorCorrectionLevel,
    defaultOutputFormat: project.save_preferences_service.OutputFormat,
    defaultColor: str,
    defaultBackgroundColor: str,
) -> project.save_preferences_service.SavePreferencesResponse | Response:
    """
    Saves user preferences for QR code generation.
    """
    try:
        res = await project.save_preferences_service.save_preferences(
            userId,
            defaultSize,
            defaultErrorCorrectionLevel,
            defaultOutputFormat,
            defaultColor,
            defaultBackgroundColor,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/login", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    email: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Authenticates a user and returns a session token.
    """
    try:
        res = await project.user_login_service.user_login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user", response_model=project.create_user_service.CreateUserResponse)
async def api_post_create_user(
    email: str, password: str
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Registers a new user account.
    """
    try:
        res = await project.create_user_service.create_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/preferences/{userId}",
    response_model=project.retrieve_preferences_service.UserPreferencesResponse,
)
async def api_get_retrieve_preferences(
    userId: str,
) -> project.retrieve_preferences_service.UserPreferencesResponse | Response:
    """
    Retrieves saved user preferences.
    """
    try:
        res = await project.retrieve_preferences_service.retrieve_preferences(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/generate", response_model=project.create_qr_code_service.GenerateQRCodeResponse
)
async def api_post_create_qr_code(
    data: str,
    size: float,
    color: str,
    backgroundColor: str,
    errorCorrectionLevel: str,
    outputFormat: str,
) -> project.create_qr_code_service.GenerateQRCodeResponse | Response:
    """
    Takes user input and customization options to generate a QR code.
    """
    try:
        res = project.create_qr_code_service.create_qr_code(
            data, size, color, backgroundColor, errorCorrectionLevel, outputFormat
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
