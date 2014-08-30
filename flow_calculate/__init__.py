import psycopg2

import psycopg2.extras
import csv

conn = psycopg2.connect(database = "beijing_osm", user = "postgres", port = "5432", )

cur = conn.cursor()
cur2 = conn.cursor()
sql_string = "\\d "
print(sql_string)
cur.execute("select planet_osm_roads.\"OSM_ID\" , ST_NumPoints(planet_osm_roads.\"the_geom\"),  ST_AsText(planet_osm_roads.\"the_geom\")  from public.planet_osm_roads;")
cur2.execute("select count(*) from public.planet_osm_roads;")
rows = cur.fetchall()
rowscount = cur2.fetchall();
print rowscount[0]
road = ()
line_string = []

node_count = []
road_id = []
print rows.count
#for i in rows:
#    print list(i)
#    line_string.append(i[2])
#    node_count.append(i[1])
#    road_id.append(i[0])
#    print line_string[i]
for i in range(1, len(rows)):
    print list(rows[i])
    line_string.append(rows[i][2])
    node_count.append(rows[i][1])
    road_id.append(rows[i][0])
    print line_string[i - 1]
    
a = line_string[1]
a = a.strip('LINE')

line_file = open("LINESTRING.csv","w")
linefile = csv.writer(line_file)

for i in range(1, len(line_string)):
    line_string[i] = line_string[i].strip('LINESTRING')
    line_string[i] = line_string[i].strip('(')
    line_string[i] = line_string[i].strip(')')
    line_string[i] = line_string[i].split(",")
    line_string[i].insert(0,node_count[i])
    line_string[i].insert(0,road_id[i])
    print line_string[i]
    print len(line_string[i])
    linefile.writerow(line_string[i])
    
line_file.close()

