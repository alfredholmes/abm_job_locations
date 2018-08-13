import csv


data = {}
with open('entity_differences.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        data[line[0]] = [int(line[2]), int(line[3])]

regions = {}
with open('lad_17_geo_info.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        if line[1] != '':
            regions[line[0]] = line[1]
        else:
            regions[line[0]] = line[2]
regional_data = {}


for id, d in data.items():
    region = regions[id]
    print(id)
    if region in regional_data:
        regional_data[region][0] += d[0]
        regional_data[region][1] += d[1]
    else:
        regional_data[region] = [0] * 2
        regional_data[region][0]  = d[0]
        regional_data[region][1]  = d[1]


with open('regional_totals.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for region, d in regional_data.items():
        writer.writerow([region] + d)
