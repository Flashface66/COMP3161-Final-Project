import random
import csv
import mysql.connector
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt"
)
cursor = db.cursor()
cursor.execute("USE notquiteourvle")

file_types = [".jpg",".svg",".mp3", ".wav", ".flac",".mp4", ".mov", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".txt", ".csv", ".json", ".xml", ".html"]

slide_titles = ["Introduction to ","Objectives for ", "Background Information on ", "Methodology for undertaking ", "Results from ", "Conclusion on ", "Future Directions to ", "References for ", "Overview on ", "Scope of ", "Assumptions to be made in regards to ", "Research Questions to assist on", "Literature Review from ", "Experimental Setup for ", "Data Collection based on ", "Data Analysis in the findings of ", "Findings about ", "Limitations on ", "Recommendations to ", "References on "]


cursor.execute("SELECT * FROM courses")
allcourses = cursor.fetchall()

sections = []
content = []
for course in allcourses:
    code = course[0]
    title = course[1]
    
    numsect = random.randint(6, 10)
    numcontent = random.randint(3, 7)
   
    for i in range(1, numsect):
        courseid = code
        secttitle= 'Topic ' + str(i)
        sections.append([i,courseid,secttitle])

        for y in range(1,numcontent):
            name = random.choice(slide_titles) + secttitle
            file = name + random.choice(file_types)
            content.append([i, code, name, file])

sectionpath = os.path.join('./csvs', 'sections.csv')
with open(sectionpath, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['section_id','course_id', 'section_title'])
    for sect in sections:
        writer.writerow(sect)

sectcontent = os.path.join('./csvs', 'sectioncontent.csv')
with open(sectcontent, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['section_id','course_id', 'content_name', 'content_file'])
    for cont in content:
        writer.writerow(cont)


sql_query = """LOAD DATA LOCAL INFILE './sections.csv'
               INTO TABLE sections
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (section_id, course_id, section_title);"""


builtsections = os.path.join('./sqlFiles', 'load_sections.sql')
with open(builtsections, "w") as f:
    f.write(sql_query)



sql_query = """LOAD DATA LOCAL INFILE './sectioncontent.csv'
               INTO TABLE section_content
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (section_id, course_id, content_name, content_file);"""


generatedcontent = os.path.join('./sqlFiles', 'load_section_content.sql')
with open(generatedcontent, "w") as f:
    f.write(sql_query)

db.commit()
db.close()