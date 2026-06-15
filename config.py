import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "panifica_pro_360_secret")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///panifica_pro_360.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False