import pytest
import os
from tasker.lib.http import HTTPClient
from tasker.pipeline import Pipeline
from tasker.tasks import Task


class HTTPTask(Task):
    def is_valid(self, response):
        return response.valid

    def process_value(self, response):
        return response.url


@pytest.fixture(scope='session')
def good_pokeapi():
    pipeline = Pipeline()
    @pipeline.setup(basetask=HTTPTask)
    class GoodPokeApi:
        def __init__(self, *args, **kwargs):
            self.client = HTTPClient('PokeAPI', 'https://pokeapi.co/api/v2/')
            print(args, kwargs)

        @pipeline.task(name="GET Ditto")
        def ditto(self, prev_result):
            return self.client.get(f'pokemon/ditto')

        @pipeline.task(name="GET Pikachu")
        def pikachu(self, prev_result):
            return self.client.get('pokemon/pikachu')
    return pipeline


@pytest.fixture(scope='session')
def bad_pokeapi():
    pipeline = Pipeline()
    @pipeline.setup(basetask=HTTPTask)
    class BadPokeApi:
        def __init__(self):
            self.client = HTTPClient('PokeAPI', 'https://pokeapi.co/api/v2/')

        @pipeline.task(name="GET Ditto")
        def ditto(self, prev_result):
            return self.client.get(f'pokemon/ditto')

        @pipeline.task(name="GET wrong URL")
        def pikachu(self, prev_result):
            return self.client.get('pokemon/p')

        @pipeline.task(basetask=Task)
        def read_disc(self, prev_result):
            return os.listdir('.')
    return pipeline


@pytest.fixture(scope='session')
def fs_api():
    pipeline = Pipeline()
    @pipeline.setup()
    class FileSystemApi:
        @pipeline.task()
        def read_disc(self, prev_result):
            return os.listdir('.')
    return pipeline