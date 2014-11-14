from __future__ import division
import psycopg2
import math

osm_connect = psycopg2.connect(database = "beijing_osm_old", user = "postgres", port = "5432", )

osm_cursor = osm_connect.cursor()

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

def node_to_gps(nodeID):
    sql_query = "SELECT * FROM public.planet_osm_nodes WHERE id = %d"
    osm_cursor.execute(sql_query% nodeID)
    node_list = osm_cursor.fetchall()[0]
    node_lat = node_list[1]/100
    node_lon = node_list[2]/100
    node_lat_a = y2lat(node_lat)
    node_lon_a = x2lon(node_lon)
    return (node_lat_a, node_lon_a)
'''
Created on Oct 10, 2014

@author: chen
'''
