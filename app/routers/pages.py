from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="app/templates"
)

router = APIRouter(
    tags=["Pages"]
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.get(
    "/home",
    response_class=HTMLResponse
)
def home_planner(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )


@router.get(
    "/party",
    response_class=HTMLResponse
)
def party_planner(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="party.html"
    )


@router.get(
    "/jewelry",
    response_class=HTMLResponse
)
def jewelry_planner(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="jewelry.html"
    )


@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


@router.get(
    "/history",
    response_class=HTMLResponse
)
def history(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="history.html"
    )