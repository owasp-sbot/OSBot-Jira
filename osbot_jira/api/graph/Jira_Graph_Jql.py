from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_jira.api.graph.Jira_Graph_View import Jira_Graph_View
from osbot_jira.api.plantuml.views.Render_Puml__Jira_Graph import Render_Puml__Jira_Graph


class Jira_Graph_Jql:

    #def __init__(self, root_node, initial_nodes, issue_links=None, skin_params=None):
    def __init__(self, jql):
        self.jira_graph       = Jira_Graph()
        self.api_jira         = self.jira_graph.api_jira
        self.jql              = jql
        self.jql_keys         = []
        self.projects_to_show = None
        self.status_to_show   = None
        self.skin_params      = {}
        self.depth            = 1
        self.link_types       = None
        # if root_node:
        #     self.jira_graph.add_node(root_node)
        # if initial_nodes:
        #     self.jira_graph.add_nodes(initial_nodes)
        # if issue_links:
        #     self.jira_graph.set_puml_link_types_to_add(issue_links)
        # if skin_params:
        #     self.jira_graph.set_skin_params(issue_links)

    def execute_jql(self):
        if self.jql:
            self.jql_keys = self.api_jira.search__return_keys(jql=self.jql)
            self.jira_graph.add_nodes(self.jql_keys)
        return self

    def graph_expand(self, depth):
        self.jira_graph.add_all_linked_issues(depth=depth)
        self.jira_graph.get_nodes_issues()                 # see if we need to do this
        return self

    def render_png(self):
        return self.jira_graph.render_puml_and_save_tmp(use_lambda=False)

    def render_png__schema(self):
        jira_graph_view = Jira_Graph_View(jira_graph=self.jira_graph)
        schema_graph = jira_graph_view.create_schema_graph()
        #schema_graph.set_puml_left_to_right(False)
        schema_graph.set_skin_param('linetype', 'polyline')
        #schema_graph.set_skin_param('linetype', 'ortho')
        schema_graph.render_puml_and_save_tmp(use_lambda=False)
        return schema_graph

    def set_depth(self, depth):
        self.depth = depth
        return self

    def set_link_types(self, link_types=None):
        if link_types:
            self.jira_graph.set_puml_link_types_to_add(link_types)
        return self

    def set_linetype_polyline(self):
        self.skin_params['linetype'] = 'polyline'
        return self

    def set_projects_to_show(self, projects_to_show=None):
        self.projects_to_show = projects_to_show
        return self

    def set_status_to_show(self, status_to_show=None):
        self.status_to_show = status_to_show
        return self

    def filter_projects_to_show(self):
        (self.jira_graph.filter().only_show_issue_types(issue_types=self.projects_to_show)
                                 .only_edges_with_both_nodes())
        return self

    def filter_status_to_show(self):
        self.jira_graph.filter().only_with_field_equal_to('Status', self.status_to_show)
        return self

    def create_png(self):
        (
            self.execute_jql()
                .set_link_types(self.link_types)
                .graph_expand(self.depth)
                .filter_projects_to_show()
                .filter_status_to_show()
                #.render_png()
        )
        (Render_Puml__Jira_Graph(self.jira_graph)
                    .set_skin_params(self.skin_params)
                    .render()
                    .save_as_png())
        return self