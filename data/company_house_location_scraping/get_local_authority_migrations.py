import csv, requests, json, time, random
import re

# TODO: Clean up Code
# TODO: Some filing histories > 100 items are not handeled well
# TODO: Errors with employee counting

post_code_regex = r'([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))\s?[0-9][A-Za-z]{2})'


def get_post_code_from_address(address, regex):
    matches = re.search(regex, address)
    try:
        return matches.group(0)
    except:
        return None

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
companies = []
errors = []

#Get current company address
r = 0
last_request = 0
for s in company_numbers:
    #preventing calling the .gov.uk api too many times
    if last_request != 0 and 0.5 - (time.time() - last_request) > 0:
        #time.sleep(0.5 - (time.time() - last_request))
        pass
    try:
        req = requests.get('https://api.companieshouse.gov.uk/company/' + s + '/filing-history', data={'items_per_page': 1000}, auth=('evHt9MOd08fueWenYhMHXCf5SFO98vSiKuP-66tI', ''))
        if req.status_code != 200:
            errors.append(['Error with companies house API request for company ' + s, req.status_code])
            continue

    except:
        errors.append(['Unknown error with companies house api ' + s])
        continue

    filing_history = json.loads(req.text)
    last_request = time.time()
    r += 1
    print(r)
    if 'items' in filing_history:
        fh = filing_history['items']
        movement_data = [] # array with reverse chronological list of [postcode, leaving_date]
        staff = 0 #company registered with director, perhaps
        try:
            j = 0

            for d in fh:
                if j == 0:
                    alive = 'gazette' not in d['category']

                j = j+1
                if d['category'] == 'address':
                    if 'old_address' in d['description_values'] and 'new_address' in d['description_values']:
                        #add the current address to the post code if haven't already
                        if len(movement_data) == 0:
                            new_post_code = get_post_code_from_address(d['description_values']['new_address'], post_code_regex)
                            if new_post_code != None:
                                movement_data.append([new_post_code])
                        #then add previous address

                        old_post_code = get_post_code_from_address(d['description_values']['new_address'], post_code_regex)
                        if old_post_code != None:
                            movement_data.append([old_post_code, d['date'], j, staff])
                        else:
                            errors.append(['Problem parsing address', old_address])
                    elif len(movement_data) > 0 and d['description'] == 'legacy' and 'office' in d['description_values']['description']:
                        old_address = d['description_values']['description']
                        old_post_code = get_post_code_from_address(old_address, post_code_regex)
                        if old_post_code != None:
                            movement_data.append([old_post_code, d['date'], j, staff])
                        else:
                            errors.append(['Problem parsing address', old_address])
                    elif d['description'] == 'legacy' and 'office' in d['description_values']['description']:
                        #find current post code
                        if last_request != 0 and 0.5 - (time.time() - last_request) > 0:
                            time.sleep(0.5 - (time.time() - last_request))
                        last_request = time.time()
                        # TODO: Catch errors that could come from here
                        address = json.loads(requests.get('https://api.companieshouse.gov.uk/company/' + s + '/registered-office-address', auth=('evHt9MOd08fueWenYhMHXCf5SFO98vSiKuP-66tI', '')).text)
                        old_address = d['description_values']['description']
                        old_post_code = get_post_code_from_address(old_address, post_code_regex)
                        if old_post_code != None:
                            movement_data.append([address['postal_code']])
                            movement_data.append([old_post_code, d['date'], j, staff])
                        else:
                            errors.append(['Problem parsing address', old_address])
                if d['category'] == 'officers':
                    if d['description'] != 'legacy':
                        if d['subcategory'] == 'appointments':
                            staff += 1
                        if d['subcategory'] == 'termination':
                            staff -= 1
                    else:
                        if 'New' in d['description_values']['description'] or 'new' in d['description_values']['description'] or 'appointed' in d['description_values']['description'] or 'Appointed' in d['description_values']['description']:
                            staff += 1
                        elif 'resigned' in d['description_values']['description'] or 'terminated' in d['description_values']['description']:
                            staff -= 1
            #process the data to find the local authority
            if len(movement_data) > 0:
                data = json.loads(requests.post('http://api.postcodes.io/postcodes', data={'postcodes': [a[0] for a in movement_data]}).text)
                for i in range(1, len(movement_data)):
                    try:
                        destination_la = data['result'][i - 1]['result']['codes']['admin_district']
                        departure_la   = data['result'][i]['result']['codes']['admin_district']
                        date = movement_data[i][1]
                        if destination_la != departure_la:
                            moves.append([departure_la, destination_la, date, len(fh) - movement_data[i][2], staff + 1 - movement_data[i][3]])
                    except:
                        if data['result'][i]['result'] == None and data['result'][i - 1]['result'] != None:
                            errors.append(['Error finding local authority for company ' + s, data['result'][i]])
                            data['result'][i] = data['result'][i - 1]
                        else:
                            errors.append(['Error finding local authority for company ' + s, data['result'][i -1]])
            companies.append([s, alive, staff, len(fh)])
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

        with open('company_info.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for company in companies:
                writer.writerow(company)
        companies = []
#find changes of address
