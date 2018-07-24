import csv, requests, json, time, random
import re

post_code_regex = r'([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))\s?[0-9][A-Za-z]{2})'

company_numbers = []

print('Loading data...')

with open('Company_Numbers_2012-2018.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        company_numbers.append(line[0])


#shuffle company numbers to get random sample
#random.shuffle(company_numbers)

print('Done')

company_addresses = {}
moves = []
errors = []

#Get current company address
r = 0
last_request = 0
for s in company_numbers:
    #preventing calling the .gov.uk api too many times
    if last_request != 0 and 0.5 - (time.time() - last_request) > 0:
        time.sleep(0.5 - (time.time() - last_request))

    last_request = time.time()

    filing_history = json.loads(requests.get('https://api.companieshouse.gov.uk/company/' + s + '/filing-history', data={'items_per_page': 1000}, auth=('evHt9MOd08fueWenYhMHXCf5SFO98vSiKuP-66tI', '')).text)
    r += 1
    print(r)
    #print(filing_history)
    if 'items' in filing_history:
        fh = filing_history['items']
        movement_data = [] # array with reverse chronological list of [postcode, leaving_date]
        staff = 0
        try:
            for d in fh:
                if d['category'] == 'address':
                    if 'old_address' in d['description_values'] and 'new_address' in d['description_values']:
                        #add the current address to the post code
                        if len(movement_data) == 0:
                            new_post_code = re.search(post_code_regex, d['description_values']['new_address']).group(0)
                            movement_data.append([new_post_code])
                        #then add previous address
                        old_post_code = re.search(post_code_regex, d['description_values']['old_address']).group(0)
                        movement_data.append([old_post_code, d['date']])
                    elif d['description'] == 'legacy' and len(movement_data) > 0:
                        old_address = d['description_values']['description']
                        old_post_code = re.search(post_code_regex, old_address).group(0)
                        movement_data.append([old_post_code, d['date']])
                    elif d['description'] == 'legacy':
                        #find current post code
                        if last_request != 0 and 0.5 - (time.time() - last_request) > 0:
                            time.sleep(0.5 - (time.time() - last_request))
                        last_request = time.time()
                        address = json.loads(requests.get('https://api.companieshouse.gov.uk/company/' + s + '/registered-office-address', auth=('evHt9MOd08fueWenYhMHXCf5SFO98vSiKuP-66tI', '')).text)
                        old_address = d['description_values']['description']
                        old_post_code = re.search(post_code_regex, old_address).group(0)
                        movement_data.append([address['postal_code']])
                        movement_data.append([old_post_code, d['date']])
                if d['category'] == 'officers':
                    if d['description'] != 'legacy':
                        if d['subcategory'] == 'appointments':
                            staff += 1
                        if d['subcategory'] == 'termination':
                            staff -= 1
                    else:
                        if 'New' in d['description_values']:
                            staff += 1
                        if 'resigned' in d['description_values'] or 'terminated' in d['description_values']:
                            staff -= 1

            #process the data to find the local authority
            if len(movement_data) > 0:
                data = json.loads(requests.post('http://api.postcodes.io/postcodes', data={'postcodes': [a[0] for a in movement_data]}).text)
                try:
                    for i in range(1, len(movement_data)):
                        destination_la = data['result'][i - 1]['result']['codes']['admin_district']
                        departure_la   = data['result'][i]['result']['codes']['admin_district']
                        date = movement_data[i][1]
                        moves.append([departure_la, destination_la, date, len(fh), staff])
                except:
                    errors.append(['Error finding local authority: ', data, d])
        except:
            errors.append(['Error with company ' + s, d])

    if r % 100 == 0:
        #append moeves to file
        with open('district_moves.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for line in moves:
                writer.writerow(line)
        moves = []
        with open('error_log.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for error in errors:
                writer.writerow(error)
        errors = []
#find changes of address
