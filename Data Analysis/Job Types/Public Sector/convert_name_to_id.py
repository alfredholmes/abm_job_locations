import csv

data = []
with open('public_sector_jobs_2012_by_la.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        data.append(line)

la_name_id = {}
with open('la_name_id.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        la_name_id[line[1]] = line[0]


for d in data:

    name = d[0]
    print(name)
    id = la_name_id[name]
    d[0] = id

with open('public_sector_jobs_2012_by_laid.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for d in data:
        writer.writerow(d)
