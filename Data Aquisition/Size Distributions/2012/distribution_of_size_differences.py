import csv


data = {}
with open('entity_differences.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)

    for line in reader:
        if int(float(line[1]) / 100) in data:
            data[int(float(line[1]) / 100)] += 1
        else:
            data[int(float(line[1]) / 100)] = 1

with open('histogram.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in data.items():
        writer.writerow([key, value])
