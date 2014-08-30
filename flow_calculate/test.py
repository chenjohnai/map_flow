'''
Created on Aug 15, 2014

@author: chen
'''
import csv;
import psycopg2;
import os;
import scipy.io as sio
import numpy as np

def insert_node(start_point, end_point):
    node_list = []
    sql_query = "select * from public.road_id where road_id.node_id ~ '%s'"
    cur.execute(sql_query, (start_point))
    traj_start = cur.fetchall()
    sql_query = "select * from public.road_id where road_id.node_id ~ '%s'"
    cur.execute(sql_query, (end_point))
    traj_end = cur.fetchall()
    if(traj_start[0] == traj_end[0]):
        start = traj_start[2].index(traj_start[0])
        end = traj_start[2].index(traj_end[0])
        node_list = node_list.append(traj_start[2][start:end])
    return node_list

node_string_file = open("g:\\sort\\2\\13301104001_sort.csv", "r")
node_string = csv.reader(node_string_file)
temp_file = open("g:\\sort\\2\\tmp.csv", "w")
filedir = "g:\\sort\\2\\mat\\"
conn = psycopg2.connect(database = "node_in_road", user = "postgres", port = "5432", )
cur = conn.cursor()
cur_count = conn.cursor()



file_list = os.listdir(filedir)
filename = filedir + file_list[0]
data = sio.loadmat(filename)
start_point = data['startpoint']
end_point = data['endpoint']
start_time = data['starttime']
end_time = data['endtime']
print len(start_point), len(end_point)
i = 0
node_insert_list = insert_node(start_point[i], end_point[i])

print node_insert_list

conn = psycopg2.connect(database = "node_in_road", user = "postgres", port = "5432", )
cur = conn.cursor()
cur_count = conn.cursor()

start_point = '0'

for row in node_string:
    if(start_point == '0'):
        continue
    end_point = row[4]
    
    start_point  = row[5]
