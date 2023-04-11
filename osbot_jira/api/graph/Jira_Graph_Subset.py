class Jira_Graph_Subset:


    def __init__(self, jira_graph):
        self.jira_graph          = jira_graph
        self.jira_graph_jql      = None
        self.key                 = None
        self.title               = None
        self.link_types          = None
        self.png_create          = True
        self.depth               = 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.render(title      = self.title      ,
                    link_types = self.link_types ,
                    key        = self.key        ,
                    depth      = self.depth      )
        if self.png_create:
            self.create_png()


    def create(self):
        from osbot_jira.api.graph.Jira_Graph_Jql import Jira_Graph_Jql  # to deal with circular dependencies

        nodes_issues        = self.jira_graph.get_nodes_issues()
        self.jira_graph_jql = Jira_Graph_Jql()
        with self.jira_graph_jql as _:
            _.set_issues            (nodes_issues)
            _.set_enable_jira_calls (False       )
            _.set_only_link_if_issue(True        )
        return self

    def create_png(self):
        self.jira_graph_jql.create_jira_graph_png()
        return self

    def issues(self, just_nodes_issues=False):
        return self.jira_graph_jql.get_issues(just_nodes_issues=just_nodes_issues)

    def nodes(self):
        return self.jira_graph_jql.get_nodes()

    def render(self, title=None, key=None, keys=None, project=None, link_types=None, depth=1):
        with self.jira_graph_jql as _:
            _.set_link_types   (link_types)
            _.set_depth        (depth     )
            _.add_node         (key       )
            _.add_nodes        (keys      )
            _.add_project      (project   )
            _.set_title        (title     )
            _.render_jira_graph()
        return self

    def show_all_links(self, value=True):
        self.jira_graph_jql.set_only_link_if_issue(not value)
        return self


    def render_and_create_png(self, **kwargs):
        self.render(**kwargs)
        self.create_png()
        return self

    def set_key(self, value):
        self.key = value
        return self

    def set_link_types(self, value):
        self.link_types = value
        return self

    def set_depth(self, value):
        self.depth = value
        return self