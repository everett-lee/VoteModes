import requests
import json

TOTAL_MPS = 650

def download_divisions_list():
    def month_to_str(month):
        if month < 10:
            return "0{month}".format(month=month)
        else:
            return "{month}".format(month=month )

    def get_fields_of_interest(division):
        return {
            'DivisionId': division['DivisionId'],
            'Date': division['Date'],
            'Title': division['Title'],
            'AyeCount': division['AyeCount'],
            'NoCount': division['NoCount']
        }

    with open('./raw/rawDivisions', 'a') as rawJSon:
        rawJSon.write('{data: ')

    divisions = []

    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:

            if month == 1:
                first_open = '2020-{month}-01'.format(month=month_to_str(month))
            else:
                first_open = '2020-{month}-02'.format(month=month_to_str(month))
            first_close = '2020-{month}-10'.format(month=month_to_str(month))

            second_open = '2020-{month}-11'.format(month=month_to_str(month))
            second_close = '2020-{month}-20'.format(month=month_to_str(month))

            third_open = '2020-{month}-21'.format(month=month_to_str(month))
            if month < 12:
                third_close = '2020-{month}-01'.format(month=month_to_str(month+1))
            else:
                third_close = '2020-12-31'

            first_params = {'queryParameters.startDate': first_open, 'queryParameters.endDate': first_close}
            first_third = requests.get('https://commonsvotes-api.parliament.uk/data/divisions.json/search', first_params)
            second_params = {'queryParameters.startDate': second_open, 'queryParameters.endDate': second_close}
            second_third = requests.get('https://commonsvotes-api.parliament.uk/data/divisions.json/search', second_params)
            third_params = {'queryParameters.startDate': third_open, 'queryParameters.endDate': third_close}
            third_third = requests.get('https://commonsvotes-api.parliament.uk/data/divisions.json/search', third_params)

            divisions += [get_fields_of_interest(div) for div in json.loads(first_third.text)]
            divisions += [get_fields_of_interest(div) for div in json.loads(second_third.text)]
            divisions += [get_fields_of_interest(div) for div in json.loads(third_third.text)]

    with open('./raw/rawDivisions', 'a') as rawJSon:
        rawJSon.write(json.dumps(divisions))
        rawJSon.write('}')

    # params = {'queryParameters.startDate': '2020-01-01', 'queryParameters.take': 1000}
    # res = requests.get('https://commonsvotes-api.parliament.uk/data/divisions.json/search', params)
    #
    # with open('./raw/rawDivisions', 'w') as rawJSon:
    #     rawJSon.write(res.text)

def what_is_it():
    def has_good_attendance(division):
        return division['AyeCount'] + division['NoCount'] > TOTAL_MPS * 0.5

    with open('./raw/rawDivisions', 'r') as rawJSon:
        res = rawJSon.read()
        raw = json.loads(res)

        print(len(res))

        with_good_attendance = [div for div in raw if has_good_attendance(div)]


def getit():
    download_divisions_list()
    what_is_it()