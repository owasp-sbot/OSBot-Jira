from hb_security_jupyter.data_utils.On_Resolve_Card_Color import On_Resolve_Card_Color
from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_jira.api.graph.Jira_Graph_View import Jira_Graph_View
from osbot_jira.api.plantuml.views.Render_Puml__Jira_Graph import Render_Puml__Jira_Graph
from osbot_utils.utils.Misc import unique, date_time_now


class Jira_Graph_Jql:

    def __init__(self, jql = None, jira_graph=None):
        self.jira_graph              = jira_graph or Jira_Graph()
        self.render_puml__jira_graph = None
        self.api_jira                = self.jira_graph.api_jira
        self.issue_fields            = 'issuelinks,summary,issuetype'
        self.jql                     = jql
        self.jql_keys                = []
        self.projects_to_show        = None
        self.status_to_show          = None
        self.skin_params             = {}
        self.depth                   = 1
        self.summary_wrap_at         = 50
        self.link_types              = None
        self.on_resolve_card_color   = None
        self.on_resolve_card_text    = None
        self.title                   = None
        self.footer                  = None
        self.show_project_icons      = False
        self.show_link_types_legend  = False
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

    def filter(self):
        return self.jira_graph.filter()

    def get_jira_graph(self):
        return self.jira_graph

    def set_arrow_font_size(self, value):
        return self.set_skin_param('ArrowFontSize', value)

    def set_card_font_size(self, value):
        return self.set_skin_param('CardFontSize', value)

    def set_depth(self, depth):
        self.depth = depth
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

    def set_title(self, value):
        self.title = f"\\n{value}\\n"
        self.set_skin_param('TitleFontSize', 75)
        self.set_skin_param('TitleFontColor', 'darkblue')
        return self

    def set_title_and_footer(self, title, footer=None):
        self.set_title(title)
        if footer:
            self.set_footer(footer)
        return self

    def set_footer(self, value):
        self.set_skin_param('FooterFontSize', 35)
        self.set_skin_param('FooterFontColor', 'darkblue')
        self.footer = f"\\n\\n{value}\\n"
        return self

    def set_info_footer(self):
        if self.footer is None:
            footer = f"JQL: <b>{self.jql}</b>  |  link_types: <b>{self.link_types}</b>  | depth: <b>{self.depth}</b> \\n # nodes: {len(self.jira_graph.nodes)}  | # edges: {len(self.jira_graph.edges)} | created at: <b>{date_time_now()}</b>"
            self.set_footer(footer)
        return self

    def show_colors__entities(self):
        return self.set_on_resolve_card_color(On_Resolve_Card_Color.for_entities_and_projects_and_nist)

    def filter_projects_to_show(self):
        (self.jira_graph.filter().only_show_issue_types(issue_types=self.projects_to_show)
                                 .only_edges_with_both_nodes())
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

    def reload_issues_with_fields(self, fields=None):
        self.jira_graph.jira_get_nodes_issues(reload=True, fields=fields)
        return self

    def create_jira_graph(self):
        return (self.execute_jql()
                    .set_link_types(self.link_types)
                    .graph_expand(self.depth)
                    .filter_projects_to_show()
                    .filter_status_to_show()
                    .add_link_types_legend())


    def create_png(self):
        return (self.create_jira_graph()
                    .reload_issues_with_fields(self.issue_fields)
                    .set_info_footer()
                    .create_jira_graph_png())

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