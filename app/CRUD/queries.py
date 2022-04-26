from app.models.basicModels import *
import database
from sqlalchemy import select, insert, delete, update, or_, and_
from hashlib import sha256
from app.parsers.numberParser import parseNumber
from datetime import datetime


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
                Object.id,
                Object.description,
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
                 ).filter(and_(Objects_Barriers.barrier_id == Barrier.id, Objects_Barriers.object_id == Object.id))
    )
    res = await database.database.fetch_all(query)
    if len(res) != 0:
        return res[0]
    else:
        return None


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


async def get_users_actions(user_id):
    query = (
        select(
            [
                UsersActions
            ]
        ).where(UsersActions.user_id == user_id)
    )
    res = await database.database.fetch_all(query)
    return res


async def check_admin():
    users = await get_all_users()
    if len(list(filter(lambda x: x.role == 'admin', users))) == 0:
        res = await insert_user("Admin", "admin", sha256("demo-123".encode('utf-8')).hexdigest())
        return res


async def insert_users_action(user_id, action, image_array):
    try:
        query = (
            insert(UsersActions).values(user_id=user_id, time=datetime.now(), action=action, image=image_array)
        )
        res = await database.database.fetch_all(query)
        return res
    except Exception as e:
        raise Exception("Не удалось добавить запись")


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
        raise Exception("Не удалось обновить запись")


async def delete_user(username):
    try:
        query = (
            delete(User).where(User.login == username)
        )
        res = await database.database.fetch_all(query)
        return res
    except:
        raise Exception("Не удалось удалить запись")
