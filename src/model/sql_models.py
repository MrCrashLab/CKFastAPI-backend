from sqlalchemy import Column, String, Integer, MetaData, Table, Float

metadata = MetaData()

parking_table = Table(
    "parking",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("longitude", Float),
    Column("latitude", Float)
)
