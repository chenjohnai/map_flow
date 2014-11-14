import csv
import psycopg2;

import math


def y2lat(a):
    return 180.0/math.pi*(2.0*math.atan(math.exp(a*math.pi/180.0))-math.pi/2.0)
def lat2y(a):
    return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))
def x2lon(a):
    return a/(math.pi/180)/6378137

file_read = open("g:\\sort\\2\\13301104001_sort.csv","r")
file_write = open("g:\\sort_new\\2\\13301104001_sort.csv", "w")
#file_write = open("g:\\sort\\2\\13301104001_sort_new.csv")

filewrite = csv.writer(file_write)
traj_read = csv.reader(file_read)

conn_old = psycopg2.connect(database = "beijing_osm_old", user = "postgres", port = "5432", )

conn_new = psycopg2.connect(database = "beijing_osm", user = "postgres", port = "5432", )
cursor_old = conn_old.cursor()
cursor_new = conn_new.cursor()
wrong_node = 0
for traj in traj_read:
    node_start_end = traj[4:6]

    node_new = []

    for node in node_start_end:
        node_use = node    
#        node_use = int(node_use)
        sql_query_oldnode = "SELECT * FROM public.planet_osm_nodes WHERE planet_osm_nodes.id = %s; "
        cursor_old.execute(sql_query_oldnode% (node_use))
        node_start_line = cursor_old.fetchall()
        node_start_lat = node_start_line[0][1]
        node_start_lon = node_start_line[0][2]
    
        sql_query_newnode = "SELECT * FROM public.planet_osm_nodes WHERE planet_osm_nodes.lat = %s AND planet_osm_nodes.lon = %s; "
        print sql_query_newnode% (node_start_lat, node_start_lon)
        cursor_new.execute(sql_query_newnode% (node_start_lat, node_start_lon))
        node_start_new_line = cursor_new.fetchall()
        node_start_new = [node_start_new_line[0][0]]

        node_new.append(node_start_new)
        if node_new == False:
            wrong_node = wrong_node + 1
    print node_new
    traj[4:6] = node_new
    
    filewrite.writerow(traj)
print wrong_node
file_write.close()

    
    

#csv.writer(string)

'''
Created on Sep 13, 2014

@author: chen
'''
