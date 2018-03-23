import csv
import datetime
from py2neo import Graph, Path
graph = Graph("http://localhost:7474/db/data/", password="admin")

start_time = datetime.datetime.now()
file_path = "C:/Users/Desktop/lego-database/"
processed_row_count = 0

def get_base_command(csv_name=None):
    file = "'file:///" + file_path + csv_name + ".csv" + "'"
    return "USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM " + file + " AS row "

def run_command(csv_name=None, command=None):
    base_command = get_base_command(csv_name)
    return_count = graph.data(base_command + command)
    return return_count

def load_file(csv_name=None, command=None):
    print('Starting ' + csv_name + '. Start time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f"))
    base_command = get_base_command(csv_name)
    return_count = graph.data(base_command + command)
    print('Total Rows in File: ' + str(get_file_row_count(csv_name)) + '. Total Rows Loaded: ' + str(return_count))
    print('Finished ' + csv_name + '. End time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f") + '\n')

def create_relationship(relationship_name=None, command=None):
    print('Starting ' + relationship_name + ' Relationship. Start time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f"))
    return_count = graph.data(command)
    print('Total Relationships Created: ' + str(return_count))
    print('Finished ' + relationship_name + ' Relationship. End time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f") + '\n')

def get_file_row_count(csv_name=None):
    file = file_path + csv_name + ".csv"
    with open(file, 'r+', encoding="utf8") as input_file:
        reader_file = csv.reader(input_file)
        file_row_count = len(list(reader_file))-1
    return file_row_count
	
def load_all():
    load_file("parts", "CREATE (Part:Part {id:row.part_num, name:row.name, cat_id:row.part_cat_id}) RETURN COUNT(Part)")
    load_file("colors", "CREATE (Color:Color {id:row.id, name:row.name, rgb:row.rgb, is_trans:row.is_trans}) RETURN COUNT(Color)")
    #load_file("sets", "CREATE (Set:Set {id:row.set_num, name:row.name, num_parts:row.num_parts}) RETURN COUNT(Set)")
    load_file("themes", "CREATE (Theme:Theme {id:row.id, name:row.name, parent_id:row.parent_id}) RETURN COUNT(Theme)")
    load_file("part_categories", "CREATE (PartCategory:PartCategory {id:row.id, name:row.name}) RETURN COUNT(PartCategory)")
	
    print('Starting Year Node Creation. Start time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f"))
    return_count = run_command("sets", "WITH DISTINCT row.year as row_year CREATE (Year:Year {id:toInt(row_year)}) RETURN COUNT(Year)")
    # make sure we have all years between min and max (there are gaps in the 50's)
    graph.run("MATCH (year:Year) WITH range(min(year.id), max(year.id)-1) AS years FOREACH (currentYear IN years | MERGE (:Year {id:currentYear}))")
    # make a linked list
    graph.run("MATCH (year:Year) MATCH (nextYear:Year {id:year.id+1}) MERGE (year)-[r:NEXT]->(nextYear)")
    print('Total Rows Loaded: ' + str(graph.data("MATCH (Year:Year) RETURN COUNT(Year)")))
    print('Finished Year Node Creation. End time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f") + '\n')
	
    print('Starting Set Node, HAS_THEME and RELEASED Relationship. Start time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f"))
    return_count = run_command("sets", "MATCH (theme:Theme {id:row.theme_id}) MATCH (year:Year {id:toInt(row.year)}) CREATE (Set:Set {id:row.set_num, name:row.name, num_parts:row.num_parts})-[HAS_THEME_Relationship:HAS_THEME]->(theme) CREATE (Set)-[RELEASED_Relationship:RELEASED]->(year) RETURN COUNT(Set), COUNT(HAS_THEME_Relationship), COUNT(RELEASED_Relationship)")
    print('Total Rows in File: ' + str(get_file_row_count("sets")) + '. Total Nodes/Relationships Created: ' + str(return_count))
    print('Finished Set Node, HAS_THEME and RELEASED Relationship. End time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f") + '\n')
	    	
    create_relationship("IS_PARENT", "match (child:Theme), (parent:Theme) where child.parent_id = parent.id create (parent)-[Relationship:IS_PARENT]->(child) RETURN COUNT(Relationship)")

    load_file("parts_sets_link", "CREATE (Part_Set_Link:Part_Set_Link {set_num:row.set_num, part_num:row.part_num, quantity:row.quantity, is_spare:row.is_spare, color_id:row.color_id}) RETURN COUNT(Part_Set_Link)")

    create_relationship("CONTAINS", "MATCH (s:Set), (p:Part), (l:Part_Set_Link) where s.id = l.set_num and p.id = l.part_num CREATE (p)<-[Relationship:CONTAINS{quantity:l.quantity, is_spare:l.is_spare, color_id:l.color_id}]-(s) RETURN COUNT(Relationship)")

    print('Deleting Part_Set_Link. Start time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f"))
    graph.run("MATCH (l:Part_Set_Link) DELETE l")
    print('Finished Deleting Part_Set_Link. End time: ' + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S:%f") + '\n')

    print('Total Loading Time: ' + str(datetime.datetime.now() - start_time))

load_all()