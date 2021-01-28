import pytest


def test_run_count(good_pokeapi):
    result = good_pokeapi.run()
    assert len(result) == 2


def test_run_values(good_pokeapi):
    result = good_pokeapi.run()
    assert result[0].value == 'https://pokeapi.co/api/v2/pokemon/ditto'


def test_run_results(good_pokeapi):
    result = good_pokeapi.run()
    values = result.values()
    assert values[0] == 'https://pokeapi.co/api/v2/pokemon/ditto'
    assert values[1] == 'https://pokeapi.co/api/v2/pokemon/pikachu'


def test_run_bad_pipeline_length(bad_pokeapi):
    result = bad_pokeapi.run()
    assert len(result) == 1  # one test was successful
    assert not result


def test_bad_pipeline_failed_results(bad_pokeapi):
    result = bad_pokeapi.run()
    failed = result.failed()[-1]
    assert not failed.status
    assert failed.value.url == 'https://pokeapi.co/api/v2/pokemon/p'


def test_filesystem(fs_api):
    result = fs_api.run()
    assert result


def test_value_chain_sum(previous_sum_pipeline):
    result = previous_sum_pipeline.run()
    assert bool(result)
    assert result.values() == [1, 3, 6]