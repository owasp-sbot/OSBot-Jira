import json

from pbx_gs_python_utils.utils.Lambdas_Helpers  import slack_message

from osbot_jira.api.graph.GS_Graph              import GS_Graph
from osbot_jira.api.graph.Lambda_Graph          import Lambda_Graph


class Graph_View:

    def __init__(self,):
        self.graph      = None
        self.lambda_graph   = Lambda_Graph()

    def handle_lambda_request(self, params, slack_channel=None,team_id=None):
        if len(params) == 1:
            graph_name = params.pop()
            self.load_graph(graph_name).render_simple()

        if len(params) > 1:
            graph_name = params[0]
            view_name  = params[1]
            self.load_graph(graph_name)
            if self.graph is None:
                slack_message(":red_circle: in Graph View, graph not found: `{0}`".format(graph_name), [], slack_channel)
            else:
                self.render_view(view_name, slack_channel,team_id, graph_name)
        return self.graph

    def render_view(self, view_name, slack_channel=None, team_id=None,graph_name=None):
        if self.graph:
            try:
                method_name  = "view_{0}".format(view_name)
                method       = getattr(Graph_View,method_name)
                try:
                    if slack_channel:
                        slack_message("Generating view `{0}` for graph with `{1}` nodes and `{2}` edges".format(view_name, len(self.graph.nodes),  len(self.graph.edges)), [], slack_channel, team_id)
                    method(self)
                    if slack_channel:
                        saved_graph = Lambda_Graph().save_gs_graph(self.graph, None, "{0} - {0}".format(view_name, graph_name), slack_channel)
                        slack_message("Saved view `{0}` as new graph `{1}`".format(view_name,saved_graph) , [],slack_channel, team_id)
                except Exception as error:
                    slack_message(":red_circle: Error executing view `{0}`".format(view_name) ,
                                  [{"text": "{0}".format(error)}], slack_channel,team_id)
            except Exception:
               slack_message(":red_circle: view not found: `{0}`".format(view_name) , [], slack_channel,team_id)
               slack_message(self.bad_params_message(), [], slack_channel,team_id)
        return self


    def bad_params_message(self):
        message    =  ":red_circle: For the `graph` `view` command, you need to provide a view name, current options are: \n"
        view_names = [func for func in dir(Graph_View) if callable(getattr(Graph_View, func)) and func.startswith("view")]

        for view_name in view_names:
            message += "            • {0} \n".format(view_name.replace('view_', ''))
            
        return message



    def load_graph(self, graph_name):
        self.graph = self.lambda_graph.get_gs_graph___by_name(graph_name)
        if self.graph:
            self.graph.reset_puml()
        return self

    def print_puml(self):
        print(self.graph.puml.puml)
        return self




    # These are the views available (just create a method and it will be available for use)

    def view_default(self):
        self.graph.render_puml()
        return self

    def view_by_issue_type(self):

        issues = self.graph.get_nodes_issues()

        self.graph.puml.add_line('left to right direction')

        for key,issue in issues.items():
            if issue:
                summary    = issue.get('Summary')
                issue_type = issue.get('Issue Type')
                self.graph.puml.add_card(issue_type,issue_type)
                self.graph.puml.add_card(summary, key)

                self.graph.puml.add_edge(issue_type, key)

        self.graph.puml.enduml()
        return self

    def view_by_labels(self):

        issues = self.graph.get_nodes_issues()

        self.graph.puml.add_line('left to right direction')

        for key,issue in issues.items():
            if issue:
                for label in issue.get('Labels'):
                    summary    = issue.get('Summary')
                    #issue_type = issue.get('Issue Type')
                    #self.graph.puml.add_card(label,label)

                    self.graph.puml.add_card(summary, key)

                    self.graph.puml.add_edge(label, key)
                    #Dev.pprint(issue.get('Labels'))

        self.graph.puml.enduml()
        return self

    def view_by_status(self):

        issues = self.graph.get_nodes_issues()

        self.graph.puml.add_line('left to right direction')

        anchors = []
        edges   = []
        for key,issue in issues.items():
            if issue:
                    summary    = issue.get('Summary')

                    #summary   = Misc.word_wrap_escaped(summary,30)
                    status     = issue.get('Status')

                    self.graph.puml.add_card (summary, key)
                    edges.append((status, key))
                    anchors.append(status)

        for anchor in list(set(anchors)):
            self.graph.puml.add_cloud(anchor, anchor)

        for edge in edges:
            self.graph.puml.add_edge(edge[0], edge[1])
        self.graph.puml.enduml()
        return self

    def view_top_down(self): 
        (
                self.graph
                    .set_puml_direction_top_down()
                    .set_puml_show_key_in_text(False)
                    .set_puml_show_edge_labels(False)
                    .set_skin_param('Padding'             , 10      )
                    .set_skin_param('DefaultFontSize'     , 40      )
                    .set_skin_param('DefaultFontColor'    , 'white' )
                    .set_skin_param('CardBorderColor'     , 'white' )
                    .set_skin_param('CardBackgroundColor' , '175B73')
                    .set_skin_param('CardBorderThickness' , 0       )
                    .set_skin_param('Shadowing'           , False   )
                    .render_puml()
         )
        return self

    def view_links(self):

        def on_add_node(element,title,id, original_id):
            issue       = self.graph.issues.get(original_id)
            if issue:
                issue_links = json.dumps(issue.get('Issue Links'), indent=4)
                self.graph.notes.append(('right', id, issue_links))
                return '{0} "{1} \\n \\n {2}" as {3}'.format(element,title, original_id, id)

        #self.graph.puml.on_add_node = on_add_node
        #self.graph.nodes = [self.graph.nodes.pop()]
        #self.graph.edges = []
        (
            self.graph
                .set_puml_show_key_in_text(False)
                .set_puml_on_add_node(on_add_node)
                .render_puml()
        )
        return self

    def view_no_keys(self):
        (
            self.graph
                .set_puml_show_key_in_text(False)
                .set_puml_show_edge_labels(False)
                .set_skin_param('Padding', '4')
                .set_skin_param('ArrowColor','DarkGray')
                .render_puml()
        )
        return self

    def view_schema(self):

        issues = self.graph.get_nodes_issues()
        schema = {}
        puml = self.graph.puml
        for edge in self.graph.edges:
            if issues[edge[0]]:
                from_issue_type = puml.fix_id(issues[edge[0]].get('Issue Type'))
            else:
                from_issue_type = 'NA'
            link_name       = edge[1]
            if issues[edge[2]]:
                to_issue_type   = puml.fix_id(issues[edge[2]].get('Issue Type'))
            else:
                to_issue_type = 'NA'
            schema_edge = (from_issue_type,link_name,to_issue_type)
            if schema.get(schema_edge) is None: schema[schema_edge] = { 'count'           : 0               ,
                                                                        'from_issue_type' : from_issue_type ,
                                                                        'link_name'       : link_name       ,
                                                                        'to_issue_type'   : to_issue_type }
            schema.get(schema_edge)['count'] += 1

        new_graph = GS_Graph()
        for item in schema.values():
            new_graph.add_node(item.get('from_issue_type'))
            new_graph.add_node(item.get('to_issue_type'))
            #new_graph.add_edge(item.get('from_issue_type'), "{0} \\n<size:7>(x{1})".format(item.get('link_name'),item.get('count')),item.get('to_issue_type'))
            new_graph.add_edge(item.get('from_issue_type'), item.get('link_name'),item.get('to_issue_type'))

        self.graph = new_graph
        self.graph.render_puml()
        return self

    def view_colors(self):

        issues = self.graph.get_nodes_issues()

        def resolve_letter(issue_type):
            if issue_type == 'GS-Project': return 'P', 'LightGreen'
            if issue_type == 'Risk'      : return 'R', 'LightPink'
            if issue_type == 'Risk Theme': return 'R', 'LightPink'
            if issue_type == 'GS Service': return 'S', 'LightGreen'
            return issue_type[0],'lightBlue'

        def resolve_status_color(status):
            if status == 'Done'       : return 'black', 'LightGreen'
            if status == 'In Progress': return 'black', 'LightGreen'
            if status == 'To Do'      : return 'black', 'LightPink'
            if status == 'Open'       : return 'white', 'Black'
            if status == 'BackLog'    : return 'black', 'LightGray'
            return 'black', 'lightBlue'

        def on_add_node(element,title,fixed_id, original_id):
            issue = issues.get(original_id)
            if issue is None: return '\t {0} "{1}" as {2}'.format(element, title, fixed_id)
            issue_type = issue.get('Issue Type').strip()
            status     = issue.get('Status')
            rating     = issue.get('Rating')
            if rating:
                if rating == 'High' or rating == 'Critical' : rating = '-' + rating
                else                                        : rating = '+' + rating
            (letter,letter_color) = resolve_letter(issue_type)
            color_text,status_back          = resolve_status_color(status)
            template =  '\tclass "<size:25> {0}" as {1} << ({2},{3} ) >>{{ \n ' + \
                        '\t\t\t  {4} | {5} | <b><color:{8}><back:{9}>{6} \n'                             + \
                        '\t\t\t----\n'                                          + \
                        '\t\t\t {7}             \n'                             + \
                        '\t\t}}'
            return template.format(title,fixed_id,letter,letter_color,
                                   original_id,issue_type, status,
                                   rating, color_text,status_back)

        self.graph.set_puml_show_key_in_text(False)
        self.graph.set_puml_on_add_node(on_add_node)
        self.graph.set_skin_param('ClassBackgroundColor' , 'White')
        self.graph.set_skin_param('ClassBorderColor'     , 'Gray' )
        self.graph.set_skin_param('ClassBorderThickness' , '2'    )
        self.graph.set_skin_param('Shadowing'            , 'False')
        self.graph.set_skin_param('ArrowColor'           , 'Gray' )
        self.graph.set_skin_param('Padding'              , '3'   )

        self.graph.render_puml()
        return self

    def view_it_systems(self):
        self.graph.set_puml_direction_top_down()
        self.graph.render_puml()
        return self

