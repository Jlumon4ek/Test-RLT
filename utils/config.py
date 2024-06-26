import os
from dotenv import load_dotenv

load_dotenv("files/envs/.env")

TOKEN = os.getenv("TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")
