from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_jira.api.graph.Jira_Graph_View import Jira_Graph_View
from osbot_jira.api.jira_server.local.Jira_Local_Cache import Jira_Local_Cache
from osbot_jira.api.plantuml.views.Render_Puml__Jira_Graph import Render_Puml__Jira_Graph
from osbot_utils.utils.Lists import list_chunks
from osbot_utils.utils.Misc import unique, date_time_now, word_wrap_escaped, list_set


class Jira_Graph_Jql:

    def __init__(self, jql = None, jira_graph=None):
        self.jira_graph               = jira_graph or Jira_Graph()
        self.render_puml__jira_graph  = None
        self.api_jira                 = self.jira_graph.api_jira
        self.issue_fields             = None                         # issues fields data are only reloaded when this value is set
        self.jql                      = jql
        self.jql_keys                 = []
        self.projects_to_show         = None
        self.status_to_show           = None
        self.skin_params              = {}
        self.depth                    = 1
        self.summary_wrap_at          = 50
        self.link_types               = None
        self.link_types_to_ignore     = None
        self.on_resolve_card_color    = None
        self.on_resolve_card_text     = None
        self.title                    = ''
        self.footer                   = None
        self.show_project_icons       = False
        self.show_link_types_legend   = False
        self.footer_font_size         = 35
        self.title_font_size          = 75
        # if root_node:
        #     self.jira_graph.add_node(root_node)
        # if initial_nodes:
        #     self.jira_graph.add_nodes(initial_nodes)
        # if issue_links:
        #     self.jira_graph.set_puml_link_types_to_add(issue_links)
        # if skin_params:
        #     self.jira_graph.set_skin_params(issue_links)
        self.jira_graph.api_jira.log_requests = True

    def add_node(self, key):
        if key:
            self.jira_graph.add_node(key)
        return self

    def delete_node(self, key, delete_edges=False, delete_from_nodes=False, delete_to_nodes=False):
        self.jira_graph.delete_node(key, delete_edges=delete_edges, delete_from_nodes=delete_from_nodes, delete_to_nodes=delete_to_nodes)
        return self

    def execute_jql(self):
        if self.jql:
            self.jql_keys = self.api_jira.search__return_keys(jql=self.jql)
            self.jira_graph.add_nodes(self.jql_keys)
        return self

    def filter(self):
        return self.jira_graph.filter()

    def query(self):
        return self.jira_graph.query()

    def graph_expand(self, depth=1):
        self.jira_graph.add_all_linked_issues(depth=depth)
        self.jira_graph.get_nodes_issues()                 # see if we need to do this
        return self

    def render_png(self):
        return self.jira_graph.render_puml_and_save_tmp(use_lambda=False)

    def render_png__schema(self):
        jira_graph_view = Jira_Graph_View(jira_graph=self.jira_graph)
        schema_graph = jira_graph_view.create_schema_graph()
        schema_graph.set_skin_param('linetype', 'polyline')  # ortho
        schema_graph.render_puml_and_save_tmp(use_lambda=False)
        return schema_graph


    def get_jira_graph(self):
        return self.jira_graph

    def get_issues(self):
        return self.jira_graph.issues

    def get_edges(self):
        return self.jira_graph.edges

    def get_edges_count(self):
        return len(self.get_edges())

    def get_nodes(self):
        return self.jira_graph.nodes

    def get_nodes_count(self):
        return len(self.get_nodes())

    def set_arrow_font_size(self, value):
        return self.set_skin_param('ArrowFontSize', value)

    def set_card_font_size(self, value):
        return self.set_skin_param('CardFontSize', value)

    def set_edge_font_size(self, value):
        return self.set_skin_param('ArrowFontSize', value)

    def set_footer_font_size(self, value):
        self.footer_font_size = value
        return self

    def set_title_font_size(self, value):
        self.title_font_size = value
        return self

    def set_title_and_footer_font_size(self, value):
        self.set_title_font_size(value)
        self.set_footer_font_size(value)
        return self

    def set_depth(self, depth):
        self.depth = depth
        return self

    def set_issue_fields(self, fields):
        self.issue_fields = fields
        return self

    def set_jql(self, jql):
        self.jql = jql
        return self

    def set_jira_graph(self, jira_graph):
        self.jira_graph = jira_graph
        return self

    def set_link_types(self, link_types=None):
        self.link_types = link_types
        self.jira_graph.set_puml_link_types_to_add(link_types)
        return self

    def set_link_types_to_ignore(self, link_types):
        self.link_types_to_ignore = link_types
        self.jira_graph.set_puml_link_types_to_ignore(link_types)
        return self

    def set_png_dpi(self, dpi):
        return self.set_skin_param('dpi', dpi)

    def set_projects_to_ignore(self,projects_to_ignore):
        self.jira_graph.set_puml_projects_to_ignore(projects_to_ignore)
        return self

    def set_skin_param(self, name, value):
        self.skin_params[name] = value
        return self

    def set_linetype_ortho(self):
        return self.set_skin_param('linetype', 'ortho')

    def set_linetype_polyline(self):
        return self.set_skin_param('linetype', 'polyline')

    def set_projects_to_show(self, projects_to_show=None):
        self.projects_to_show = projects_to_show
        return self

    def set_status_to_show(self, status_to_show=None):
        self.status_to_show = status_to_show
        return self

    def set_show_link_types_legend(self, value=True):
        self.show_link_types_legend = value
        return self

    def set_show_project_icons(self, value=True):
        self.show_project_icons = value
        return self

    def set_summary_wrap_at(self, value):
        self.summary_wrap_at = value
        return self

    def set_on_resolve_card_color(self, on_resolve_card_color):
        self.on_resolve_card_color = on_resolve_card_color
        return self

    def set_on_resolve_card_text(self, on_resolve_card_text):
        self.on_resolve_card_text = on_resolve_card_text
        return self

    def set_issues(self, issues):
        self.jira_graph.issues = issues
        return self

    def set_title(self, value):
        self.title = f"\\n{value}\\n"
        self.set_skin_param('TitleFontSize', self.title_font_size)
        self.set_skin_param('TitleFontColor', 'darkblue')
        return self

    def set_title_and_footer(self, title, footer=None):
        self.set_title(title)
        if footer:
            self.set_footer(footer)
        return self

    def set_footer(self, value):
        self.set_skin_param('FooterFontSize', self.footer_font_size)
        self.set_skin_param('FooterFontColor', 'darkblue')
        self.footer = f"\\n\\n{value}\\n"
        return self

    def set_info_footer(self):
        if self.footer is None:
            footer = ''
            if self.jql:
                footer = f"JQL: <b>{self.jql}</b>  |  "
            if self.link_types:
                footer += f"Link types to follow: <b>{self.link_types}</b>  |  "
            if self.link_types_to_ignore:
                footer += f"Link types to Ignore: "
                for chunk in list_chunks(self.link_types_to_ignore, 3):
                    print(chunk)
                    footer += f"<b>{chunk}</b> \\n"
                footer += ' | '
            footer += f"depth: <b>{self.depth}</b> | # nodes: <b>{len(self.jira_graph.nodes)}</b>  | # edges: <b>{len(self.jira_graph.edges)}</b> | created at: <b>{date_time_now()}</b>"
            self.set_footer(footer)
        return self

    def filter_projects_to_show(self):
        self.jira_graph.filter().only_show_issue_types(issue_types=self.projects_to_show)
                                 #.only_edges_with_both_nodes())
        return self

    def filter_status_to_show(self):
        self.jira_graph.filter().only_with_field_equal_to('Status', self.status_to_show)
        return self

    def add_link_types_legend(self):
        if self.show_link_types_legend:
            all_link_types = []
            for from_id, link_type, to_id in self.jira_graph.edges:
                all_link_types.append(link_type)

            unique_link_types = unique(all_link_types)
            legend_text = "\tlegend top left\n" + \
                          f"\t\t={len(unique_link_types)} unique links types in Graph\n\n"
            for link_type in unique_link_types:
                legend_text += f"\t\t\t {link_type}\n"
            legend_text += "\tendlegend"
            self.jira_graph.extra_puml_lines += legend_text
        return self

    def add_nodes(self, keys):
        self.jira_graph.add_nodes(keys)
        return self

    def reload_issues_with_fields(self):
        if self.issue_fields:                   # only reload if this field is set, note that when running with live queries this will have some performance implications for large number of nodes
            self.jira_graph.jira_get_nodes_issues(reload=True, fields=self.issue_fields)
        return self

    def render_jira_graph(self):
        return (self.execute_jql()
                    .set_link_types(self.link_types)
                    .graph_expand(self.depth)
                    .filter_projects_to_show()
                    .filter_status_to_show()
                    .add_link_types_legend())


    def render_and_create_png(self, create_png=True):
        self.render_jira_graph()
        if create_png:
            (self.reload_issues_with_fields()
                 .set_info_footer()
                 .create_jira_graph_png())
        return self

    def create_jira_graph_png(self):
        self.render_puml__jira_graph = (Render_Puml__Jira_Graph(self.jira_graph))
        (self.render_puml__jira_graph.set_skin_params(self.skin_params)
                                     .set_on_resolve_card_color(self.on_resolve_card_color)
                                     .set_on_resolve_card_text(self.on_resolve_card_text)
                                     .set_show_project_icons(self.show_project_icons)
                                     .set_summary_wrap_at(self.summary_wrap_at)
                                     .set_title(self.title)
                                     .set_footer(self.footer)
                                     .render()
                                     .save_as_png())
        return self

    def print_nodes_edges_count(self):
        print("******* Nodes and Edges count for current Jira Graph *********")
        print(f"{self.get_nodes_count()} nodes | {self.get_edges_count()} edges")
        return self


    def use_cache(self, value=True):
        if value:
            cached_issues = Jira_Local_Cache().all_issues(index_by='Key')
            self.set_issues(cached_issues)
        return self

