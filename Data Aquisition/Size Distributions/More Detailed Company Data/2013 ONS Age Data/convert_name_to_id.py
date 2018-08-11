import csv

NAME_HEADERS = ['name', 'name2', 'name3']

def main():
    las = load_la_ids()

    age_dist = load_la_age_dist()

    output = {}

    for la in age_dist:
        if la[0] in las:
            output[las[la[0]]] = la[1:]
        else:
            print(la[0])

    with open('2013_ONS_by_age_la_id.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for id, data in output.items():
            writer.writerow([id] + data)
def load_la_ids():
    data = {}
    with open('lad_17_geo_info.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            for name in NAME_HEADERS:
                if line[name] != '':
                    data[line[name]] = line['id']
    return data
def load_la_age_dist():
    data = []
    with open('ONS_age_dist_by_la_name.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data.append(line)
    return data

if __name__ == '__main__':
    main()
