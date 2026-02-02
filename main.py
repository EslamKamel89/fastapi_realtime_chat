from dotenv import load_dotenv
from fastapi import FastAPI

from config import settings

load_dotenv()

app = FastAPI(title=settings.APP_NAME)


@app.get("/health")
async def health():
    return {"status": "ok"}
