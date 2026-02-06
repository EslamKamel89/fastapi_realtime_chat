from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from core.config import settings
from core.database import Database
from core.deps import get_session

templates = Jinja2Templates(directory="templates")


def create_app() -> FastAPI:
    database_url = settings.DATABASE_URL
    if not database_url:
        raise RuntimeError("Database url is not loaded from the environment variables")
    database = Database(database_url=database_url, echo=True)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("startup: performing lightweight app checks")
        yield
        print("shutdown: cleaning up")
        await database.dispose()

    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.dependency_overrides[get_session] = database.get_session

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})
