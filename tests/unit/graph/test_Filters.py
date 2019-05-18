from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.api.graph.Filters import Filters
from osbot_jira.api.graph.GS_Graph import GS_Graph


class test_Filters(TestCase):

    def setUp(self):
        self.graph = GS_Graph()
        self.filters = Filters().setup(self.graph)
        self.result  = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert self.filters.graph == self.graph