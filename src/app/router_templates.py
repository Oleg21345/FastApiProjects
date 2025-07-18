from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from src.database.metod_for_database import MetodSQL
from src.database.engine import SessionDep
from typing import Annotated
from src.schemas.schema.validate_data import RegisterFild
from fastapi import Body
from src.schemas.schema.validate_data import RegisterFild

router = APIRouter(
    tags=["TemplatesCheck"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/items", response_class=HTMLResponse)
async def get_items(session: SessionDep,request: Request):
    users = await MetodSQL.find_user(session)
    number = 0
    context = {"request": request, "users": users, "number": number}
    return templates.TemplateResponse(
        "register_user.html", context
    )

@router.get("/register_user", response_class=HTMLResponse, summary="Форма реєстрації")
async def show_register_form(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})


@router.post("/submit", response_class=HTMLResponse, summary="Реєстрація")
async def register_user(
    request: Request,
    session: SessionDep,
    name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_repeat: str = Form(...)
):

    user = RegisterFild(
        name=name,
        age=age,
        email=email,
        password=password,
        password_repeat=password_repeat
    )

    user_add = await MetodSQL.add_user(session, user)

    context = {
        "request": request,
        "user_add": user_add
    }

    return templates.TemplateResponse("users.html", context)