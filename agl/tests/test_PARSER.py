import unittest
from agl import PARSER

seq = 'tibudogolatupabikutibudodaropipabikudaropigolatutibudopabikutibudogola' \
      'tupabikudaropitibudopabikutibudogolatupabikudaropitibudodaropigolatupa' \
      'bikutibudogolatupabikudaropipabikudaropipabikudaropigolatudaropipabiku' \
      'daropigolatutibudogolatupabikugolatudaropitibudogolatudaropigolatudaro' \
      'pigolatutibudopabikutibudodaropitibudopabikugolatutibudodaropitibudoda' \
      'ropigolatutibudodaropipabikutibudodaropitibudogolatudaropipabikutibudo' \
      'golatutibudopabikudaropigolatutibudopabikudaropipabikugolatutibudodaro' \
      'pipabikudaropipabikutibudogolatudaropitibudodaropigolatudaropitibudoda' \
      'ropigolatutibudodaropipabikugolatupabikugolatupabikutibudodaropipabiku' \
      'tibudopabikugolatupabikutibudodaropigolatudaropitibudogolatudaropigola' \
      'tutibudogolatupabikugolatudaropipabikugolatutibudodaropigolatupabikugo' \
      'latutibudopabikutibudogolatutibudogolatupabikutibudodaropigolatupabiku' \
      'golatupabikudaropigolatudaropipabikutibudodaropitibudopabikutibudogola' \
      'tudaropigolatutibudodaropipabikutibudopabikugolatutibudopabikutibudopa' \
      'bikudaropipabikudaropitibudopabikugolatupabikugolatupabikudaropipabiku' \
      'golatudaropigolatutibudodaropi'

perceptsizes = [1, 2, 3, 2, 1, 3, 2, 3, 1, 2, 3, 2, 2, 3, 1, 3, 3, 2, 3, 1, 1,
                3, 2, 3, 2, 3, 1, 1, 2, 2, 3, 1, 1, 3, 2, 3, 1, 2, 2, 2, 2, 2,
                2, 2, 2, 1, 1, 3, 1, 3, 2, 2, 1, 2, 3, 3, 2, 2, 2, 1, 3, 3, 3,
                3, 1, 2, 1, 1, 3, 2, 1, 3, 1, 2, 3, 1, 2, 2, 3, 3, 2, 1, 1, 1,
                3, 2, 2, 3, 1, 3, 1, 3, 2, 1, 1, 1, 1, 1, 1, 3, 2, 2, 2, 2, 2,
                1, 3, 1, 2, 2, 1, 3, 3, 2, 1, 2, 2, 2, 3, 1, 3, 2, 1, 1, 2, 2,
                3, 2, 2, 2, 3, 3]

# these are the scores by running the seq string above using the original
# PARSER implementation provided by Perruchet.
scores = {
    'budo': 7.819983,
    'daropi': 10.71499,
    'daropipabi': 0.4,
    'golatu': 9.604987,
    'golatudaropigolatutibudo': 0.935,
    'golatupabi': 0.76,
    'golatupabiku': 0.675,
    'golatuti': 1.509995,
    'golatutibudo': 2.165,
    'golatutibudodaropi': 0.07500006,
    'ku': 8.059995,
    'kudaropi': 0.815,
    'kutibudo': 2.174999,
    'pabi': 12.35999,
    'pabiku': 1.655,
    'pabikutibudo': 1.335001,
    'pabikutibudopabiku': 1.080001,
    'pi': 2.654987,
    'ti': 4.324985,
    'tibudo': 0.6349999
}


class TestModel(unittest.TestCase):

    def test_correctscores(self):
        primitives = set([seq[i:i + 2] for i in range(len(seq) - 1)])
        model = PARSER.PARSER(primitives=primitives, readingframe=2)
        model.run(seq, perceptsizes=perceptsizes)
        # next is present with insignificant weight because of small rounding
        # differences between original PARSER and PyPARSER, remove it
        model.perceptshaper.pop('golatudaropi')
        self.assertSetEqual(set(model.perceptshaper.keys()),
                            set(scores.keys()))
        for unit, weight in model.perceptshaper.items():
            self.assertAlmostEqual(weight, scores[unit], delta = 0.001)
