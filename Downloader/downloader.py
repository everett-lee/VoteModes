import requests
import json

TOTAL_MPS = 650

def has_good_attendance(division):
    return division['ayes'] + division['noes'] > TOTAL_MPS * 0.8

def download_divisions_list():
    params = {'queryParameters.startDate': '2020-01-01'}
    res = requests.get('https://commonsvotes-api.parliament.uk/data/divisions.json/search', params)

    with open('./raw/rawDivsions', 'w') as rawJSon:
        rawJSon.write(res.text)

def what_is_it():
    with open('./raw/rawDivsions', 'r') as rawJSon:
        res = rawJSon.read()
        raw = json.loads(res)

        print(len(raw))
        with_good_attendance = [div for div in raw if has_good_attendance(div)]
        print(len(with_good_attendance))


def getit():
    what_is_it()