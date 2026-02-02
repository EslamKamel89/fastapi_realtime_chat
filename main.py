from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from config import settings

load_dotenv()

templates = Jinja2Templates(directory="templates")


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("startup: performing lightweight app checks")
        yield
        print("shutdown: cleaning up")

    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})
