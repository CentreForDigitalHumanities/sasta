from sastadev.readmethod import read_method
import pytest


@pytest.mark.parametrize('variant', ['astae', 'astafuture'])
def test_sastadev_queries_variants(asta_method, variant):
    result = read_method(asta_method.category.name.lower(),
                         asta_method.content.path)

    variant_queries = [q.id for q in result.queries.values()
                       if variant in q.variants]
    other_variant_queries = [q.id for q in result.queries.values()
                             if q.variants != [] and variant not in q.variants]

    result_variant = read_method(asta_method.category.name.lower(),
                                 asta_method.content.path, variant=variant)

    assert len(result.queries) != len(result_variant.queries)
    for q in variant_queries:
        assert q in result_variant.queries
    for q in other_variant_queries:
        assert q not in result_variant.queries
