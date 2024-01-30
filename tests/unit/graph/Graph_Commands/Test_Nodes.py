from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_jira.api.graph.Graph_Commands.Nodes import Nodes


class Test_Nodes(Test_Helper):

    def setUp(self):
        super().setUp()
        self.nodes = Nodes()

    def test_update_lambda(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.graph')

    def test_add_edge(self):
        (text, attachments) = self.nodes.add_edge(["graph_WLA","GSP-1", "creates_RISK","GSP-95"])
        #Dev.pprint(text)

    def test_add_node(self):
        (text, attachments) = self.nodes.add_node(["graph_WLA","GSP-1"])
        assert 'added node: `GSP-1` to new graph called ' in text
        assert attachments  == []

    def test_list(self):
        (text, attachments) = self.nodes.list(["graph_WLA"])
        #Dev.pprint(text)


    def test_remove_node(self):
        (text, attachments) = self.nodes.remove_node(["graph_2F8","SOW-129"])
        #Dev.pprint(text)

    def test_remove_link(self):
        (text, attachments) = self.nodes.remove_link(["graph_SHL","is_parent_of,    is_Stakeholder"])
        #Dev.pprint(text)

    # def test_remove_no_links(self):
    #     (text, attachments) = self.nodes.remove_no_links(["graph_GL2"])
    #     Dev.pprint(text)

    def test_stats(self):
        (text, attachments) = self.nodes.stats(["graph_WLA"])
        assert text        == 'Here are the stats for the graph `graph_WLA`'
        assert attachments == [{'text': "*1x Nodes:* \n['GSP-95']"}, {'text': '*0x Edges:* \n[]'}]



    # def test_update_lambda_vis_js(self):
    #     Lambda('lambdas.gsbot.gsbot_graph').update_with_src()