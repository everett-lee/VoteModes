import requests
import json

TOTAL_MPS = 650

def download_divisions_list():
    params = {'queryParameters.startDate': '2020-01-01'}
    res = requests.get('https://commonsvotes-api.parliament.uk/data/divisions.json/search', params)

    with open('./raw/rawDivsions', 'w') as rawJSon:
        rawJSon.write(res.text)

def what_is_it():
    def has_good_attendance(division):
        return division['AyeCount'] + division['NoCount'] > TOTAL_MPS * 0.8

    def get_fields_of_interest(division):
        return {
            'DivisionId': division['DivisionId'],
            'Date': division['Date'],
            'Title': division['Title']
        }

    with open('./raw/rawDivsions', 'r') as rawJSon:
        res = rawJSon.read()
        raw = json.loads(res)

        with_good_attendance = [div for div in raw if has_good_attendance(div)]
        with_fields_of_interest = [get_fields_of_interest(div) for div in with_good_attendance]
        print(with_fields_of_interest)


def getit():
    what_is_it()