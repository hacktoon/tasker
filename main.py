import requests
import os
from tasker.pipeline import Pipeline, Task


class HTTPTask(Task):
    def is_valid(self, response):
        # print(response)
        return response.status_code < 400

    def process_value(self, response):
        return response.url


pipeline = Pipeline()
@pipeline.setup(basetask=HTTPTask)
class PokeApi:
    def __init__(self):
        self.default = 'ditto'

    @pipeline.task(name="GET Ditto")
    def ditto(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.default}'
        return requests.get(url)

    @pipeline.task(name="GET Pikachu")
    def pikachu(self):
        url = f'https://pokeapi.co/api/v2/pokemon/pikachu'
        return requests.get(url)

    @pipeline.task(basetask=Task)
    def read_disc(self):
        return os.listdir('.')


print(pipeline.run())