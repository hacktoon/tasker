import requests
import os
from tasker.pipeline import Pipeline, Task


class InfobloxTask(Task):
    def __init__(self, name, function, params={}):
        self.name = name
        self.function = function

    def run(self):
        result = self.function()
        print(f'OK task={self.name}, result={result}')

    def __str__(self):
        return f'task="{self.name}"'


pipeline = Pipeline()  # rename to Pipeline

@pipeline.setup(type=Task)
class PokeApi:
    def __init__(self):
        self.default = 'ditto'

    @pipeline.task(name="GET Ditto")
    def ditto(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.default}'
        ability_name = requests.get(url).json()['abilities'][0]['ability']['name']
        return f'ability: {ability_name}'

    @pipeline.task(name="GET Pikachu")
    def pikachu(self):
        url = f'https://pokeapi.co/api/v2/pokemon/pikachu'
        name = requests.get(url).json()['species']['name']
        return f'name: {name}'

    @pipeline.task(type=Task)
    def read_disc(self):
        return os.listdir('.')


pipeline.run()