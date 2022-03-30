from models.basicModels import *
from models import database
from sqlalchemy import select, insert, delete, update

# пока по id, потом по номеру
async def get_barrier(barrier_id: int):
    query = (
        select(
            [
                Barrier.id,
                Barrier.number,
                Barrier.camera_url,
                Barrier.camdirect_url,
                Barrier.description,
                Object.name_and_address,
                Object.is_free_departure_prohibited,
                Object.is_free_jkh_passage_prohibited,
                Object.is_free_delivery_passage_prohibited,
                Object.is_free_collection_passage_prohibited,
                Object.is_free_garbtrucks_passage_prohibited,
                Object.is_free_post_passage_prohibited,
                Object.is_free_taxi_passage_prohibited

            ]
        ).where(Barrier.id == barrier_id and Objects_Barriers.barrier_id == Barrier.id
                and Objects_Barriers.object_id == Object.id)
    )
    res = await database.database.fetch_all(query)

    return res[0]


async def get_all_users():
    query = (
        select(
            [
                User
            ]
        )
    )
    res = await database.database.fetch_all(query)
    return res


async def insert_user(username, role, password):
    try:
        query = (
            insert(User).values(login=username, role=role, password_sha256=password)
        )
        res = await database.database.fetch_all(query)
        return res
    except:
        raise Exception("Не удалось добавить запись")


async def update_user(user_id, username, role, password):
    try:
        query = (
            update(User).where(User.id == user_id).values(login=username, role=role, password_sha256=password)
        )
        res = await database.database.fetch_all(query)
        return res
    except:
        raise Exception("Не удалось добавить запись")


async def delete_user(username):
    try:
        query = (
            delete(User).where(User.login == username)
        )
        res = await database.database.fetch_all(query)
        return res
    except:
        raise Exception("Не удалось удалить запись")
