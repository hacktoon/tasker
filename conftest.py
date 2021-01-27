import pytest
import requests
import os
from tasker.pipeline import Pipeline
from tasker.tasks import Task


class HTTPTask(Task):
    def is_valid(self, response):
        return response.status_code < 400

    def process_value(self, response):
        return response.url


_good_pokeapi = Pipeline()
@_good_pokeapi.setup(basetask=HTTPTask)
class GoodPokeApi:
    def __init__(self):
        self.default = 'ditto'

    @_good_pokeapi.task(name="GET Ditto")
    def ditto(self, prev_result):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.default}'
        return requests.get(url)

    @_good_pokeapi.task(name="GET Pikachu")
    def pikachu(self, prev_result):
        url = f'https://pokeapi.co/api/v2/pokemon/pikachu'
        return requests.get(url)

    @_good_pokeapi.task(basetask=Task)
    def read_disc(self, prev_result):
        return os.listdir('.')


@pytest.fixture()
def good_pokeapi():
    return _good_pokeapi