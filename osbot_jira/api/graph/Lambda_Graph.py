import pprint
from time import sleep

from osbot_aws.apis.Lambda           import Lambda
from osbot_aws.helpers.Lambda_Helpers import slack_message, log_to_elk
from osbot_elastic.Save_To_ELK import Save_To_ELK

from osbot_jira.api.graph.GS_Graph   import GS_Graph
from osbot_jira.osbot_graph.Graph    import Graph
from osbot_jira.osbot_graph.engines.Graph_Dot import Graph_Dot
from osbot_utils.utils.Misc import random_string_and_numbers


class Lambda_Graph():
    def __init__(self):
        self._save_to_elk = None
        self.doc_type     = 'lambda_graph'

    def save_to_elk(self):
        if self._save_to_elk is None:
            self._save_to_elk    = Save_To_ELK()
        return self._save_to_elk

    def get_graph(self, graph_name):
        graph_data = self.get_graph_data(graph_name)
        nodes = graph_data.get('nodes').keys()
        edges = graph_data.get('edges')
        return Graph().add_nodes(nodes)     \
                      .add_edges(edges)

    def get_graph_dot(self, graph_name):
        return Graph_Dot(self.get_graph(graph_name))

    def get_graph_data(self, graph_name):
        graph_data = { "graph_name": graph_name ,
                       "nodes"     : []         ,
                       "edges"     : []         }
        graph      = self.load_gs_graph(graph_name)

        if graph:
            graph_data['nodes'] = graph.get_nodes_issues()
            graph_data["edges"] = graph.edges
        return graph_data

        #data['nodes'] =
    def get_gs_graph_from_most_recent_version(self, lucene_query):
        data = self.save_to_elk().get_most_recent_version_of_document(lucene_query)
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
        puml_to_png = Lambda('gw_bot.lambdas.puml_to_png').invoke
        return puml_to_png({"puml": puml})

    def get_last_10_graphs(self):
        return self.get_last_n_graphs_of_type(self.doc_type, 10)

    def get_last_n_graphs_of_type(self, doc_type, count):
        lucene_query = 'doc_type."{0}"'.format(doc_type)
        return self.save_to_elk().elastic.search_using_lucene_sort_by_date(lucene_query, count)

    def handle_lambda_event(self, event):
        #log_to_elk("in Lambda_Graph.handle_lambda_event :{0}".format(event))
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

        from osbot_jira.api.graph.Lambda_Graph_Commands import Lambda_Graph_Commands # can only do this here to avoid circular dependencies
        try:
            method_name  = params.pop(0)
            method       = getattr(Lambda_Graph_Commands, method_name)
        except Exception:
            method = Lambda_Graph_Commands.help
        try:
            return method(team_id, channel, params, data)
        except Exception as error:
            message = ':red_circle: Error processing params `{0}`: _{1}_'.format(params, pprint.pformat(error))
            slack_message(message, [], channel)
            log_to_elk("Error in Lambda_Graph.handle_lambda_event :{0}".format(error), level = 'error')
            return message


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
            graph_name = random_string_and_numbers(3, 'graph_' )   # give it a temp name

        graph = {
                "name"      : graph_name ,
                "type"      : graph_type ,
                "extra_data": extra_data,
                "nodes"     : nodes      ,
                "edges"     : edges
            }

        self.save_to_elk().add_document_with_id(self.doc_type, graph_id, graph)
        return graph_name

    def send_graph_to_slack___by_type(self, graph_name, channel):
        graph = self.get_gs_graph___by_type(graph_name)
        return Lambda('gw_bot.lambdas.puml_to_slack').invoke({"puml"   : graph.get_puml(), "channel": channel})

    def graph_links(self, target, depth=1):
        if target is None:
            return None
        graph = self.get_gs_graph___by_name(target)             # check if the value provided is a saved graph
        if graph is not None:                                   # if it exists
            keys = graph.nodes                                  # set keys to graph nodes
        else:                                                   # if not
            keys = target.upper().split(",")                    # use value as keys

        graph = GS_Graph()
        graph.add_all_linked_issues(keys, depth)
        return graph

    def wait_for_elk_to_index_graph(self, graph_name, wait_count=10, wait_for_ms=100):
        for i in range(wait_count):
            graph = self.get_gs_graph___by_name(graph_name)
            if graph:
                return True
            #print(f'[{wait_count}] not there yet so sleeping for {wait_for_ms}')
            sleep(wait_for_ms/1000)
        return False
