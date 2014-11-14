# this file is used for 
# 1. read nodes_id from sql(planet_osm_ways)
# 2. new a database, create relationship between nodes and roads
#    nodes and roads relationship are
#    in a road, what nodes are in
#    in a node, how many ways are they in
#    if a node only in has two roads, 
#    we can combine two roads together
#    
import csv;
import psycopg2;

conn = psycopg2.connect(database = "beijing_osm_old", user = "postgres", port = "5432", )
cur = conn.cursor()
cur2 = conn.cursor()

con_node = psycopg2.connect(database = "node_index", user = "postgres", port = "5432", )
cur_node = con_node.cursor()

node_string_file = open("nodes_index_roads.csv", "w")
write_nodes = csv.writer(node_string_file)
sql_fetch_database = "SELECT * FROM public.planet_osm_ways"
cur.execute(sql_fetch_database)
nodes_in_road = cur.fetchall()
nodes_list = []
count = 0
#0-->way_id
#1-->way_nodes;
for ways in nodes_in_road:
    count = count + 1
    nodes_query = ways[1]
    nodes_start = nodes_query[0]
    nodes_end = nodes_query[len(nodes_query) - 1]
#    print nodes_start, nodes_end
    find_node_query = "SELECT * FROM public.planet_osm_ways WHERE %d = ANY (planet_osm_ways.nodes)"
#    print nodes_list
    if nodes_list.count(nodes_start) < 2:
        nodes_list.append(nodes_start)
        connect = False;
        way_ids = []
        cur2.execute(find_node_query% (nodes_start))
        way_list = cur2.fetchall()
        for wlist in way_list:
            way_ids.append(wlist[0])
            if(len(wlist) == 2):
                if nodes_end == wlist[1][0] or nodes_end == wlist[1][len(wlist[1] - 1)]:
                    connect = True
        way_ids.append(connect)
#        print way_ids
        insert_query = "INSERT INTO node_index (node_id, index_road) VALUES (%d, '%s'); "
#        print insert_query% (nodes_start, str(way_ids[0:len(way_ids) - 1]))
        cur_node.execute(insert_query% (nodes_start, str(way_ids[0:len(way_ids) - 1])))

        write_nodes.writerow(way_ids)
    if nodes_list.count(nodes_end) < 2  :
        nodes_list.append(nodes_end)
        way_ids = []
        cur2.execute(find_node_query% (nodes_end))
        way_list = cur2.fetchall()

        for wlist in way_list:
            way_ids.append(wlist[0])
            if(len(wlist) == 2):
                if nodes_end == wlist[1][0] or nodes_end == wlist[1][len(wlist[1] - 1)]:
                    connect = True
        way_ids.append(connect)
#        print way_ids
        insert_query = "INSERT INTO node_index (node_id, index_road) VALUES (%d, '%s'); "
#        print insert_query% (nodes_end, str(way_ids[0:len(way_ids) - 1]))
        cur_node.execute(insert_query% (nodes_end, str(way_ids[0:len(way_ids) - 1])))
        write_nodes.writerow(way_ids)
    print str(count/500.0) + "%"
node_string_file.close()

node_string_file = open("nodes_index_roads.csv", "r")
#using file.readlines() can successfully read csv file line by line
conn.commit()
cur.close()
conn.close()
con_node.commit()
cur_node.close()
con_node.close()
