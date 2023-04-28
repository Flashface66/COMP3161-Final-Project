import csv
import random
import os

# Generate a list of unique student IDs between 620,000 and 720,000
student_ids = random.sample(range(620000, 720001), 100000)

first_names = ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Evelyn', 'Abigail', 'Harper', 'Emily', 'Elizabeth', 'Avery', 'Sofia', 'Ella', 'Madison', 'Scarlett', 'Victoria', 'Aria', 'Liam','Noah','Ethan','Aiden','Caden','Jackson','Grayson','Lucas','Mason','Logan','Oliver','Elijah','Caleb','Benjamin','William','James','Michael','Alexander','Daniel','Joseph']


last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'King', 'Wright', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed', 'Cook', 'Morgan', 'Bell', 'Cooper']

courses = {
    'Introduction to databases': 'ITDB3007',
    'Object-Oriented Programming in Java': 'ITJA2010',
    'Web Development with HTML, CSS, and JavaScript': 'ITWD3010',
    'Data Structures and Algorithms': 'ITDS4020',
    'Operating Systems': 'ITOS3010',
    'Computer Networks': 'ITCN4030',
    'Database Management Systems': 'ITDB4010',
    'Software Engineering': 'ITSE5010',
    'Artificial Intelligence': 'ITAI6010',
    'Machine Learning': 'ITML6015',
    'Computer Graphics': 'ITCG4010',
    'Human-Computer Interaction': 'ITHC4010',
    'Computer Architecture and Organization': 'ITCA4010',
    'Information Security and Privacy': 'ITIS5010',
    'Big Data Analytics': 'ITBD6010',
    'Cloud Computing': 'ITCC5010',
    'Blockchain and Cryptocurrencies': 'ITBC6010',
    'Computer Vision': 'ITCV6010',
    'Natural Language Processing': 'ITNL6010',
    'Data Mining': 'ITDM5010',
    'Data Warehousing': 'ITDW5010',
    'Information Retrieval': 'ITIR5010',
    'Internet of Things': 'ITIO6010',
    'Network Security': 'ITNS5010',
    'Mobile Application Development': 'ITMA5010',
    'Programming Languages': 'ITPL4010',
    'Compiler Design': 'ITCD5010',
    'Computer Forensics': 'ITCF6010',
    'Embedded Systems': 'ITES5010',
    'Parallel and Distributed Computing': 'ITPC6010',
    'Data Science': 'ITDS6010',
    'Cloud Security': 'ITCS6010',
    'Computer Ethics and Professionalism': 'ITCE4010',
    'Computer Music and Sound Design': 'ITMS4010',
    'Computer Gaming and Virtual Reality': 'ITCG4015',
    'Social Computing and Networks': 'ITSC6010',
    'Ubiquitous Computing': 'ITUC6010',
    'Virtual Machines and Emulators': 'ITVM5010',
    'Web Services and APIs': 'ITWS5010',
    'Advanced Programming Techniques': 'ITAP5010',
    'Digital Image Processing': 'ITDI6010',
    'Digital Signal Processing': 'ITDS6015',
    'Distributed Systems': 'ITDS5010',
    'Human-Robot Interaction': 'ITHR6010',
    'Innovative Computing Technologies': 'ITIC6010',
    'Machine Vision and Perception': 'ITMP6010',
    'Multimedia Computing': 'ITMC6010',
    'Network Programming': 'ITNP5010',
    'Real-Time Systems': 'ITRT5010',
    'Robotics and Automation': 'ITRA6010',
    'Web Content Management Systems': 'ITWC5010',
    'Web Security': 'ITWS6010',
    'Wireless Networks': 'ITWN5010',
    'Cloud Computing Technologies': 'ITCC6010',
    'Cloud Computing Security': 'ITCC6015',
    'Cloud Computing Architecture': 'ITCC6020',
    'Cloud Computing Services': 'ITCC6025',
    'Computational Intelligence': 'ITCI6010',
    'Computer Algebra Systems': 'ITAS5010',
    'Computer Networks and Security': 'ITCN5010',
    'Introduction to Biology': 'BIOL1001',
    'General Biology I': 'BIOL1011',
    'General Biology II': 'BIOL1021',
    'Cell Biology': 'BIOL2021',
    'Genetics': 'BIOL3011',
    'Evolution': 'BIOL3021',
    'Ecology': 'BIOL3031',
    'Anatomy and Physiology': 'BIOL4011',
    'Molecular Biology': 'BIOL4021',
    'Microbiology': 'BIOL4031',
    'Neurobiology': 'BIOL4041',
    'Immunology': 'BIOL4051',
    'Biochemistry': 'BIOL4061',
    'Plant Biology': 'BIOL4071',
    'Animal Behavior': 'BIOL4081',
    'Conservation Biology': 'BIOL4091',
    'Biostatistics': 'BIOL4101',
    'Marine Biology': 'BIOL4111',
    'Environmental Science': 'BIOL4121',
    'Human Anatomy': 'BIOL4131',
    'Physiology': 'BIOL4141',
    'Developmental Biology': 'BIOL4151',
    'Pharmacology': 'BIOL4161',
    'Cancer Biology': 'BIOL4171',
    'Medical Microbiology': 'BIOL4181',
    'Ecological Genetics': 'BIOL4191',
    'Bioinformatics': 'BIOL4201',
    'Virology': 'BIOL4211',
    'Immunogenetics': 'BIOL4221',
    'Population Biology': 'BIOL4231',
    'Neuropharmacology': 'BIOL4241',
    'Biological Oceanography': 'BIOL4251',
    'Biomechanics': 'BIOL4261',
    'Ecotoxicology': 'BIOL4271',
    'Animal Physiology': 'BIOL4281',
    'Stem Cell Biology': 'BIOL4291',
    'Entomology': 'BIOL4301',
    'Animal Ecology': 'BIOL4311',
    'Environmental Physiology': 'BIOL4321',
    'Bioengineering': 'BIOL4331',
    'Medical Physiology': 'BIOL4341',
    'Physiological Ecology': 'BIOL4351',
    'Computational Biology': 'BIOL4361',
    'Cognitive Neuroscience': 'BIOL4371',
    'Developmental Genetics': 'BIOL4381',
    'Biodiversity and Conservation': 'BIOL4391',
    'Endocrinology': 'BIOL4401',
    'Behavioral Ecology': 'BIOL4411',
    'Toxicology': 'BIOL4421',
    'Bioenergetics': 'BIOL4431',
    'Plant Physiology': 'BIOL4441',
    'Biological Modeling': 'BIOL4451',
    'Genomics': 'BIOL4461',
    'Parasitology': 'BIOL4471',
    'Symbiosis': 'BIOL4481',
    'Aquatic Ecology': 'BIOL4491',
    'Bioethics': 'BIOL4501',
    'Animal Communication': 'BIOL4511',
    'Conservation Genetics': 'BIOL4521',
    'Molecular Genetics': 'BIOL4531',
    'Biomaterials': 'BIOL4541',
    'Evolutionary Genetics': 'BIOL4551',
    'Introduction to Chemistry': 'CHEM1001',
    'General Chemistry I': 'CHEM1101',
    'General Chemistry II': 'CHEM1201',
    'Organic Chemistry I': 'CHEM2101',
    'Organic Chemistry II': 'CHEM2201',
    'Physical Chemistry I': 'CHEM3101',
    'Physical Chemistry II': 'CHEM3201',
    'Analytical Chemistry': 'CHEM3301',
    'Inorganic Chemistry': 'CHEM3401',
    'Biochemistry I': 'CHEM4101',
    'Biochemistry II': 'CHEM4201',
    'Environmental Chemistry': 'CHEM4301',
    'Polymer Chemistry': 'CHEM4401',
    'Nuclear Chemistry': 'CHEM4501',
    'Materials Chemistry': 'CHEM4601',
    'Food Chemistry': 'CHEM4701',
    'Green Chemistry': 'CHEM4801',
    'Medicinal Chemistry': 'CHEM4901',
    'Supramolecular Chemistry': 'CHEM5001',
    'Chemical Kinetics': 'CHEM5101',
    'Quantum Chemistry': 'CHEM5201',
    'Electrochemistry': 'CHEM5301',
    'Spectroscopy': 'CHEM5401',
    'Thermodynamics': 'CHEM5501',
    'Surface Chemistry': 'CHEM5601',
    'Photochemistry': 'CHEM5701',
    'Coordination Chemistry': 'CHEM5801',
    'Chemical Biology': 'CHEM5901',
    'Forensic Chemistry': 'CHEM6001',
    'Astrochemistry': 'CHEM6101',
    'Geochemistry': 'CHEM6201',
    'Chemical Engineering': 'CHEM6301',
    'Nanomaterials Chemistry': 'CHEM6401',
    'Organometallic Chemistry': 'CHEM6501',
    'Chemical Ecology': 'CHEM6601',
    'Chemical Toxicology': 'CHEM6701',
    'Advanced Organic Synthesis': 'CHEM6801',
    'Advanced Physical Chemistry': 'CHEM6901',
    'Chemical Informatics': 'CHEM7001',
    'Chemical Education': 'CHEM7101',
    'Chemical History': 'CHEM7201',
    'Chemical Philosophy': 'CHEM7301',
    'Science Communication for Chemists': 'CHEM7401',
    'Science Writing for Chemists': 'CHEM7501',
    'Scientific Ethics in Chemistry': 'CHEM7601',
    'Calculus I': 'MATH1010',
    'Calculus II': 'MATH1020',
    'Linear Algebra': 'MATH2010',
    'Discrete Mathematics': 'MATH2020',
    'Differential Equations': 'MATH3010',
    'Abstract Algebra': 'MATH3020',
    'Real Analysis I': 'MATH4010',
    'Real Analysis II': 'MATH4020',
    'Topology': 'MATH4030',
    'Numerical Analysis': 'MATH4040',
    'Calculus III': 'MATH1030',
    'Multivariable Calculus': 'MATH2015',
    'Partial Differential Equations': 'MATH3015',
    'Probability Theory': 'MATH3025',
    'Stochastic Processes': 'MATH4025',
    'Complex Analysis': 'MATH4035',
    'Functional Analysis': 'MATH4045',
    'Graph Theory': 'MATH4055',
    'Combinatorics': 'MATH4065',
    'Algebraic Geometry': 'MATH4075',
    'Introduction to Civil Engineering': 'CEEN1001',
    'Structural Analysis and Design': 'CEEN2002',
    'Soil Mechanics and Foundations': 'CEEN3003',
    'Introduction to Environmental Engineering': 'CEEN4004',
    'Introduction to Architecture': 'ARCH1001',
    'Architectural Design and Representation': 'ARCH2002',
    'Building Systems and Technologies': 'ARCH3003',
    'Sustainable Architecture and Urbanism': 'ARCH4004',
    'Introduction to Mechanical Engineering': 'MEEN1001',
    'Thermodynamics': 'MEEN2002',
    'Fluid Mechanics': 'MEEN3003',
    'Materials Science and Engineering': 'MEEN4004',
    'Introduction to Electrical Engineering': 'ELEN1001',
    'Circuits and Electronics': 'ELEN2002',
    'Digital Signal Processing': 'ELEN3003',
    'Power Systems Analysis': 'ELEN4004',
    'Structural Dynamics': 'CEEN5005',
    'Transportation Engineering': 'CEEN6006',
    'Water Resources Engineering': 'CEEN7007',
    'Advanced Topics in Environmental Engineering': 'CEEN8008',
    'Architectural History and Theory': 'ARCH5005',
    'Building Information Modeling': 'ARCH6006',
    'Urban Design and Planning': 'ARCH7007',
    'Advanced Topics in Sustainable Architecture': 'ARCH8008',
    'Mechanical Design and Manufacturing': 'MEEN5005',
    'Robotics and Control': 'MEEN6006',
    'Heat Transfer': 'MEEN7007',
    'Advanced Topics in Materials Science and Engineering': 'MEEN8008',
    'Power Electronics and Renewable Energy': 'ELEN5005',
    'Advanced Circuit Design': 'ELEN6006',
    'Wireless Communications': 'ELEN7007',
    'Advanced Topics in Power Systems Analysis': 'ELEN8008',
}

students = []
for student_id in student_ids:
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    password = "password"

    email = f"{last_name.lower()}.{first_name.lower()}@example.com"

    students.append([student_id, first_name, last_name, email, password, 1])



studentroster = os.path.join('./csvs', 'students.csv')
coursesheet = os.path.join('./csvs', 'courses.csv')
student_courses = os.path.join('./csvs', 'student_course.csv')

with open(studentroster, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['student_id', 'first_name', 'last_name', 'email', 'password', 'user_type'])
    for student in students:
        writer.writerow(student)

allcourses = []
for course, id in courses.items():
    allcourses.append([id,course])


with open(coursesheet, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['course_id', 'course_name'])
    for course in allcourses:
        writer.writerow(course)


with open(student_courses, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['student_id', 'course_id'])
    for student in students:
        num_courses = random.randint(3, 6)
        course_ids = []
        while len(course_ids) < num_courses:
            course_id = random.choice(list(courses.values()))
            if course_id in course_ids or course_ids.count(course_id) >= 10:
                continue
            course_ids.append(course_id)
        for course_id in course_ids:
            writer.writerow([student[0], course_id])