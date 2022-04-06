from app.models.basicModels import *
import database
from sqlalchemy import select, insert, delete, update, or_
from hashlib import sha256
from app.parsers.numberParser import parseNumber


async def get_barrier(barrier_number: str):
    barrier_number = parseNumber(barrier_number)
    query = (
        select(
            [
                Barrier.id,
                Barrier.number,
                Barrier.camera_url,
                Barrier.camdirect_url,
                Barrier.description,
                Object.name_and_address,
                Barrier.gsm_number_vp,
                Barrier.sip_number_vp,
                Object.is_free_departure_prohibited,
                Object.is_free_jkh_passage_prohibited,
                Object.is_free_delivery_passage_prohibited,
                Object.is_free_collection_passage_prohibited,
                Object.is_free_garbtrucks_passage_prohibited,
                Object.is_free_post_passage_prohibited,
                Object.is_free_taxi_passage_prohibited

            ]
        ).filter(or_(Barrier.gsm_number_vp == barrier_number,
                     Barrier.sip_number_vp == barrier_number)
                 )
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


async def check_admin():
    users = await get_all_users()
    if len(list(filter(lambda x: x.role == 'admin', users))) == 0:
        res = await insert_user("Admin", "admin", sha256("demo-123".encode('utf-8')).hexdigest())
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
