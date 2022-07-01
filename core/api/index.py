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

index = APIRouter(
    prefix="",
    tags=["index"],
)

templates = Jinja2Templates(directory="templates")
#
# index.mount("/static", StaticFiles(directory="static"), name="static")


@index.get("/", response_class=HTMLResponse, status_code=status.HTTP_202_ACCEPTED)
async def home(request: Request):
    data = {"page": "Home page"}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})
