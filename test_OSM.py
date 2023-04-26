from requests import get, ConnectionError
import pytest
import csv
import logging
import allure

TESTED_URL = "https://nominatim.openstreetmap.org/search"
TESTED_URL_REVERSE = "https://nominatim.openstreetmap.org/reverse"
ROUND_LEVEL = 3
logger = logging.getLogger(__name__)


def get_data(file):
    '''Чтение входных данных из файла'''
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for el in reader:
            yield el


data = get_data('search_data.csv')
data_structured = get_data('search_data_structured.csv')
data_reverse = get_data('reverse_data.csv')


@allure.step('Отправка запроса на сервер')
def connection(tested_url, params):
    '''Отправка запроса на сервер'''
    response = get(tested_url, params=params)
    return response


@allure.title("Search_by_q_param")
@pytest.mark.parametrize('data', data)
def test_search_by_q(data):
    '''Проверка эндпоинта search с параметром поиска в свободной форме'''
    params = {
                'q': data[0],
                'format': 'json'
             }
    try:
        response = connection(TESTED_URL, params)
    except ConnectionError as error:
        logger.error(error)
    else:
        logger.info('Соединение установлено')
    with allure.step("Проверяю, что широта соответствует ожидаемой"):
        assert round(
            float(response.json()[0]['lat']), ROUND_LEVEL
            ) == round(float(data[1]), ROUND_LEVEL)
    with allure.step("Проверяю, что долгота соответствует ожидаемой"):
        assert round(
            float(response.json()[0]['lon']), ROUND_LEVEL
            ) == round(float(data[2]), ROUND_LEVEL)


@allure.title("Search_by_structured_params")
@pytest.mark.parametrize('data_structured', data_structured)
def test_search_by_params(data_structured):
    '''Проверка эндпоинта search со структурировынным запросом'''
    params = {
        'street': data_structured[0],
        'city': data_structured[1],
        'county': data_structured[2],
        'state': data_structured[3],
        'country': data_structured[4],
        'postalcode': data_structured[5],
        'format': 'json'
    }
    try:
        response = connection(TESTED_URL, params)
    except ConnectionError as error:
        logger.error(error)
    else:
        logger.info('Соединение установлено')
    with allure.step("Проверяю, что широта соответствует ожидаемой"):
        assert round(
            float(response.json()[0]['lat']), ROUND_LEVEL
            ) == round(float(data_structured[6]), ROUND_LEVEL)
    with allure.step("Проверяю, что долгота соответствует ожидаемой"):
        assert round(
            float(response.json()[0]['lon']), ROUND_LEVEL
            ) == round(float(data_structured[7]), ROUND_LEVEL)


@allure.title("Reverse_search")
@pytest.mark.parametrize('data_reverse', data_reverse)
def test_reverse(data_reverse):
    '''Проверка эндпоинта reverse'''
    params = {
        'lat': data_reverse[4],
        'lon': data_reverse[5],
        'format': 'json',
        'details': 1
    }
    try:
        response = connection(TESTED_URL_REVERSE, params)
    except ConnectionError as error:
        logger.error(error)
    else:
        logger.info('Соединение установлено')
    if 'house_number' in response.json()['address']:
        with allure.step("Проверяю, что номер дома соответствует ожидаемому"):
            assert data_reverse[0] == (
                response.json()['address']['house_number']
            )
    if 'road' in response.json()['address']:
        with allure.step("Проверяю, что улица соответствует ожидаемой"):
            assert data_reverse[1].lower() in (
                response.json()['address']['road'].lower()
            )
    if 'city' in response.json()['address']:
        with allure.step("Проверяю, что город соответствует ожидаемому"):
            assert data_reverse[2].lower() in (
                response.json()['address']['city'].lower()
            )
    elif 'town' in response.json()['address']:
        with allure.step("Проверяю, что номер дома соответствует ожидаемому"):
            assert data_reverse[2].lower() in (
                response.json()['address']['town'].lower()
            )
    with allure.step("Проверяю, что страна соответствует ожидаемой"):
        assert data_reverse[3].lower() in (
            response.json()['address']['country'].lower()
        )
