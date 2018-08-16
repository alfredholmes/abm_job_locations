import csv, random

#Script to test the effects of companies being registered multiple times on companies house / companies form partnerships that are
#recorded as one company on companies house


P_MATCH = 0.0003
N_CITIES = 100



def main():
    cities = []
    for _ in range(N_CITIES):
        cities.append(random.randint(1000, 5000))

    data = []
    for city in cities:
        print(city)
        partnerships = []
        for i in range(city):
            for j in range(i + 1, city):
                if random.random() < P_MATCH:
                    partnerships.append((i, j))
        groups = []
        for i, j in partnerships:
            i_group = None
            j_group = None
            for x, group in enumerate(groups):
                if i in group:
                    i_group = x
                if j in group:
                    j_group = x
                if i_group is not None and j_group is not None:
                    break
            if i_group is not None and j_group is None:
                groups[i_group].add(j)
                continue
            if j_group is not None and i_group is None:
                groups[j_group].add(i)
                continue
            if i_group is not None and j_group is not None:
                #join the two groups
                m = min(i_group, j_group)
                M = max(i_group, j_group)
                groups[m] = groups[m].union(groups[M])
                del groups[M]
                continue
            groups.append(set([i, j]))

        not_listed = 0
        for i in range(city):
            for group in groups:
                if i in group:
                    break
            else:
                not_listed += 1
        data.append([city, not_listed + len(groups)])

    with open('partnerships_results.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for d in data:
            writer.writerow(d)

if __name__ == '__main__':
    main()
