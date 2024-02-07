from pydantic import BaseModel


class GoogleCallbackIn(BaseModel):
    callback_url: str
    state: str


class GoogleTokenIn(BaseModel):
    token: str
