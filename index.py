import csv
from falkordb import FalkorDB

#this will remove the sinsle quotes in the data so no errors occurs during executing .....like ' will replace with \ otherwise you will get error some time while executing the query 
def escape(value):
    return value.replace("'", "\\'")

client = FalkorDB(host="localhost", port=6379)
graph = client.select_graph("PropertiesGraph")

try:
    graph.query("MATCH (n) DETACH DELETE n")
except:
    pass

csv_file = "data/properties.csv"
with open("data/properties.csv") as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        props = ", ".join(f"`{h}`:'{escape(v)}'" for h, v in zip(headers, row))
        graph.query(f"CREATE (:Property {{{props}}})")
        
print("roperties imported succesfuly!")

graph.query("MATCH (p:Property) MERGE (:Project {`Project Name`: p.`Project Name`})")
graph.query("""
MATCH (p:Property), (proj:Project {`Project Name`: p.`Project Name`})
MERGE (p)-[:BELONGS_TO]->(proj)
""")

graph.query("MATCH (p:Property) MERGE (:City {`City`: p.`City`})")
graph.query("""
MATCH (p:Property), (c:City {`City`: p.`City`})
MERGE (p)-[:LOCATED_IN]->(c)
""")

print(" Done dona don...jhingalala jhingalala...")