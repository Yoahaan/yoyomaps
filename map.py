import osmnx as ox
import networkx as nx
from name_fetcher import get_lat_lon
from networkx.algorithms.simple_paths import shortest_simple_paths


def compute_route(source_name, destination_name, k=3):
    print(f"[DEBUG] Fetching coordinates for '{source_name}' and '{destination_name}'...")
    source_coords = get_lat_lon(source_name)
    destination_coords = get_lat_lon(destination_name)

    if "error" in source_coords or "error" in destination_coords:
        print("[ERROR] Invalid location names provided.")
        return {"error": "Invalid location names provided."}

    center_lat = (source_coords["latitude"] + destination_coords["latitude"]) / 2
    center_lon = (source_coords["longitude"] + destination_coords["longitude"]) / 2
    print(f"[DEBUG] Center point: ({center_lat}, {center_lon})")

    # Load road network
    print("[DEBUG] Downloading road network from OSM...")
    G_multi = ox.graph_from_point((center_lat, center_lon), dist=1000, network_type="drive")

    try:
        source_node = ox.distance.nearest_nodes(G_multi, source_coords["longitude"], source_coords["latitude"])
        destination_node = ox.distance.nearest_nodes(G_multi, destination_coords["longitude"], destination_coords["latitude"])
        print(f"[DEBUG] Source node: {source_node}, Destination node: {destination_node}")
    except Exception as e:
        print(f"[ERROR] Nearest node lookup failed: {e}")
        return {"error": "One of the locations is not on the road network."}

    # Convert to DiGraph for shortest path calculations
    G = nx.DiGraph()
    for u, v, data in G_multi.edges(data=True):
        weight = data.get('length', 1)
        if G.has_edge(u, v):
            if G[u][v]['weight'] > weight:
                G[u][v]['weight'] = weight
        else:
            G.add_edge(u, v, weight=weight)

    # Compute up to k shortest paths using generator
    try:
        print(f"[DEBUG] Computing up to {k} shortest paths using generator...")
        path_gen = shortest_simple_paths(G, source_node, destination_node, weight='weight')
        k_paths = []
        for i, path in enumerate(path_gen):
            print(f"[DEBUG] Path {i + 1} received.")
            k_paths.append(path)
            if i + 1 >= k:
                break
    except nx.NetworkXNoPath:
        print("[ERROR] No path found.")
        return {"error": "No path found between the specified locations."}
    except nx.NodeNotFound:
        print("[ERROR] One of the nodes not found in graph.")
        return {"error": "One of the nodes was not found in the graph."}
    except Exception as e:
        print(f"[ERROR] Unexpected error in path generation: {e}")
        return {"error": "An unexpected error occurred while generating paths."}

    # Construct the result
    result_paths = []
    for idx, path in enumerate(k_paths):
        print(f"[DEBUG] Building result for path {idx + 1}")
        coords = [[G_multi.nodes[n]['y'], G_multi.nodes[n]['x']] for n in path]
        total_distance = 0
        for u, v in zip(path[:-1], path[1:]):
            edge_data = G_multi.get_edge_data(u, v)
            if edge_data:
                total_distance += min(d.get("length", 0) for d in edge_data.values())

        result_paths.append({
            "route": coords,
            "distance_km": round(total_distance / 1000, 2)
        })

    print(f"[DEBUG] Returning {len(result_paths)} route(s).")
    return {"routes": result_paths}
