import pytest
import os
from tasker.lib.http import HTTPClient
from tasker.pipeline import pipeline, task
from tasker.tasks import Task


class HTTPTask(Task):
    def is_valid(self, response):
        return response.valid

    def process_value(self, response):
        return response.url


@pytest.fixture(scope='session')
def good_pokeapi():
    @pipeline(model=HTTPTask)
    class GoodPokeApi:
        def __init__(self, *args, **kwargs):
            self.http = HTTPClient('PokeAPI', 'https://pokeapi.co/api/v2/')

        @task(name="GET Ditto")
        def ditto(self, prev_result):
            return self.http.get(f'pokemon/ditto')

        @task(name="GET Pikachu")
        def pikachu(self, prev_result):
            return self.http.get('pokemon/pikachu')
    return GoodPokeApi()


@pytest.fixture(scope='session')
def bad_pokeapi():
    @pipeline(model=HTTPTask)
    class BadPokeApi:
        def __init__(self):
            self.http = HTTPClient('PokeAPI', 'https://pokeapi.co/api/v2/')

        @task(name="GET Ditto")
        def ditto(self, prev_result):
            return self.http.get(f'pokemon/ditto')

        @task(name="GET wrong URL")
        def pikachu(self, prev_result):
            return self.http.get('pokemon/p')

        @task(model=Task)
        def read_disc(self, prev_result):
            return os.listdir('.')
    return BadPokeApi()


@pytest.fixture(scope='session')
def fs_api():
    @pipeline()
    class FileSystemApi:
        @task()
        def read_disc(self, prev_result):
            return os.listdir('.')
    return FileSystemApi()