from __future__ import division
import psycopg2
  
way_index_conn = psycopg2.connect(database = "node_index", user = "postgres", port = "5432", host = "localhost")
way_index_cur = way_index_conn.cursor()

search_index_conn = psycopg2.connect(database = "beijing_osm_old", user = "postgres", port = "5432")
search_cur = search_index_conn.cursor()

way_list_query = "SELECT id FROM public.planet_osm_ways"
search_cur.execute(way_list_query)
way_index_list = list(search_cur.fetchall())
counter = 0
all_length = len(way_index_list)
for single_way in way_index_list:
    nodes_in_way_query = "SELECT nodes FROM public.planet_osm_ways WHERE id = %d"
    search_cur.execute(nodes_in_way_query% (single_way))
    nodes = list(search_cur.fetchall()[0])[0]
    single_way_list = []
    for node in nodes:
        node_find_road_query = "SELECT id FROM public.planet_osm_ways WHERE %d = ANY (planet_osm_ways.nodes)"
        search_cur.execute(node_find_road_query% (node))
        cur_node_way = search_cur.fetchall()
        for way in cur_node_way: 
            single_way_list.append(way[0]) 
    single_way_list = list(set(single_way_list))
    single_way_list.remove(single_way[0])
    write_ways_index_query = "INSERT INTO ways_index (id, ways_index) VALUES (%d,'%s')"
    way_index_cur.execute(write_ways_index_query% (single_way[0], single_way_list))
    counter = counter + 1
    print counter/all_length

way_index_conn.commit()
search_index_conn.commit()
way_index_cur.close()
search_cur.close()
'''
#Created on Sep 24, 2014

#@author: chen
'''