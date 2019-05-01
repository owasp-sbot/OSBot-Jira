import pprint

from osbot_aws.apis.Lambda import Lambda

#from gs_elk.Lambda_Graph_Commands   import Lambda_Graph_Commands
from osbot_jira.api.graph.GS_Graph                      import GS_Graph
from pbx_gs_python_utils.utils.Lambdas_Helpers          import log_to_elk, slack_message
from pbx_gs_python_utils.utils.Misc                     import Misc
from pbx_gs_python_utils.utils.Save_To_ELK              import Save_To_ELK


class Lambda_Graph():
    def __init__(self):
        self.save_to_elk = Save_To_ELK()
        self.doc_type    = 'lambda_graph'

    def get_gs_graph_from_most_recent_version(self, lucene_query):
        data = self.save_to_elk.get_most_recent_version_of_document(lucene_query)
        if data is None: return None
        graph = GS_Graph()
        if data.get('nodes'):
            graph.nodes = data.get('nodes')
            graph.edges = data.get('edges')
            graph.puml.puml = data.get('extra_data').get('puml')
        return graph

    def get_gs_graph___by_name  (self, graph_name): return self.get_gs_graph_from_most_recent_version(lucene_query = 'doc_data.name:"{0}"'           .format(graph_name))
    def get_gs_graph___by_type  (self, graph_type): return self.get_gs_graph_from_most_recent_version(lucene_query = 'doc_data.type:"{0}"'           .format(graph_type))
    def get_gs_graph___from_user(self, user      ): return self.get_gs_graph_from_most_recent_version(lucene_query = 'doc_data.extra_data.user:"{0}"'.format(user      ))

    def get_graph_png___by_name(self, graph_name):
        graph = self.get_gs_graph___by_name(graph_name)
        puml = graph.puml.puml
        puml_to_png = Lambda('utils.puml_to_png').invoke
        return puml_to_png({"puml": puml})

    def get_last_10_graphs(self):
        return self.get_last_n_graphs_of_type(self.doc_type, 10)

    def get_last_n_graphs_of_type(self, doc_type, count):
        lucene_query = 'doc_type."{0}"'.format(doc_type)
        return self.save_to_elk.elastic.search_using_lucene_sort_by_date(lucene_query, count)

    def handle_lambda_event(self, event):
        log_to_elk("in Lambda_Graph.handle_lambda_event :{0}".format(event))
        data    = event.get('data')
        if data:
            channel = data.get('channel')
            team_id = data.get('team_id')
        else:
            channel = None
            team_id = None
        params  = event.get('params')

        if params is None or len(params) == 0:
            params = ['help']

        from osbot_jira.api.graph import Lambda_Graph_Commands # can only do this here to avoid circular dependencies
        try:
            method_name  = params.pop(0)
            method       = getattr(Lambda_Graph_Commands, method_name)
        except Exception:
            method = Lambda_Graph_Commands.help
        try:
            return method(team_id, channel, params, data)
        except Exception as error:
            slack_message(':red_circle: Error processing params `{0}`: _{1}_'.format(params, pprint.pformat(error)), [], channel)
            log_to_elk("Error in Lambda_Graph.handle_lambda_event :{0}".format(error), level = 'error')


        ##Lambda_Graph_Commands().help(channel, data)

    def load_gs_graph(self,name):
        return self.get_gs_graph___by_name(name)

    def save_gs_graph(self, graph: GS_Graph, graph_name = None, graph_type = None, channel= None, user = None):
        nodes = graph.nodes
        edges = graph.edges
        puml  = graph.puml.puml
        if '@enduml' not in puml:       # means that graph is not rendered
            puml = graph.render_puml().puml

        extra_data = {
                        "user"    : user                ,
                        "channel" : channel             ,
                        "puml"    : puml                ,
                        "params"  : graph.create_params ,
                        "stats"   : graph.stats()
                    }
        return self.save_graph(nodes, edges, extra_data, None, graph_name, graph_type)

    def save_graph(self, nodes, edges, extra_data = None, graph_id = None, graph_name = None, graph_type = None):
        if graph_name is None:                                          # if graph_name is not set
            graph_name = Misc.random_string_and_numbers(3, 'graph_' )   # give it a temp name

        graph = {
                "name"      : graph_name ,
                "type"      : graph_type ,
                "extra_data": extra_data,
                "nodes"     : nodes      ,
                "edges"     : edges
            }

        self.save_to_elk.add_document_with_id(self.doc_type, graph_id, graph)
        return graph_name

    def send_graph_to_slack___by_type(self, graph_name, channel):
        graph = self.get_gs_graph___by_type(graph_name)
        return Lambda('utils.puml_to_slack').invoke({"puml"   : graph.get_puml(), "channel": channel})
