import csv, requests, json, time
from requests.auth import HTTPBasicAuth
import re

post_code_regex = r'([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))\s?[0-9][A-Za-z]{2})'

company_numbers = []

print('Loading data...')

with open('CompanyNumbers.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        company_numbers.append(line[0])

print('Done')

company_addresses = {}
moves = []

#Get current company address
r = 0
last_request = 0
for s in company_numbers:
    #preventing calling the .gov.uk api too many times
    if last_request != 0 and 0.5 - (time.time() - last_request) > 0:
        time.sleep(0.5 - (time.time() - last_request))
    last_request = time.time()

    filing_history = json.loads(requests.get('https://api.companieshouse.gov.uk/company/' + s + '/filing-history', auth=('evHt9MOd08fueWenYhMHXCf5SFO98vSiKuP-66tI', '')).text)
    r += 1
    print(r)
    if 'items' in filing_history:
        fh = filing_history['items']
        for d in fh:
            if d['category'] == 'address':
                if 'old_address' in d['description_values'] and 'new_address' in d['description_values']:
                    try:

                        old_address = d['description_values']['old_address']
                        new_address = d['description_values']['new_address']

                        old_post_code = re.search(post_code_regex, old_address).group(0)
                        new_post_code = re.search(post_code_regex, new_address).group(0)

                        #find local authority areas using the postcode.io api
                        data = json.loads(requests.post('http://api.postcodes.io/postcodes', data={'postcodes': [old_post_code, new_post_code]}).text)



                        old_district = data['result'][0]['result']['codes']['admin_district']
                        new_district = data['result'][1]['result']['codes']['admin_district']
                        date = d['action_date']

                        if old_district != new_district:
                            moves.append([old_district, new_district, date])
                    except:
                        pass


    if r % 100 == 0:
        with open('district_moves.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for line in moves:
                writer.writerow(line)

        moves = []
#find changes of address
