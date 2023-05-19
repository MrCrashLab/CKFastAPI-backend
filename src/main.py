from fastapi import FastAPI
import sys
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import Session
import configparser
import databases

sys.path.append('/Users/buenajen/pet_project/CKFastAPI-backend/src')
from model.api_models import Point, Parking, Map
from model.sql_models import point_table, parking_table, map_table


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

@app.get("/points", response_model=list[Point])
async def get_points() -> list[Point]:
    query = (
        select(
            [
                point_table.c.id,
                point_table.c.longitude,
                point_table.c.latitude
            ]   
        )
        .select_from(point_table)
    )
    return [(Point(id=p.id, longitude=p.longitude, latitude=p.latitude)) for p in await database.fetch_all(query)]

@app.post("/points", response_model=Point)
async def create_point(point: Point):
    parks = await get_points()
    flag = 1
    for p in parks:
        if p.latitude == point.latitude and p.longitude == point.longitude:
            flag = 0
    query = (
        insert(point_table).
        values(longitude=point.longitude, latitude=point.latitude)
    )
    if flag:
        await database.execute(query)
    return point


@app.get("/parkings", response_model=list[Parking])
async def get_parkings() -> list[Parking]:
    query = (
        select(
            [
                parking_table.c.id,
                parking_table.c.id_point,
                parking_table.c.name,
                parking_table.c.description,
                parking_table.c.address,
                parking_table.c.all_slot,
                parking_table.c.free_slot
            ]   
        )
        .select_from(parking_table)
    )
    return [(Parking(id=p.id, id_point=p.id_point, name=p.name, description=p.description, address=p.address, all_slot=p.all_slot, free_slot=p.free_slot)) for p in await database.fetch_all(query)]

@app.get("/parkings/{point_id}", response_model=Parking)
async def get_parking(point_id: int):
    query = (
        select(
            [
                parking_table.c.id,
                parking_table.c.id_point,
                parking_table.c.name,
                parking_table.c.description,
                parking_table.c.address,
                parking_table.c.all_slot,
                parking_table.c.free_slot
            ]   
        )
        .select_from(parking_table.join(point_table))
        .where(point_table.c.id == point_id)
    )
    p = await database.fetch_one(query)
    if p != None:
        return Parking(id=p.id, id_point=p.id_point, name=p.name, description=p.description, address=p.address, all_slot=p.all_slot, free_slot=p.free_slot)
    else:
        return None



@app.post("/parkings", response_model=Parking)
async def create_parking(parking: Parking):
    parks = await get_parkings()
    flag = 1
    for p in parks:
        if p.id_point == parking.id_point:
            flag = 0
    query = (
        insert(parking_table).
        values(id=parking.id, id_point=parking.id_point, name=parking.name, description=parking.description, address=parking.address, all_slot=parking.all_slot, free_slot=parking.free_slot)
    )
    if flag:
        await database.execute(query)
    return parking


@app.get("/map/{parking_id}", response_model=list[Map])
async def get_map(parking_id: int):
    query = (
        select(
            [
                map_table.c.id,
                map_table.c.id_parking,
                map_table.c.floor,
                map_table.c.src
            ]   
        )
        .select_from(map_table.join(parking_table))
        .where(parking_table.c.id == parking_id)
    )
    return [Map(id=p.id, id_parking=p.id_parking, floor=p.floor, src=p.src) for p in await database.fetch_all(query)]

@app.post("/map", response_model=Map)
async def create_parking(map: Map):
    maps = await get_map(map.id_parking)
    flag = 1
    for m in maps:
        if map.id_parking == m.id_parking and map.floor == m.floor:
            flag = 0
    query = (
        insert(map_table).
        values(id=map.id, id_parking=map.id_parking, floor=map.floor, src=map.src)
    )
    if flag:
        await database.execute(query)
    return map