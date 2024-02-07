from pydantic import BaseModel


class GoogleGetAuthOut(BaseModel):
    google_auth_url: str
    state: str


class GoogleCallbackOut(BaseModel):
    token: str
