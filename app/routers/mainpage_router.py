from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from app import env
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Request, Depends, status, Form
from fastapi_login.exceptions import InvalidCredentialsException
from app.CRUD.queries import *
from app.parsers.numberParser import *
import database
import requests
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.CRUD.dbsynchronization import synchronizeDBs
import cv2
import base64
import asyncio

templates = Jinja2Templates(directory="app/templates")


async def to_login(request, exc):
    return templates.TemplateResponse("pages/login.html", {"request": request, })


exceptions = {
    404: to_login,
    401: to_login,
}

app = FastAPI(exception_handlers=exceptions)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
manager = LoginManager(env.secret, token_url='/auth/token', use_cookie=True, default_expiry=timedelta(hours=12))
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
    await check_admin()


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


def wrap_frame(frame):
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def get_camera(src):
    return cv2.VideoCapture(src)


def read_camera(camera):
    return camera.read()


async def gen_frames(src):
    try:
        if src not in ("False", None, "", False):
            yield wrap_frame(env.loadingFrame)
            camera = get_camera(src)
            try:
                successCount = 0
                totalCount = 0
                while True:
                    await asyncio.sleep(1)
                    totalCount += 1
                    success, frame = camera.read()
                    if not success:
                        if successCount == 0:
                            yield wrap_frame(env.loadingFrame)
                        camera = await asyncio.get_event_loop().run_in_executor(None, get_camera, src)
                        if totalCount > 20 and successCount == 0:
                            yield wrap_frame(env.erroFrame)
                            break
                        else:
                            continue
                    else:
                        successCount += 1
                        ret, buffer = cv2.imencode('.jpg', frame)
                        frame = buffer.tobytes()
                        yield wrap_frame(frame)

            except cv2.error:
                yield wrap_frame(env.erroFrame)
            except Exception as e:
                yield wrap_frame(env.erroFrame)
        else:
            yield wrap_frame(env.noImageFrame)
    except cv2.error:
        yield wrap_frame(env.erroFrame)
    except Exception as e:
        yield wrap_frame(env.erroFrame)


def get_stream(src):
    return StreamingResponse(gen_frames(src), media_type='multipart/x-mixed-replace; boundary=frame')


@app.get("/video_feed", response_class=HTMLResponse, summary="Dashboard")
async def get_translation(src: str):
    try:
        # gen = gen_frames(src)
        return await asyncio.get_event_loop().run_in_executor(None, get_stream, src)
    except Exception as e:
        return e.args


@app.get("/dashboard", response_class=HTMLResponse, summary="Dashboard")
async def get_dashboard(request: Request, user=Depends(manager)):
    if user:
        content = dict()
        content["user"] = user

        return templates.TemplateResponse("pages/mainpage.html", {"request": request, "content": content})
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.post("/static_data_from_aster/")
async def get_static_data(data, APIKey: str):
    if APIKey == env.APIKeyAster:
        return data
    else:
        return HTMLResponse(status_code=status.HTTP_401_UNAUTHORIZED)


# добавляет только новые записи, старые не обновляет
@app.post("/synchronize_db_with_aster/")
async def get_static_data(APIKey: str):
    return await synchronizeDBs(APIKey)


@app.post("/incoming_call/")
async def add_barrier_to_list(barrier_number: str):
    filtred = list(filter(lambda x: parseNumber(x.gsm_number_vp) == parseNumber(barrier_number) or parseNumber(
        x.sip_number_vp) == parseNumber(barrier_number), barriers))
    if len(filtred) > 0:
        while filtred[0] in barriers:
            barriers.remove(filtred[0])
        return "Call removed"
    else:
        barrier = await get_barrier(barrier_number)
        if barrier is not None:
            barriers.append(barrier)
        return barrier


@app.get("/incoming_calls")
async def get_current_incoming_calls(request: Request, user=Depends(manager)):
    return barriers


@app.get("/open_barrier_by_core")
async def open_barrier_by_core(button_name, barrier_number, user=Depends(manager)):
    # заменить тестовый uid на barrier_number
    response = requests.post(
        f'http://client.comendant24.ru/barrier/api/v1/open?key=aiko9ooChoogeique3ph&uid={barrier_number}&open_reason={button_name}')
    if response:
        await add_barrier_to_list(barrier_number)
    bar = await get_barrier(barrier_number)
    img_url = bar["camera_url"]
    img = await asyncio.get_event_loop().run_in_executor(None, get_screen, img_url)
    base64_byte_array = base64.b64encode(img)
    await insert_users_action(user_id=user.id,
                              action=f"send open_barrier_by_core request, barrier uid: {barrier_number}, "
                                     f"reason: {button_name}, response status code: {response.status_code}",
                              image_array=base64_byte_array)
    if response:
        return True
    else:
        return False


@app.get("/open_manually")
async def open_manually(button_name, barrier_number):
    return True


def get_screen(src):
    try:
        resp = requests.get(src, timeout=10)
        img = resp.content
    except requests.exceptions.RequestException as e:
        img = env.erroFrame
    return img


@app.get("/close_manually")
async def close_manually(button_name, barrier_number, user=Depends(manager)):
    await add_barrier_to_list(barrier_number)
    bar = await get_barrier(barrier_number)
    img_url = bar["camera_url"]
    img = await asyncio.get_event_loop().run_in_executor(None, get_screen, img_url)
    base64_byte_array = base64.b64encode(img)
    await insert_users_action(user_id=user.id,
                              action=f"close card, barrier uid: {barrier_number}",
                              image_array=base64_byte_array)
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
    user = await load_user(username)
    if not user:
        raise InvalidCredentialsException
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


@app.get("/logs", response_class=HTMLResponse, summary="Users page", tags=['Users'])
async def get_users(request: Request, user=Depends(manager)):
    if user:
        content = dict()
        content["actions"] = await get_users_actions(user.id)
        content["user"] = user
        return templates.TemplateResponse("pages/logpage.html", {"request": request, "content": content})
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
