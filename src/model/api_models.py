from pydantic import BaseModel


class Parking(BaseModel):
    id: int
    longitude: float
    latitude: float

    # def __init__(self, longitude:float, latitude:float):
    #     self.longitude = longitude
    #     self.latitude = latitude
