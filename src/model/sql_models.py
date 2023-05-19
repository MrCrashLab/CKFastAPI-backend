from sqlalchemy import Column, String, Integer, MetaData, Table, Float, ForeignKey

metadata = MetaData()

point_table = Table(
    "point",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("longitude", Float),
    Column("latitude", Float)
)

parking_table = Table(
    "parking",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_point", Integer, ForeignKey(point_table.c.id)),
    Column("name", String),
    Column("description", String),
    Column("address", String),
    Column("all_slot", Integer),
    Column("free_slot", Integer)
)

map_table = Table(
    "map",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_parking", Integer, ForeignKey(parking_table.c.id)),
    Column("floor", Integer),
    Column("src", String)
)