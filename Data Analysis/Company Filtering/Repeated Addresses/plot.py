import csv

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

def main():
	ch_data, ons_totals = get_data()
	plt.figure(figsize=(14, 6))
	plt.subplot(1, 2, 1)
	plt.scatter(ons_totals, ch_data['repeats'], alpha=0.3)
	grad = minimize(lambda x: np.sum(np.array(ch_data['repeats'])  - x * np.array(ons_totals)) ** 2, 1.0).x
	plt.plot(ons_totals, grad * ons_totals, color='orange')
	plt.title('One Enterprise per Company')
	plt.xlabel('ONS')
	plt.ylabel('Companies House')


	plt.subplot(1, 2, 2)
	plt.scatter(ons_totals, ch_data['no_repeats'] , alpha=0.3)
	grad = minimize(lambda x: np.sum(np.array(ch_data['no_repeats']) - x * ons_totals) ** 2, 1).x
	plt.plot(ons_totals, grad * ons_totals, color='orange')
	plt.title('One Enterprise per Address')
	plt.xlabel('ONS')

	plt.savefig('filtered_addresses')

	plt.show()


def get_data():
	data = {'no_repeats': [], 'repeats': []}
	las = []
	with open('no_repeated_addresses_2017_la_totals.csv', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for line in reader:
			data['repeats'].append(float(line[1]))
			data['no_repeats'].append(float(line[2]))
			las.append(line[0])

	ons_data = np.zeros(len(las))
	with open('2017_enterprise_size_by_la.csv', 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		sizes = ['0-4','5-9','10-19','20-49','50-99','100-249','250+']
		for line in reader:
			if line['la'] in las:
				id = las.index(line['la'])
				ons_data[id] += np.sum([float(line[s]) for s in sizes])

	return data, ons_data

if __name__ == '__main__':
	main()
