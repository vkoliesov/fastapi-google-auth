import re
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from configs.google import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CONFIGS,
    GOOGLE_SCOPES,
    GOOGLE_AUTH_REDIRECT_PATH
)
from managers.auth import AuthManager
from managers.users import UserManager
from schemas.request.auth import GoogleCallbackIn


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/google/get-auth-url")
async def google_get_auth_url(request: Request):
    flow = Flow.from_client_config(
        client_config=GOOGLE_CONFIGS,
        scopes=GOOGLE_SCOPES
    )
    request_customer = request.headers.get("origin", "https://127.0.0.1:8000")
    callback_url = request_customer + GOOGLE_AUTH_REDIRECT_PATH

    if callback_url.startswith("http:"):
        callback_url = re.sub("^http:", "https:", callback_url)
    flow.redirect_uri = callback_url

    google_auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="select_account"
    )
    return {"google_auth_url": google_auth_url, "state": state}


@router.post("/google/callback")
async def google_callback(request: Request, callback_data: GoogleCallbackIn):
    state = callback_data.dict().get("state")

    flow = Flow.from_client_config(
        client_config=GOOGLE_CONFIGS,
        scopes=GOOGLE_SCOPES,
        state=state
    )
    request_customer = request.headers.get("origin", "https://127.0.0.1:8000")
    callback_url = request_customer + GOOGLE_AUTH_REDIRECT_PATH

    if callback_url.startswith("http:"):
        callback_url = re.sub("^http:", "https:", callback_url)
    flow.redirect_uri = callback_url

    authorization_response = callback_data.dict().get("callback_url")

    try:
        flow.fetch_token(authorization_response=authorization_response)
    except InvalidGrantError as error:
        raise HTTPException(status_code=400, detail=str(error))

    credentials = flow.credentials
    token = credentials.id_token

    idinfo = id_token.verify_oauth2_token(
        token, google_requests.Request(), GOOGLE_CLIENT_ID
    )

    if idinfo["iss"] not in (
        "accounts.google.com",
        "https://accounts.google.com",
    ):
        raise HTTPException(status_code=400, detail="Wrong issuer")

    email = idinfo.get("email")
    first_name = idinfo.get("given_name")
    last_name = idinfo.get("family_name")

    user = await UserManager.get_user_by_email(email)
    if user:
        user_do = await UserManager.get_user_by_id(user.id)
        token = AuthManager.encode_token(user_do)
        return {"token": token}
    id_ = await UserManager.create_user(email, first_name, last_name)
    user_do = await UserManager.get_user_by_id(id_)
    token = AuthManager.encode_token(user_do)
    return {"token": token}
