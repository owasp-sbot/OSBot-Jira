import json
import unittest
from unittest        import TestCase
from osbot_jira.api.graph.GS_Graph import GS_Graph
from osbot_utils.utils.Dev import Dev


class Test_GS_Graph(TestCase):

    def setUp(self):
        self.graph  = GS_Graph()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_add_node(self):
        self.graph.add_node('a')
        assert self.graph.nodes == ['a']

    def test_add_linked_issues_of_type(self):
        self.graph.add_node('SEC-9195')
        self.graph.add_linked_issues_of_types([
                      'is parent of'        ,
                      'supports RISK'       ,
                      'creates RISK'        ,
                      'is Vulnerability of' ,
                      'creates R2'          ,
                      'creates R1'          ,
                      'has Stakeholder'     ])

        self.graph.render_puml()
        self.graph.puml.save_tmp()
        #self.graph.save('/tmp/graph-sec-9195.json')
        #print(self.graph.puml.puml)

        # self.graph.puml.add_line("scale 2.25")

        # self.graph.puml.add_line("\tscale 2024 height   \n")
        #self.graph.puml.add_line('skinparam handwritten true')

    # def test_add_all_linked_issues(self):
    #     keys = ['RISK-1494']
    #     (self.graph.set_links_path_mode_to_down()
    #                .set_puml_show_key_in_text  (True)
    #                #.set_puml_only_from_projects(['RISK', 'VULN'])
    #                .set_puml_width             (4000)
    #                #.set_puml_height            (6000)
    #                .add_all_linked_issues      (keys, 5)
    #                #.add_link_types_as_nodes(self.graph.risk_links_paths_down)
    #                .render_puml_and_save_tmp   ()
    #      )
    #
    #     Dev.pprint(len(self.graph.nodes))
    #     Dev.pprint(len(self.graph.edges))

    def test_add_all_linked_issues____with_color_coding_on_rating(self):

        issues = None

        def on_add_node(element,title, id, original_id):
            key = id.replace('_', '-')
            issue = issues.get(key)
            color = '#FFFFFF'
            if issue:
                rating = issue['Rating']
                if   rating == 'High'    : color = '#F37071'
                elif rating == 'Medium'  : color = '#F0BF99'
                elif rating == 'Low'     : color = '#78999D'
                elif rating == 'TBD'     : color = '#F7A4A4'

            node_puml = '{0} "<color:#000000>{1}</color>" as {2} {3}'.format(element, title, id, color)
            return node_puml
        self.graph.puml.on_add_node = on_add_node

        self.graph.puml.add_line("\tscale 3024 width   \n")
        keys = ['RISK-1610'] # ['GSP-95'] # 'FACT-47', #
        (
            self.graph.set_puml_left_to_right   (True )
                      .set_puml_only_from_projects(['RISK','VULN'])
                      .set_puml_show_key_in_text(False)
                      .set_puml_show_edge_labels(False)
                      .add_all_linked_issues(keys, 2)
        )
        issues = self.graph.get_nodes_issues()

        self.graph.render_puml()
        self.graph.puml.save_tmp()

        Dev.pprint(len(self.graph.nodes))
        Dev.pprint(len(self.graph.edges))

        #self.graph.render_puml_and_save_tmp()

    def test_add_all_linked_issues____with___risk_links_paths_down(self):
        issues = None

        def on_add_node(element,title,id, original_id):
            key = id.replace('_', '-')
            issue = issues.get(key)
            color = '#FFFFFF'
            if issue:
                status = issue['Status']
                if   status in ['Blocked', 'Backlog']             : color = '#F37071'
                elif status in ['To VULN Assess' , 'To Validate'] : color = '#F0BF99'
                elif status == 'Allocated for Fix'                : color = '#78999D'
                elif status == 'Fixed'                            : color = '#6DD1A3'

            node_puml = '{0} "<color:#000000>{1}</color>" as {2} {3}'.format(element, title, id, color)
            return node_puml
        self.graph.puml.on_add_node = on_add_node

        keys = ['IA-333']#['RISK-1526'] #['RISK-1610']  # ['GSP-95'] # 'FACT-47', #
        graph = self.graph
        #self.risk_links_paths_down
        (graph #.set_puml_node_edge_value("Status")
              .set_puml_link_types_to_add(graph.risk_links_paths_down)
              .set_puml_show_key_in_text(False)
              .add_all_linked_issues(keys, 4))

        issues = self.graph.get_nodes_issues()

        graph.render_puml_and_save_tmp()
        Dev.pprint(len(graph.nodes))
        Dev.pprint(len(graph.edges))

    def test_add_all_linked_issues____with___risk_links_paths_up(self):
        keys = ['SEC-8708'] #['RISK-1610']  # ['GSP-95'] # 'FACT-47', #
        graph = self.graph
        #self.risk_links_paths_down
        (graph#.set_puml_node_edge_value(None)
              .set_puml_link_types_to_add(graph.risk_links_paths_up)
              .add_all_linked_issues(keys, 5))
        graph.render_puml_and_save_tmp()

        #self.graph.add_link_types_as_nodes()


        Dev.pprint(len(graph.nodes))
        Dev.pprint(len(graph.edges))

    @unittest.skip("needs fixing the ES index")
    def test_add_all_linked_issues____IT_Assets(self):
        it_systems = self.graph.api_issues.elastic().search_using_lucene_index_by_id('Issue\ Type: "IT Assets"')
        keys       = list(it_systems.keys())[0:20]
        self.graph.set_puml_width(5000)
        self.graph.set_link_types_from_issues(it_systems)
        self.graph.set_puml_link_types_to_add(['has to be done after'])

        self.graph.add_all_linked_issues(keys, 1)
        self.graph.render_puml_and_save_tmp()

        return

    def test_add_link_types_as_nodes____GitHub(self):

        self.graph.add_node('IA-333')
        self.graph.add_linked_issues_of_types(['is Vulnerable to', 'has Stakeholder'])
        self.graph.add_link_types_as_nodes()
        self.graph.render_puml_and_save_tmp()

        return


    # def test_edges__link_types(self):
    #     self.graph.add_all_linked_issues( ['RISK-1610'], 2)
    #     result = self.graph.get_unique_link_types()
    #     #Dev.pprint(result)
    #     assert len(result) == 22



    def test_graph(self):
        self.result = self.graph.add_node('aaa').graph().nodes()


    def test_remove_with_links(self):

        (self.graph  .add_node("RISK-424")
                     .add_node("ID-42")
                     .add_node("ID-41")
                     .add_edge("RISK-424", '', "ID-42")
                     .add_edge("RISK-424", '', "ID-7"))

        Dev.pprint(self.graph.nodes)
        Dev.pprint(self.graph.edges)
        self.graph.remove_with_links()
        Dev.pprint(self.graph.nodes)
        Dev.pprint(self.graph.edges)



    def test_save(self):
        (self.graph .add_node("RISK-424")
                    .add_node("ID-42")
                    .add_edge("RISK-424", '', "ID-42")
                    .add_edge("RISK-424", '', "ID-7"))
        file         = self.graph.save()
        loaded_graph = GS_Graph()
        loaded_graph.load(file)
        assert loaded_graph.nodes            == self.graph.nodes
        assert len(loaded_graph.edges)       == len(self.graph.edges)
        assert self.graph.render_puml().puml == loaded_graph.render_puml().puml
        #loaded_graph.puml.save_tmp()

    #### use cases

    def test____create_org_chart_everybody(self):
        is_a_manager_nodes = self.graph.all_link_types('it_assets')['is manager of'].keys()
        self.graph.add_nodes(is_a_manager_nodes)
        self.graph.add_linked_issues_of_type('is manager of')

        self.graph.render_puml()
        self.graph.puml.save_tmp()


    def test____load_and_render_left_to_right(self):
        file = '/tmp/graph-sec-9195.json'
        graph = GS_Graph().load(file)
        graph.puml_options['left-to-right'] = True
        graph.render_puml()
        graph.puml.save_tmp()

    def test____create_stakeholder_graph_from_security_story(self):

        #from gs_elk.API_Jira_Diagrams import API_Jira_Diagrams
        #graph = API_Jira_Diagrams().risks_story_mixed_orders_v2__puml()

        file = '/tmp/graph-sec-9195.json'
        graph = GS_Graph().load(file)

        issue_types_path = ['is Stakeholder',
                            'is created by R2',
                            'is created by R3',
                            'is created by R4',
                            'is created by VULN',
                            'is Vulnerability of',
                            'RISK supported by',
                            'risk reduced by',
                            'is child of',
                            'is fixed by']
        start_node ='SEC-8651'
        self.graph.create_sub_graph_from_start_node(graph.nodes, start_node, issue_types_path)
        self.graph.add_link_types_as_nodes()
        self.graph.puml.save_tmp()

    def test__create_graph_with_epic_data__top_level_okrs_up(self):
        graph = self.graph
        (graph.add_all_linked_issues(['GSOKR-924'])
              .add_nodes_from_epics()
              .set_link_paths_to_ignore(['is child of', 'has Stakeholder'])
              .set_links_path_mode_to_up()
              .add_all_linked_issues(depth=3)
             )
        graph.render_puml_and_save_tmp()

    def test__create_graph_with_epic_data__top_level_okrs_down(self):
        graph = self.graph
        (graph.add_all_linked_issues(['GSOKR-924'])
              .add_nodes_from_epics()
              .set_links_path_mode_to_up()
              .set_link_paths_to_ignore(['is child of', 'has Stakeholder'])
              .set_links_path_mode_to_up()
              .add_all_linked_issues(depth=4)
             )
        graph.render_puml_and_save_tmp()

    def test__create_graph_for_epic_SEC_8694(self):
        graph = self.graph
        (graph.add_all_linked_issues(['SEC-8694'])
             .add_nodes_from_epics()
             .set_links_path_mode_to_up()
             .add_all_linked_issues(depth=2)
        )
        graph.render_puml_and_save_tmp()



    def test__create_graph_with_epic_data__sec_9195(self):
        graph = self.graph

        #Dev.pprint(self.graph.api_issues.epic_issues('SEC-9195'))
        #return
        (graph.add_all_linked_issues(['GSOKR-924'])
              .add_nodes_from_epics()
              .set_link_paths_to_ignore(['is child of', 'has Stakeholder'])
              .set_links_path_mode_to_up()
              .add_all_linked_issues(depth=3)
             )
        Dev.pprint(len(graph.nodes))
        graph.render_puml_and_save_tmp()


    # def test__create_graph_with_epic_data__assignee(self):
    #     keys = ['SEC-9696']
    #     graph = self.graph
    #     (graph  .set_links_path_mode_to_down()
    #             .add_all_linked_issues(keys, 1)
    #             .add_nodes_from_epics()
    #             .add_all_linked_issues()
    #             .set_puml_node_text_value('Assignee')
    #     )
    #     self.graph.render_puml()
    #     self.graph.puml.save_tmp()
    #
    #     #graph.render_puml_and_save_tmp()
    #
    #     API_Slack('DDKUZTK6X').puml_to_slack(graph.puml.puml)


    def test__create_graph_with_up_down_data(self):
        keys = ['SEC-9696']

        graph = self.graph
        (graph  # .set_puml_node_edge_value(None)
                .set_puml_link_types_to_add(graph.risk_links_paths_down)
                .add_all_linked_issues(keys, 1))
        graph.render_puml_and_save_tmp()


    def test__create_graph_with_up_down_data(self):
        keys = ['IA-386']
        graph = self.graph
        (graph
                .set_puml_link_types_to_add(["is parent of"])
                .add_all_linked_issues(keys, 2)     # was 6
                .set_puml_direction_top_down()
         )
        graph.render_puml_and_save_tmp()

    def tests_expand_link_types_to_add(self):

        self.graph.set_puml_link_types_to_add(['risks_up','stakeholders_up'])     \
                  .expand_link_types_to_add()

    def test__create_graph_with_special_link_types(self):
        keys = ['RISK-1494']

        graph = self.graph
        (graph  # .set_puml_node_edge_value(None)
                .set_puml_link_types_to_add(['risks_down'])
                .add_all_linked_issues(keys, 5))
        graph.render_puml_and_save_tmp()
        #Dev.pprint(result)


    def test_to_json__from_json(self):
        graph = self.graph
        graph.add_nodes(['abc','xyz','123']).add_edges([('abc','', 'xyz'),('abc','','123')])
        graph.create_params = ['in','unit test']

        assert json.loads(graph.to_json()) == {   'create_params': ['in','unit test'],
                                                  'edges': [['abc', '', 'xyz'], ['abc', '', '123']],
                                                  'node_type': {},
                                                  'nodes': ['abc', 'xyz', '123'],
                                                  'notes': [],
                                                  'puml_config': True,
                                                  'puml_options': { 'height': None,
                                                                    'left-to-right': True,
                                                                    'link-types-to-add': [],
                                                                    'link-types-to-ignore': [],
                                                                    'node-text-value': 'Summary',
                                                                    'only-from-projects': [],
                                                                    'show-edge-labels': True,
                                                                    'show-key-in-text': True,
                                                                    'width': None},
                                                  'skin_params': []}
        assert json.loads(graph.to_json(puml_config=False)) == { 'edges': [['abc', '', 'xyz'], ['abc', '', '123']],
                                                                 'nodes': ['abc', 'xyz', '123']}

        graph_json = graph.to_json()
        new_graph = GS_Graph().from_json(graph_json)

        new_graph_json = new_graph.to_json()
        assert graph_json == new_graph_json
        assert graph_json != GS_Graph().to_json()

        assert GS_Graph().from_json(graph.to_json(puml_config=False)).nodes == ['abc', 'xyz', '123']

    def test_to_json__from_json__store_issues(self):

        graph = self.graph
        graph.add_nodes(['RISK-12', 'RISK-24', 'RISK-1084']).add_edges([('RISK-12', '', 'RISK-24'), ('RISK-12', '', 'RISK-1084')])

        graph_json = graph.to_json(store_issues=True)
        assert set(json.loads(graph_json).get('issues')) == {'RISK-12', 'RISK-24', 'RISK-1084'}
        assert set(GS_Graph().from_json(graph_json).issues) == {'RISK-12', 'RISK-24', 'RISK-1084'}
