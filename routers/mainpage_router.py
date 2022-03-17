from fastapi import FastAPI
from models import database
from sqlalchemy import select
from models import basicModels
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{database.DB_USER}:{database.DB_PASSWORD}@{database.DB_HOST}:5432/{database.DB_NAME}"
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


async def get_all_barriers():
    query = (
        select(
            [
                basicModels.barriers_table.c.number,
                basicModels.barriers_table.c.description
            ]
        )
    )
    res = await database.database.fetch_all(query)
    barriers = list()
    for row in res:
        barriers.append([row[0], row[1]])
    return barriers


@app.get("/")
async def read_root(request: Request):
    content = dict()
    content['barriers_list'] = await get_all_barriers()
    return templates.TemplateResponse("pages/mainpage.html", {"request": request, "content": content})


@app.get("/incoming_call/")
async def add_page_to_dashboard(number: str):
    # ???
    app.get("/")
