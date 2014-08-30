import csv;
import psycopg2;

node_string_file = open("Road_Node.csv", "r")
node_string = csv.reader(node_string_file)

conn = psycopg2.connect(database = "node_in_road", user = "postgres", port = "5432", )
cur = conn.cursor()
cur_count = conn.cursor()

i = 0
for row in node_string:
    road_id = int(float(row[2]))
    node_count = int(float(row[3]))
    list_nodeid = row[4: node_count + 4 : 1]
    list_nodeid = ','.join(list_nodeid)

    print list_nodeid
    i = i + 1
    sql_query3 = "INSERT into public.road_id values(%s, %s, %s);"
    cur.execute(sql_query3, (road_id, i, list_nodeid ))
    cur.execute("select * from public.road_id;")
conn.commit()
cur.close()
conn.close()
    