from fastapi import FastAPI
import sys
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import Session
import configparser
import databases

sys.path.append('/Users/buenajen/pet_project/CKFastAPI-backend/src')
from model.api_models import Parking
from model.sql_models import parking_table


config = configparser.ConfigParser()
config.read("conf.ini")

DATABASE_URL = (
    f"postgresql://{config['postgres']['username']}:{config['postgres']['password']}@{config['postgres']['host']}:5432/{config['postgres']['dbname']}"
    )
app = FastAPI()
database = databases.Database(DATABASE_URL)
# print(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/parkings", response_model=list[Parking])
async def get_parking_point() -> list[Parking]:
    query = (
        select(
            [
                parking_table.c.id,
                parking_table.c.longitude,
                parking_table.c.latitude
            ]   
        )
        .select_from(parking_table)
    )
    return [(Parking(id=p.id, longitude=p.longitude, latitude=p.latitude)) for p in await database.fetch_all(query)]

@app.post("/parkings", response_model=Parking)
async def create_parking(parking: Parking):
    parks = await get_parking_point()
    flag = 1
    for p in parks:
        if p.latitude == parking.latitude and p.longitude == parking.longitude:
            flag = 0
    query = (
        insert(parking_table).
        values(longitude=parking.longitude, latitude=parking.latitude)
    )
    if flag:
        await database.execute(query)
    return parking
    