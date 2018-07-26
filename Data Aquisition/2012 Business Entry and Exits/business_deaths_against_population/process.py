import csv

new_businesses = {}
population = {}

with open('business_deaths_by_local_authority.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print(row[1])
		new_businesses[row[0]] = int(row[1])

with open('uk_local_authority_populations_2012.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		population[row[0]] = int(row[1])

dataset = []

for key, value in population.items():
	dataset.append([population[key], new_businesses[key]])

with open('data.csv', 'w') as csvfile:
	writer = csv.writer(csvfile)
	for line in dataset:
		writer.writerow(line)
