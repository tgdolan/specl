"""Hypothesis strategies used to generate data for specl tests."""
from hypothesis.strategies import characters, composite, integers, lists, sampled_from, text
from hypothesis.extra import pandas as hpd

from hypothesis.extra.pandas import columns, data_frames, column, range_indexes

# names = text(
#     characters(max_codepoint=1000, blacklist_categories=('Cc', 'Cs')),
#     min_size=1).map(lambda s: s.strip()).filter(lambda s: len(s) > 0)

names = text(alphabet=list('abcdefghijklmnopqrstuvwxyz'), min_size=1)

a_b_dataframe = data_frames([column('A', dtype=int), column('B', dtype=float)], index=range_indexes(min_size=2))


@composite
def gen_rando_dataframe(draw, elements=names):
    column_names = draw(lists(elements, min_size=1, unique=True))
    return draw(hpd.data_frames(hpd.columns(column_names, elements=elements),
                         index=hpd.range_indexes(min_size=5)))

@composite
def gen_columns_and_subset(draw, elements=names):
    column_names = draw(lists(elements, min_size=1, unique=True))
    num_columns_to_keep = draw(integers(min_value=1, max_value=len(column_names)))
    i = num_columns_to_keep
    columns_to_keep = set()
    while i > 0:
        keeper_column = draw(integers(min_value=0, max_value=len(column_names) - 1))
        columns_to_keep.add(column_names[keeper_column])
        i = i - 1

    # With column data and 'keeper' columns selected, utilize draw to return
    # a hypothesis DataFrame column strategies defined.
    return draw(hpd.data_frames(hpd.columns(column_names, elements=elements),
                                index=hpd.range_indexes(min_size=5))), columns_to_keep
