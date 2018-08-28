import csv

names = ['name','name2','name3']

las = {}

with open('lad_17_geo_info.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        for name in names:
            las[line[name]] = line['id']


data = {}
with open('local_units_2012_by_la_id.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        if line[0] not in las:
            print(line[0])
            continue
        data[las[line[0]]] = line[1:]

with open('2012_local_units_by_la.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', '0-4', '4-9', '10-19', '20-49', '49-100', '100-249', '250+', 'Total'])
    for la, d in data.items():
        writer.writerow([la] + d)
