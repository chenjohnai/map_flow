from __future__ import division
import math
import psycopg2

def y2lat(a):
    l = a/6378137
    m = math.exp(l)
    t = math.atan(m)
    return 180.0/math.pi*(2.0*t-math.pi/2.0)
def lat2y(a):
    return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))
def x2lon(a):
    return a/(math.pi/180)/6378137
def lon2x(a):
    return a*(math.pi/180)*6378137

conn = psycopg2.connect(database = "beijing_osm_old", user = "postgres", port = "5432", )
cur = conn.cursor()

filename = "test.txt"
write_node_file = open(filename, "w")

node_list = [356721990L, 356721989L, 356721988L, 356721987L, 356721986L, 356721985L, 356721984L, 356721983L, 356721982L, 356721981L, 356721980L, 356721979L, 356721978L, 356721977L, 425298842L, 425298834L, 425298838L, 425298842L, 425298845L, 425298865L, 425298848L, 611031122L, 425298860L, 425298850L, 425298852L, 425298855L, 425298862L, 425298857L, 425298834L, 611031122L, 356721975L, 356721974L, 380376222L, 356721973L, 356721972L, 356721971L]
for node in node_list:
    sql_query = "SELECT * FROM public.planet_osm_nodes WHERE id = %d"
    cur.execute(sql_query% node)
    node_list = cur.fetchall()[0]
    node_lat = node_list[1]/100
    node_lon = node_list[2]/100
    node_lat_a = y2lat(node_lat)
    node_lon_a = x2lon(node_lon)
    print node_lat_a
    print node_lon_a
    write_node_file.writelines(str(node_lat_a) + "  " + str(node_lon_a))
    write_node_file.writelines("\n")
    



'''


Created on Oct 2, 2014

@author: chen
'''
