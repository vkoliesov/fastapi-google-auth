from decouple import config


GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_REDIRECT_PATH = "/auth/google/callback"
GOOGLE_CONFIGS = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "project_id": "run4ukraine-a81bc",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uris": [
            "http://localhost:8000/auth/google/callback",
            "https://localhost:8000/auth/google/callback",
        ],
        "javascript_origins": [
            "http://localhost:8000",
            "https://localhost:8000",
        ],
    },
}
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive",
    "openid",
]
