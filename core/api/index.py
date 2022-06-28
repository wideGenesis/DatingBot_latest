from fastapi import (
    APIRouter,
    Request,
    Response,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_201_CREATED

router = APIRouter(
    prefix='',
    tags=['index'],
)

router.mount("/static", StaticFiles(directory="static_assets"), name="static")

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_202_ACCEPTED)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": None})
