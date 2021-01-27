import pytest


def test_run_count(good_pokeapi):
    results = good_pokeapi.run()
    assert len(results) == 3


def test_run_values(good_pokeapi):
    results = good_pokeapi.run()
    assert results[0] == 'https://pokeapi.co/api/v2/pokemon/ditto'