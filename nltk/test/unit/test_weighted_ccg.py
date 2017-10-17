from __future__ import absolute_import
import unittest

from nltk.ccg import chart, lexicon


class TestMultipleSemanticForms(unittest.TestCase):

    lex = lexicon.fromstring(r"""
:- NN, DET

DET :: NN/NN

the => DET {\x.unique(x)}
dog => NN {'dog'}
dog => NN {'cat'}""", include_semantics=True)

    def test_parse(self):
        # Lexicon has two entries for 'dog'. (TODO: verify to be thorough)

        # Try a parse. Do the two senses get through to different
        # candidate parses?
        parser = chart.CCGChartParser(self.lex, chart.DefaultRuleSet)
        results = list(parser.parse("the dog".split()))

        self.assertEquals(len(results), 2)

        leaf_semantics = [str(result.pos()[1][1].semantics())
                          for result in results]
        self.assertEquals(set(leaf_semantics), set(["'dog'", "'cat'"]))
