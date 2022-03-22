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
barriers = list()


@app.on_event("startup")
async def startup():
    await database.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


# пока по id, потом по номеру
async def get_barrier(barrier_id: int):
    query = (
        select(
            [
                basicModels.barriers_table.c.id,
                basicModels.barriers_table.c.number,
                basicModels.barriers_table.c.description
            ]
        ).where(basicModels.barriers_table.c.id == barrier_id)
    )
    res = await database.database.fetch_all(query)
    fetched_barriers = list()
    for row in res:
        fetched_barriers.append([row[0], row[1], row[2]])
    return fetched_barriers[0]


async def get_all_barriers():
    query = (
        select(
            [
                basicModels.barriers_table.c.id,
                basicModels.barriers_table.c.number,
                basicModels.barriers_table.c.description
            ]
        )
    )
    res = await database.database.fetch_all(query)
    fetched_barriers = list()
    for row in res:
        fetched_barriers.append([row[0], row[1], row[2]])
    return fetched_barriers


@app.get("/")
async def read_root(request: Request):
    content = dict()
    content['barriers_list'] = await get_all_barriers()
    return templates.TemplateResponse("pages/mainpage.html", {"request": request, "content": content})


@app.get("/main")
async def add_page_to_dashboard(request: Request):
    content = dict()
    content['barriers_list'] = await get_all_barriers()
    return templates.TemplateResponse("pages/dynamic_data.html", {"request": request, "content": content})


# пока по id, потом по номеру
@app.post("/incoming_call/")
async def add_barrier_to_list(barrier_id: int):
    filtred = list(filter(lambda x: x["id"] == barrier_id, barriers))
    if len(filtred) > 0:
        while filtred[0] in barriers:
            barriers.remove(filtred[0])
    else:
        barrier = await get_barrier(barrier_id)
        barriers.append({"id": barrier[0], "number": barrier[1], "description": barrier[2]})
    return {"id": barrier[0], "number": barrier[1], "description": barrier[2]}


@app.get("/incoming_calls")
async def get_current_incoming_calls(request: Request):
    return barriers
