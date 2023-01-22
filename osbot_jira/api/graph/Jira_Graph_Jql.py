from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_jira.api.graph.Jira_Graph_View import Jira_Graph_View
from osbot_jira.api.jira_server.local.Jira_Local_Cache import Jira_Local_Cache
from osbot_jira.api.plantuml.views.Render_Puml__Jira_Graph import Render_Puml__Jira_Graph
from osbot_utils.utils.Json import json_dumps
from osbot_utils.utils.Lists import list_chunks
from osbot_utils.utils.Misc import unique, date_time_now, word_wrap_escaped, list_set


class Jira_Graph_Jql:

    def __init__(self, jql = None, jira_graph=None):
        self.jira_graph                   = jira_graph or Jira_Graph()
        self.render_puml__jira_graph      = None
        self.api_jira                     = self.jira_graph.api_jira
        self.issue_fields                 = None                         # issues fields data are only reloaded when this value is set
        self.jql                          = jql
        self.jql_keys                     = []
        self.projects_to_show             = None
        self.status_to_show               = None
        self.skin_params                  = {}
        self.depth                        = 1
        self.summary_wrap_at              = 50
        self.link_types                   = None
        self.link_types_to_ignore         = None
        self.keys_to_ignore               = None
        self.on_resolve_card_color        = None
        self.on_resolve_card_text         = None
        self.title                        = ''
        self.footer                       = None
        self.show_project_icons           = False
        self.show_link_types_legend       = False
        self.show_link_types_as_notes     = False
        self.show_summary_in_notes        = False
        self.show_existing_edges_in_notes = False
        self.link_types_as_notes_position = 'bottom'  # bottom, top, left, right
        self.footer_font_size             = 35
        self.title_font_size              = 75
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

    def disable_jira_requests(self):
        self.api_jira.disable_requests()
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

    def get_issues(self, just_nodes_issues=True):
        if just_nodes_issues:
            return self.jira_graph.get_nodes_issues()
        return self.jira_graph.issues or {}

    def get_issue(self, issue_id, just_nodes_issues=True):
        if just_nodes_issues:
            if issue_id not in self.get_nodes():
                return {}
        return self.jira_graph.issues.get(issue_id, {})

    def get_edges(self):
        return self.jira_graph.edges

    def get_edges_count(self):
        return len(self.get_edges())

    def get_nodes(self):
        return self.jira_graph.nodes

    def get_nodes_count(self):
        return len(self.get_nodes())

    def issue(self, issue_id, just_nodes_issues=True):
        return self.get_issue(issue_id, just_nodes_issues=just_nodes_issues)

    def issue__linked_issues(self, issue_id, link_type=None,just_nodes_issues=True):
        linked_issues = self.issue(issue_id,just_nodes_issues=just_nodes_issues).get('Issue Links', {})
        if link_type:
            return linked_issues.get(link_type)
        return linked_issues

    def issues(self, issues_ids, just_nodes_issues=True):
        issues_data = {}
        if issues_ids:
            for issue_id in issues_ids:
                issues_data[issue_id] = self.issue(issue_id,just_nodes_issues=just_nodes_issues)
        return issues_data

    def show_links(self, show_links_as_notes=True, show_existing_edges_in_notes=False, show_summary_in_notes=False):
        self.set_show_links_as_notes         (show_links_as_notes         )
        self.set_show_existing_edges_in_notes(show_existing_edges_in_notes)
        self.set_show_summary_in_notes       (show_summary_in_notes       )

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

    def set_keys_to_ignore(self, keys_to_ignore):
        self.keys_to_ignore = keys_to_ignore
        self.jira_graph.set_puml_keys_to_ignore(keys_to_ignore)
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

    def set_show_links_as_notes(self, value=True):
        self.show_link_types_as_notes = value
        return self

    def set_show_summary_in_notes(self, value=True):
        self.show_summary_in_notes = value
        return self

    def set_show_existing_edges_in_notes(self, value=True):
        self.show_existing_edges_in_notes = value
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

    def set_title_and_footer(self, title=None, footer=None):
        if title:
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
                footer += f"Link types to follow: "
                for chunk in list_chunks(self.link_types, 12):
                    #print(chunk)
                    footer += f"<b>{chunk}</b> \\n"

                #footer += f"Link types to follow: <b>{self.link_types}</b>  |  "
            if self.link_types_to_ignore:
                footer += f"Link types to Ignore: "
                for chunk in list_chunks(self.link_types_to_ignore, 3):
                    #print(chunk)
                    footer += f"<b>{chunk}</b> \\n"
                footer += ' | '
            if self.keys_to_ignore:
                footer += f"Keys to ignore: <b>{self.keys_to_ignore}</b>  \\n  "
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

    def add_link_types_as_notes(self):
        issues = self.get_issues(just_nodes_issues=False)
        edges  = self.jira_graph.edges
        if self.show_link_types_as_notes:
            self.jira_graph.notes.clear()  # removes previous notes
            for link_key, node in self.jira_graph.get_nodes_issues().items():
                key_id           = link_key.replace('-', '_')    # fix key to PlantUml ID
                issue_links      = node.get('Issue Links')
                notes_text = ""
                for link_type, keys in issue_links.items():
                    link_type_text = ""
                    for key in keys:
                        if self.show_existing_edges_in_notes is False:
                            edge = (link_key, link_type, key)
                            if edge in edges:
                                continue
                        link_type_text += f"\t- {key}"
                        if self.show_summary_in_notes:
                            issue = issues.get(key,{})
                            summary = issue.get('Summary','')
                            link_type_text += f" - {summary}"
                        link_type_text += "\n"
                    if link_type_text != "":
                        notes_text += f"\n={link_type}\n{link_type_text}\n"
                if notes_text != "":
                    self.jira_graph.notes.append((self.link_types_as_notes_position, key_id, notes_text))

    def add_link_types_legend(self):
        if self.show_link_types_legend:
            link_types_in_edges = []
            link_types_not_used = []

            legend_text = "\tlegend top left\n"

            #link_types_in_edges
            for _, link_type, _ in self.jira_graph.edges:
                link_types_in_edges.append(link_type)
            link_types_in_edges = unique(link_types_in_edges)

            legend_text += f"\t\t={len(link_types_in_edges)} link types used\n\n"

            for link_type in unique(link_types_in_edges):
                legend_text += f"\t\t\t {link_type}\n"

            #link_types_not_used
            for key, node in self.jira_graph.get_nodes_issues().items():
                for issue_link in node.get('Issue Links'):
                    if issue_link not in link_types_in_edges:
                        link_types_not_used.append(issue_link)

            link_types_not_used = unique(link_types_not_used)

            legend_text += f"\n\t\t={len(link_types_not_used)} link types NOT used\n\n"

            for link_type in unique(link_types_not_used):
                legend_text += f"\t\t\t {link_type}\n"

            legend_text += "\tendlegend\n"
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
                    .add_link_types_legend()
                    .add_link_types_as_notes())


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


    def puml_code(self):
        return self.jira_graph.get_puml()

    def use_cache(self, value=True):
        if value:
            cached_issues = Jira_Local_Cache().all_issues(index_by='Key')
            self.set_issues(cached_issues)
        return self

    # def export_to_csv(self, root_key):
    #     edges    = self.query().edges_from_id(root_key)
    #     headers  = ['key']
    #     headers.extend(list_set(edges))
    #     cells    = []
    #     csv_data = [headers, cells]
    #     for link_type, values in edges.items():
    #         row = {'key': root_key }
    #         for value in values:
    #             row[link_type] = value
    #         #print(row)
    #
    #     import csv
    #     from osbot_utils.utils.Csv import load_csv_from_iterable
    #     return load_csv_from_iterable(cells)
    #     csv_reader = csv.DictReader(csv_data, delimiter=',')
    #     return csv_reader