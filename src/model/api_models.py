from pydantic import BaseModel


class Point(BaseModel):
    id: int
    longitude: float
    latitude: float

class Parking(BaseModel):
    id: int
    id_point: int
    name: str
    description: str
    address: str
    all_slot: int
    free_slot: int

class Map(BaseModel):
    id: int
    id_parking: int
    floor: int
    src: str
