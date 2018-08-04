import csv

data = {}
with open('2012-branches-without-enterprises.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        data[line[0]] = line[1]

la_name_id = {}
with open('la_name_id.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        la_name_id[line[1]] = line[0]

data_by_id = []
for la,id in la_name_id.items():
    data_by_id.append([id, data[la]])

with open('local_units_2012_by_la_id.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for d in data_by_id:
        writer.writerow(d)
