from typing import List
from dataclasses import dataclass

@dataclass()
class LatLng:
    lat: float
    lon: float

    def __str__(self) -> str:
        return str(self.lat) + "," + str(self.lon)
