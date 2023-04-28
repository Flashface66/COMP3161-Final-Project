import csv
import random
import os

# Generate a list of unique admin IDs between 100,000 and 200,000
ad_id = random.sample(range(100000, 200000), 5)

first_names = ['Adair', 'Bellamy', 'Calliope', 'Dashiell', 'Emrys', 'Finley', 'Greyson', 'Holland', 'Isolde', 'Jovian', 'Kael', 'Lyra', 'Maven', 'Nieve', 'Orion', 'Phoenixia', 'Quincy', 'Rosalind', 'Soren', 'Thalia']

last_names = ['Ashcroft', 'Brightman', 'Cordova', 'Delgado', 'Everly', 'Fortune', 'Goldstein', 'Harrington', 'Irons', 'Kensington', 'Langley', 'MacAllister', 'Navarro', 'Olivetti', 'Paxton', 'Quinones', 'Rutherford', 'Sinclair', 'Teague', 'Vega']

adminlst = []
for admin in ad_id:
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    email = f"{last_name.lower()}.{first_name.lower()}@example.rdu"
    password= "password"

    adminlst.append([admin, first_name, last_name, email, password, 3])


adminroster = os.path.join('./csvs', 'admin.csv')

with open(adminroster, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['admin_id', 'first_name', 'last_name', 'email', 'password', 'user_type'])
    for ad in adminlst:
        writer.writerow(ad)