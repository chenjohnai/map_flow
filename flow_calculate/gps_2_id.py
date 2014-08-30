'''
Created on Aug 11, 2014

@author: chen
'''

import psycopg2
import csv

conn = psycopg2.connect(database = "beijing_osm", user = "postgres", port = "5432", )
cur = conn.cursor()

open_csv_file = open("LINESTRING.csv","r")
string_node_file = open("Road_Node.csv", "w")
csvfile_string = csv.reader(open_csv_file)
stringnode_file = csv.writer(string_node_file)
for row in csvfile_string:
    node_count = int(row[1])
    node_list = []
    count = 0
    over_count = 0
    test_count = 0
    for i in range(node_count):

        GPS_point_string = row[i + 2].split(" ")
        GPS_point = [float(GPS_point_string[0])]
        GPS_point.append(float(GPS_point_string[1]))
        GPS_point_real = [int(GPS_point[0]*100), int(GPS_point[1]*100)]
        #print GPS_point_real
        sql_query = "SELECT * FROM public.planet_osm_nodes WHERE planet_osm_nodes.lon = %s OR planet_osm_nodes.lat = %s; "
        cur.execute(sql_query, (GPS_point_real[0], GPS_point_real[1]))
        node_id1 = cur.fetchall()
#        print node_id1[0][0]
        if(len(node_id1) == 1):
            node_list.append(node_id1[0][0])
        if(len(node_id1) > 1):
            for i in range(len(node_id1)):
                flag = 0  
                if(abs(node_id1[i][2] - GPS_point_real[0]) > 5 or abs(node_id1[i][1] - GPS_point_real[1]) > 5):  
                    continue
                if(abs(node_id1[i][2] - GPS_point_real[0]) < 50 and abs(node_id1[i][1] - GPS_point_real[1]) < 50):
                    node_list.append(node_id1[i][0])
                    over_count = over_count + 1
                    flag = 1
                    break
                if(flag < 1):
                    node_list.append('N/A')
                    test_count = test_count + 1
                    print "none match!!!"
        if(len(node_id1) == 0):
            node_list.append('N/A')
            count = count + 1
    print "over:  " + str(over_count) + "   test:  " + str(test_count) + "  none:  " + str(count)
#    stringnode_file.writerow(row)
    node_list.insert(0, row[1])
    node_list.insert(0, row[0])
    node_list.insert(0, over_count)
    node_list.insert(0, test_count)
    stringnode_file.writerow(node_list)    
open_csv_file.close()
string_node_file.close()
    