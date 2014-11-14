import psycopg2

osm_connect = psycopg2.connect(database = "beijing_osm_old", user = "postgres", port = "5432", )

osm_cursor = osm_connect.cursor()

def node_to_gps(nodeID):
    node_ret = {}
    node_query = "SELECT lat, lon FROM public.planet_osm_nodes WHERE planet_osm_nodes.id = %d;"
    osm_cursor.execute(node_query% int(nodeID))
    try:
        node_lat_lon_pair = osm_cursor.fetchall()[0]
    except:
        return None
    node_ret[str(nodeID)] = node_lat_lon_pair
    return node_ret
    
