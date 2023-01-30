from unittest import TestCase

from osbot_jira.api.graph.Jira_Graph_Jql import Jira_Graph_Jql
from osbot_jira.api.graph.Jira_Graph_Subset import Jira_Graph_Subset
from osbot_jira.api.jira_server.local.Jira_Local_Cache import Jira_Local_Cache
from osbot_utils.utils.Dev import pprint


class test_Jira_Graph_Subset(TestCase):

    def setUp(self):
        print()
        self.jira_graph_jql = Jira_Graph_Jql().use_cache()
        #self.jira_graph_jql.disable_jira_requests()
        self.jira_graph_subset = self.jira_graph_jql.create_jira_graph_subset()
        self.root_key   = 'PERSON-5' # Dinis
        self.issues_ids = [self.root_key]
        self.link_types = ['has activity', 'delivers','is key result of', 'is objective of', 'is project of','is programme of']
        self.depth      = 10
        self.jira_graph_jql.add_linked_issues_for_nodes_and_link_types(issues_ids=self.issues_ids,link_types=self.link_types, depth=self.depth)

    def test_create(self):
        self.jira_graph_jql.print_nodes_edges_count()
        self.jira_graph_jql.create_jira_graph_png()

        #self.jira_graph_subset.create().render_and_create_png(self.root_key , depth=10)
        #self.jira_graph_subset.create().render_and_create_png('ACTIVITY-76' , depth=10)
        #self.jira_graph_subset.create().render_and_create_png('KEYRESULT-333', depth=10)
        #self.jira_graph_subset.create().render_and_create_png('PROJ-170', depth=10)

        # self.jira_graph_subset.create()
        # with self.jira_graph_subset.jira_graph_jql as _:
        #     _.add_linked_issues_for_node_and_link_types(issue_id='ACTIVITY-73',link_type='delivers', depth=2)
        #     _.create_jira_graph_png()

        #self.jira_graph_subset.create().render_and_create_png('PROG-29', depth=10)
        #return
        self.jira_graph_subset.create()
        with self.jira_graph_subset.jira_graph_jql as _:
            depth      = 7
            issue_id   = 'PROG-7'
            link_types = ['has programme', 'has project', 'has objective', 'has key result', 'is delivered by','has activity']
            #link_types = None
            _.add_linked_issues_for_node_and_link_types(issue_id=issue_id,link_types=link_types, depth=depth)
            _.create_jira_graph_png()





