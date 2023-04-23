from requests import get, ConnectionError
import pytest
import csv

TESTED_URL = "https://nominatim.openstreetmap.org/search?format=json"
ROUND_LEVEL = 3


def get_data():
    with open('search_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for el in reader:
            yield el


data = get_data()

@pytest.mark.parametrize('data', data)
def test_search_by_q(data):
    try:
        response = get(TESTED_URL, params={'q': data[0]})
    except ConnectionError:
        print("Проверьте подключение к сети.")
    assert round(
        float(response.json()[0]['lat']), ROUND_LEVEL
        ) == round(float(data[1]), ROUND_LEVEL)
    assert round(
        float(response.json()[0]['lon']), ROUND_LEVEL
        ) == round(float(data[2]), ROUND_LEVEL)
