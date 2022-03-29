from fastapi import FastAPI
from models import database
from sqlalchemy import select
from fastapi import Request
from fastapi.templating import Jinja2Templates
from models.basicModels import *

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
                barriers_table.c.id,
                barriers_table.c.number,
                barriers_table.c.camera_url,
                barriers_table.c.camdirect_url,
                barriers_table.c.description,
                objects_table.c.name_and_address,
                objects_table.c.is_free_departure_prohibited,
                objects_table.c.is_free_jkh_passage_prohibited,
                objects_table.c.is_free_delivery_passage_prohibited,
                objects_table.c.is_free_collection_passage_prohibited,
                objects_table.c.is_free_garbtrucks_passage_prohibited,
                objects_table.c.is_free_post_passage_prohibited,
                objects_table.c.is_free_taxi_passage_prohibited

            ]
        ).where(barriers_table.c.id == barrier_id and objects_barriers_links_table.c.barrier_id == barriers_table.c.id
                and objects_barriers_links_table.c.object_id == objects_table.c.id)
    )
    res = await database.database.fetch_all(query)
    fetched_barriers = list()
    for row in res:
        fetched_barriers.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                 row[10], row[11], row[12]])
    return fetched_barriers[0]


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("pages/mainpage.html", {"request": request})


# пока по id, потом по номеру
@app.post("/incoming_call/")
async def add_barrier_to_list(barrier_id: int):
    filtred = list(filter(lambda x: x["id"] == barrier_id, barriers))
    if len(filtred) > 0:
        while filtred[0] in barriers:
            barriers.remove(filtred[0])
    else:
        barrier = await get_barrier(barrier_id)
        barier_in_json = {"id": barrier[0], "number": barrier[1], "camera_url": barrier[2], "camdirect_url": barrier[3],
                          "description": barrier[4],
                          "object_name_and_address": barrier[5], "is_free_departure_prohibited": barrier[6],
                          "is_free_jkh_passage_prohibited": barrier[7],
                          "is_free_delivery_passage_prohibited": barrier[8],
                          "is_free_collection_passage_prohibited": barrier[9],
                          "is_free_garbtrucks_passage_prohibited": barrier[10],
                          "is_free_post_passage_prohibited": barrier[11],
                          "is_free_taxi_passage_prohibited": barrier[12]}
        barriers.append(barier_in_json)
    return barier_in_json


@app.get("/incoming_calls")
async def get_current_incoming_calls(request: Request):
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
