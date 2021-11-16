import osmnx as ox
from typing import List
from models import LatLng

ox.config(use_cache=True, log_console=True)

def nodes_to_linestring(path, graph):
    coords_list = [
        LatLng(lon=graph.nodes[i]["x"], lat=graph.nodes[i]["y"]) for i in path
    ]
    return coords_list

def shortest_path(orig_lat, orig_lng, dest_lat, dest_lng, graph) -> List[LatLng]:
    orig_node = ox.nearest_nodes(graph, Y=orig_lat, X=orig_lng)
    dest_node = ox.nearest_nodes(graph, Y=dest_lat, X=dest_lng)

    shortest_path = ox.shortest_path(graph, orig_node, dest_node)

    route = nodes_to_linestring(shortest_path, graph)
    return route

def k_shortest_paths(orig_lat, orig_lng, dest_lat, dest_lng, graph, k) -> List[List[LatLng]]:
    orig_node = ox.nearest_nodes(graph, Y=orig_lat, X=orig_lng)
    dest_node = ox.nearest_nodes(graph, Y=dest_lat, X=dest_lng)

    shortest_paths = ox.k_shortest_paths(graph, orig=orig_node, dest=dest_node, k=k)

    paths = [nodes_to_linestring(p, graph) for p in shortest_paths]
    return paths