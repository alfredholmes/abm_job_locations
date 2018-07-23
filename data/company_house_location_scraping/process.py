import csv, requests, json
from requests.auth import HTTPBasicAuth

company_numbers = []

print('Loading data...')

with open('CompanyNumbers.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        company_numbers.append(line[0])

print('Done')

company_addresses = {}

#Get current company address

for s in company_numbers:
    filing_history = json.loads(requests.get('https://api.companieshouse.gov.uk/company/' + s + '/filing-history', auth=('evHt9MOd08fueWenYhMHXCf5SFO98vSiKuP-66tI', '')).text)['items']
    for d in filing_history:
        if d['category'] == 'address':
            print(d)
#find changes of address
