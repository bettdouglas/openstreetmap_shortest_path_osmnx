from typing import List
from fastapi import FastAPI, Response
from geojson_pydantic.features import Feature, FeatureCollection
import osmnx as ox
from shapely.geometry import box, Point
import find_route_functions
from typing import List
from models import LatLng

capetown_G = ox.graph_from_address(
    "Cape Town, South Africa", dist=5000, network_type="drive"
)

nodes, edges = ox.graph_to_gdfs(capetown_G)

minx, miny, maxx, maxy = nodes.total_bounds

graph_bounds = box(minx, miny, maxx, maxy)

print(f"Using bounds {graph_bounds}")


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/graph_bounds")
def read_graph():
    return Feature(**graph_bounds.__geo_interface__)


@app.get("/shortest_route")
def read_shortest_route(
    origin_lat: float,
    origin_lng: float,
    destination_lat: float,
    destination_lng: float,
):
    if not (
        graph_bounds.contains(Point(origin_lng, origin_lat))
        and graph_bounds.contains(Point(destination_lng, destination_lat))
    ):
        return Response(
            status_code=400, content="Origin or destination outside of Cape Town"
        )

    shortest_path = find_route_functions.shortest_path(
        orig_lat=origin_lat,
        orig_lng=origin_lng,
        dest_lat=destination_lat,
        dest_lng=destination_lng,
        graph=capetown_G,
    )
    return linestring_to_feature(shortest_path)


@app.post("/k_shortest_paths")
def read_k_shortest_paths(
    origin_lat: float,
    origin_lng: float,
    destination_lat: float,
    destination_lng: float,
    k: int,
):
    if not (
        graph_bounds.contains(Point(origin_lng, origin_lat))
        and graph_bounds.contains(Point(destination_lng, destination_lat))
    ):
        return Response(
            status_code=400, content="Origin or destination outside of Cape Town"
        )
        
    k_shortest_paths = find_route_functions.k_shortest_paths(
        orig_lat=origin_lat,
        orig_lng=origin_lng,
        dest_lat=destination_lat,
        dest_lng=destination_lng,
        graph=capetown_G,
        k=k,
    )
    return linestrings_to_feature_collection(k_shortest_paths)


def linestring_to_feature(linestring: List[LatLng]) -> Feature:
    coordinates = [[c.lon, c.lat] for c in linestring]
    linestring_feature = {
        "type": "Feature",
        "properties": {},
        "id": f"{str(linestring[0])} {str(linestring[-1])}",
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates,
        },
    }
    return Feature(**linestring_feature)


def linestrings_to_feature_collection(
    linestrings: List[List[LatLng]],
) -> FeatureCollection:
    features = [linestring_to_feature(linestring) for linestring in linestrings]
    return FeatureCollection(features=features)
