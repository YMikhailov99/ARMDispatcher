from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from env import secret
from fastapi.responses import HTMLResponse, RedirectResponse, ORJSONResponse
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Request, Depends, status, Form
from hashlib import sha256
from fastapi_login.exceptions import InvalidCredentialsException
from CRUD.queries import *

templates = Jinja2Templates(directory="templates")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{database.DB_USER}:{database.DB_PASSWORD}@{database.DB_HOST}:5432/{database.DB_NAME}"
)


async def to_login(request, exc):
    return templates.TemplateResponse("pages/login.html", {"request": request, })


exceptions = {
    404: to_login,
    401: to_login,
}

app = FastAPI(exception_handlers=exceptions)
manager = LoginManager(secret, token_url='/auth/token', use_cookie=True, default_expiry=timedelta(hours=12))
manager.cookie_name = 'ARMDispatcher'
barriers = list()


@manager.user_loader()
async def load_user(username: str):
    query = (
        select(
            User
        ).where(User.login == username)
    )
    user = await database.database.fetch_one(query)
    return user


@app.on_event("startup")
async def startup():
    await database.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


@app.get("/dashboard", response_class=HTMLResponse, summary="Dashboard")
async def get_dashboard(request: Request, user=Depends(manager)):
    if user:
        content = dict()
        content["user"] = user

        return templates.TemplateResponse("pages/mainpage.html", {"request": request, "content": content})
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


# пока по id, потом по номеру
@app.post("/incoming_call/")
async def add_barrier_to_list(barrier_id: int):
    filtred = list(filter(lambda x: x["id"] == barrier_id, barriers))
    if len(filtred) > 0:
        while filtred[0] in barriers:
            barriers.remove(filtred[0])
    else:
        barrier = await get_barrier(barrier_id)
        barriers.append(barrier)
    return barrier


@app.get("/incoming_calls")
async def get_current_incoming_calls(request: Request, user=Depends(manager)):
    return barriers


@app.get("/open_barrier_by_core")
async def open_barrier_by_core(button_name, barrier_id):
    return await send_request_to_core(None)


async def send_request_to_core(request):
    response = False
    return response


@app.get("/open_manually")
async def open_manually(button_name, barrier_id):
    return True


@app.get("/close_manually")
async def close_manually(button_name, barrier_id):
    await add_barrier_to_list(int(barrier_id))
    return True


@app.post('/auth/login', tags=['Users'])
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = sha256(data.password.encode('utf-8')).hexdigest()
    user = await load_user(username)
    if not user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    elif password != user.password_sha256:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    resp = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.post('/auth/token', tags=['Users'])
async def token(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = sha256(data.password.encode('utf-8')).hexdigest()
    user = await load_user(username)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user.password_sha256:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    return access_token


@app.get("/", response_class=HTMLResponse, summary="Login page")
async def login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request, })


@app.get("/users", response_class=HTMLResponse, summary="Users page", tags=['Users'])
async def get_users(request: Request, user=Depends(manager)):
    if user.role == "admin":
        content = dict()
        content["users"] = await get_all_users()
        content["user"] = user
        return templates.TemplateResponse("pages/userspage.html", {"request": request, "content": content})
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.post('/add_user', tags=['Users'])
async def add_user(username: str = Form(...), role: str = Form(...), password: str = Form(...), user=Depends(manager)):
    if user:
        try:
            await insert_user(username, role, sha256(password.encode('utf-8')).hexdigest())
            return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
        except Exception:
            return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.post('/edit_user', tags=['Users'])
async def edit_user(user_id: int = Form(...), user_login: str = Form(...), user_role: str = Form(...),
                    user_password: str = Form(...), user=Depends(manager)):
    if user:
        try:
            if len(user_password) < 5:
                return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
            else:
                await update_user(user_id, user_login, user_role, sha256(user_password.encode('utf-8')).hexdigest())
                return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
        except Exception:
            return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.post('/remove_user', tags=['Users'])
async def add_user(user_login: str = Form(...), user=Depends(manager)):
    if user:
        try:
            await delete_user(user_login)
            return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
        except Exception:
            return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
