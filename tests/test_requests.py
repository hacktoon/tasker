import pytest


def test_run_count(good_pokeapi):
    results = good_pokeapi.run()
    assert len(results) == 2


def test_run_values(good_pokeapi):
    results = good_pokeapi.run()
    assert results[0].value == 'https://pokeapi.co/api/v2/pokemon/ditto'


def test_run_results(good_pokeapi):
    results = good_pokeapi.run()
    values = results.values()
    assert values[0] == 'https://pokeapi.co/api/v2/pokemon/ditto'
    assert values[1] == 'https://pokeapi.co/api/v2/pokemon/pikachu'