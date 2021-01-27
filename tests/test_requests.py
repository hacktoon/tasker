import pytest


def test_run_count(good_pokeapi):
    ppl_result = good_pokeapi.run()
    assert len(ppl_result) == 2


def test_run_values(good_pokeapi):
    ppl_result = good_pokeapi.run()
    assert ppl_result[0].value == 'https://pokeapi.co/api/v2/pokemon/ditto'


def test_run_results(good_pokeapi):
    ppl_result = good_pokeapi.run()
    values = ppl_result.values()
    assert values[0] == 'https://pokeapi.co/api/v2/pokemon/ditto'
    assert values[1] == 'https://pokeapi.co/api/v2/pokemon/pikachu'


def test_run_bad_pipeline_length(bad_pokeapi):
    ppl_result = bad_pokeapi.run()
    assert len(ppl_result) == 1  # one test was successful
    assert not ppl_result


def test_bad_pipeline_failed_results(bad_pokeapi):
    ppl_result = bad_pokeapi.run()
    failed = ppl_result.failed()[-1]
    assert not failed.status
    assert failed.value.url == 'https://pokeapi.co/api/v2/pokemon/p'