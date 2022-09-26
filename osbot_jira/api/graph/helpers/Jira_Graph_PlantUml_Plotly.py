from hb_security_jupyter.network_graphs.Network_Graph_For_Jira_Graph import Network_Graph_For_Jira_Graph
from osbot_jira.api.graph.Jira_Graph_Jql import Jira_Graph_Jql
from osbot_jira.api.jira_server.local.Jira_Local_Cache import Jira_Local_Cache


class Jira_Graph_PlantUml_Plotly:

    def __init__(self, on_init=False, key=None, jql=None, link_types=None, depth=None, title=None, nx_iterations=None, nx_show_text= False, create_png=True):
        self.jira_graph_jql = Jira_Graph_Jql()
        self.plotly_graph   = Network_Graph_For_Jira_Graph(jira_graph_jql=self.jira_graph_jql)
        self.key            = key
        self.jql            = jql
        self.link_types     = link_types
        self.depth          = depth
        self.title          = title
        self.create_png     = create_png
        self.nx_node_field  = 'Project'
        self.nx_show_text   = nx_show_text
        self.nx_iterations  = nx_iterations
        if on_init:
            on_init(self)

    def set_title           (self, value): self.title           = value; return self
    def set_depth           (self, value): self.depth           = value; return self
    def set_jql             (self, value): self.jql             = value; return self
    def set_key             (self, value): self.key             = value; return self
    def set_create_png      (self, value): self.create_png      = value; return self
    def set_nx_node_field   (self, value): self.nx_node_field   = value; return self
    def set_nx_show_text    (self, value): self.nx_show_text    = value; return self
    def set_nx_iterations   (self, value): self.nx_iterations   = value; return self

    def use_jira_cache(self, value=True):
        if value:
            cached_issues = Jira_Local_Cache().all_issues(index_by='Key')
            self.jira_graph_jql.set_issues(cached_issues)
        return self

    # .set_issue_fields('issuelinks,summary,issuetype,status,project')
    def render_images(self):
        (self.jira_graph_jql.set_title            (self.title       )
                            .set_depth            (self.depth       )
                            .set_jql              (self.jql         )
                            .add_nodes            (self.key         )
                            .set_link_types       (self.link_types  )
                            .render_and_create_png(self.create_png ))

        (self.plotly_graph.set_node_text_field      (self.nx_node_field)
                          .set_title                (self.title)
                          .show_nodes_and_edges_text(self.nx_show_text)
                          .create_networkx_graph    ()
                          .set_layout_iterations    (self.nx_iterations)
                          .create_jpg_from_graph    ())

        return self
