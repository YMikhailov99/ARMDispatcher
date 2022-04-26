import requests
from app.models.basicModels import *
import database
from sqlalchemy import insert


async def insert_object_with_barriers(obj):
    try:
        query = [
            insert(Object).values(id=int(obj[0]),
                                  name_and_address=obj[1]["address"],
                                  number=int(obj[0]),
                                  description=str(obj[1]["description"]),
                                  is_free_departure_prohibited=obj[1]["regulations"]["free_exit"]["value"],
                                  is_free_jkh_passage_prohibited=obj[1]["regulations"]["jkh"]["value"],
                                  is_free_delivery_passage_prohibited=obj[1]["regulations"]["delivery"]["value"],
                                  is_free_collection_passage_prohibited=obj[1]["regulations"]["cash_collection"][
                                      "value"],
                                  is_free_garbtrucks_passage_prohibited=obj[1]["regulations"]["trash"]["value"],
                                  is_free_post_passage_prohibited=obj[1]["regulations"]["post"]["value"],
                                  is_free_taxi_passage_prohibited=obj[1]["regulations"]["taxi"]["value"],
                                  )
        ]
        for bar in obj[1]["barriers"].items():
            query.append(
                insert(Barrier).values(
                    id=str(bar[1]["uid"]),
                    number=int(bar[1]["uid"]),
                    description=str(bar[1]["description"]),
                    gsm_number_vp=bar[1]["uid"],
                    sip_number_vp=bar[1]["uid"],
                    camera_url=str(bar[1]["camera_url"]),
                    camdirect_url=str(bar[1]["camdirect_url"]),
                )
            )
            query.append(
                insert(Objects_Barriers).values(
                    barrier_id=str(bar[1]["uid"]),
                    object_id=int(obj[0])
                )
            )
        res_list = list()
        for q in query:
            await database.database.fetch_all(q)
        return f"obj id {obj[0]} добавлен в БД"
    except Exception as e:
        print(e)
        return f"obj id {obj[0]} error:{str(e)}\n"


async def synchronizeDBs(APIKey):
    try:
        response = requests.post(f'http://client.comendant24.ru/barrier/api/v1/barriers?key={APIKey}')
        r = response.json()
        await database.database.connect()
        res_list = list()
        for obj in r.items():
            res_list.append(await insert_object_with_barriers(obj))
    except Exception as e:
        return str(e)
    finally:
        return res_list

