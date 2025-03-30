# map.py
import osmnx as ox
import networkx as nx
from name_fetcher import get_lat_lon

def compute_route(source_name, destination_name):
    # Convert place names to coordinates
    source_coords = get_lat_lon(source_name)
    destination_coords = get_lat_lon(destination_name)

    if "error" in source_coords or "error" in destination_coords:
        return {"error": "Invalid location names provided."}

    # Define the center point for the network graph
    center_lat = (source_coords["latitude"] + destination_coords["latitude"]) / 2
    center_lon = (source_coords["longitude"] + destination_coords["longitude"]) / 2

    # Download the road network
    G = ox.graph_from_point((center_lat, center_lon), dist=2000, network_type="drive")

    # Find the nearest nodes to the provided coordinates
    source_node = ox.distance.nearest_nodes(G, source_coords["longitude"], source_coords["latitude"])
    destination_node = ox.distance.nearest_nodes(G, destination_coords["longitude"], destination_coords["latitude"])

    # Compute the shortest path
    try:
        shortest_path = nx.shortest_path(G, source=source_node, target=destination_node, weight="length")
    except nx.NetworkXNoPath:
        return {"error": "No path found between the specified locations."}
    except nx.NodeNotFound:
        return {"error": "One of the nodes was not found in the graph."}

    # Convert the node IDs to latitude/longitude coordinates for easier consumption
    route_coords = [[G.nodes[node]['y'], G.nodes[node]['x']] for node in shortest_path]
    return {"shortest_path": route_coords}
