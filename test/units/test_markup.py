import nose
from ansibledocgen.formatter.markup import MarkupFormatter
import unittest
import sys
import os


class TestMarkup(unittest.TestCase):

    def test_all(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        projectunit = os.path.join(localdir, "../integration/projectunit")
        # TODO
