from requests import get, ConnectionError
import pytest
import csv
import logging

TESTED_URL = "https://nominatim.openstreetmap.org/search?format=json"
ROUND_LEVEL = 3
logger = logging.getLogger(__name__)


def get_data(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for el in reader:
            yield el


data = get_data('search_data.csv')
data_structured = get_data('search_data_structured.csv')

@pytest.mark.parametrize('data', data)
def test_search_by_q(data):
    '''Проверка эндпоинта search с параметром поиска в свободной форме'''
    try:
        response = get(TESTED_URL, params={'q': data[0]})
    except ConnectionError as error:
        logger.error(error)
    assert round(
        float(response.json()[0]['lat']), ROUND_LEVEL
        ) == round(float(data[1]), ROUND_LEVEL)
    assert round(
        float(response.json()[0]['lon']), ROUND_LEVEL
        ) == round(float(data[2]), ROUND_LEVEL)


@pytest.mark.parametrize('data_structured', data_structured)
def test_search_by_params(data_structured):
    '''Проверка эндпоинта search со структурировынным запросом'''
    params = {
        'street': data_structured[0],
        'city': data_structured[1],
        'county': data_structured[2],
        'state': data_structured[3],
        'country': data_structured[4],
        'postalcode': data_structured[5]
    }
    try:
        response = get(TESTED_URL, params=params)
    except ConnectionError as error:
        logger.error(error)
    assert round(
        float(response.json()[0]['lat']), ROUND_LEVEL
        ) == round(float(data_structured[6]), ROUND_LEVEL)
    assert round(
        float(response.json()[0]['lon']), ROUND_LEVEL
        ) == round(float(data_structured[7]), ROUND_LEVEL)
