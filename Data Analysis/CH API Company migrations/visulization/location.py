import csv

class LocationManager:
    def __init__(self, local_authority_data, company_migration_data):
        self.local_authorities = {}

        business_migrations = []

        with open(company_migration_data, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                business_migrations.append(line)

        with open(local_authority_data, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                self.local_authorities[line['lad17cd']] = LocalAuthority(line['lad17cd'], (float(line['long']), float(line['lat'])))

        for id,la in self.local_authorities.items():
            la.add_migrations(business_migrations, self.local_authorities)

class LocalAuthority:
    def __init__(self, id, location):
        self.id = id
        self.long = location[0]
        self.lat = location[1]



    def add_migrations(self, business_migrations, local_authorities):
        self.immigration = {}
        self.emmigration = {}

        for migration in business_migrations:

            if migration[0] == self.id:
                try:
                    self.emmigration[local_authorities[migration[1]]] = int(migration[2])
                except:
                    pass
            elif migration[1] == self.id:
                try:
                    self.immigration[local_authorities[migration[0]]] = int(migration[2])
                except:
                    pass
