import json
import pprint

from osbot_aws.apis.S3 import S3
from osbot_aws.apis.Lambda           import Lambda

from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_jira.api.graph.GS_Graph import GS_Graph
from osbot_jira.api.graph.Graph_Commands.Commands_Helper import Commands_Helper
from osbot_jira.api.graph.Graph_Commands.Graph_Filters import Graph_Filters
from osbot_jira.api.graph.Graph_Commands.Nodes import Nodes
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph
from osbot_jira.api.slack.API_Slack_Attachment import API_Slack_Attachment
from osbot_utils.utils import Misc
from osbot_utils.utils.Lists import array_pop

Lambda_Graph_Commands_version = "v0.35 (GW)"

class Lambda_Graph_Commands:

    # @staticmethod
    # def create(team_id, channel, params, data):
    #     (graph, graph_name, graph_or_key, depth, link_types_to_add) = Lambda_Graph_Commands.expand(team_id, channel, params, data,only_create=True)
    #     if channel:
    #         text = "Created new graph called `{0}`,\n by expanding the graph/key `{1}` with depth `{2}`, for link types `{3}` (`{4}` nodes, `{5}` edges)" \
    #             .format(graph_name, graph_or_key, depth, link_types_to_add,
    #                     len(graph.nodes), len(graph.edges))
    #         slack_message(text, [], channel, team_id)
    #         Lambda('osbot_jira.lambdas.graph').invoke_async({ "data": {"team_id": team_id,"channel":channel},"params" :['viva_graph', graph_name ,'default']})
    #         #'lambdas.browser.lambda_browser'
    #     else:
    #         return graph

    # @staticmethod
    # def edit(team_id, channel, params, data):
    #     def send_slack_message(message):
    #         slack_message(message, [], channel, team_id)
    #
    #     if len(params) < 1:
    #         text = ":exclamation: you must provide an `graph_name`"
    #         send_slack_message(text)
    #     else:
    #         #params.pop(0)           # remove 1st command since it is 'server'
    #         graph_name = params.pop(0)
    #         send_slack_message(':one: creating Sheet from Graph data ...')
    #
    #         response = Lambda('osbot_jira.lambdas.jira').invoke({"params":['server','/jira-sync/sheet-from-graph/{0}'.format(graph_name)]})
    #         if response:
    #             weblink = json.loads(response.get('text')).get('status')
    #             jira_id = weblink.split('=')[1]
    #             send_slack_message(":point_right: Here is the link to the sheet created: {0}. \n\n:point_right: You will need to run the `jira load_sheet {1}` command before syncing".format(weblink,jira_id))
    #         else:
    #             send_slack_message(":red_circle: Some error occurred on the sync server (no data received from it)")
    #
    #         #Lambda('gs.lambda_gdocs').invoke({"params": ['pdf', file_id], 'data': {'team_id': team_id, 'channel': channel}})

    @staticmethod
    def help(team_id, channel, params,  data):
        commands        = [func for func in dir(Lambda_Graph_Commands) if callable(getattr(Lambda_Graph_Commands, func)) and not func.startswith("__")]

        help_text = ""
        for command in commands:
            help_text += " • {0}\n".format(command)
        attachments = API_Slack_Attachment(help_text, 'good').render()
        text = "*Here are the `graph` commands available:*"
        if channel:
            slack_message(text, attachments, channel,team_id)
        else:
            return text,attachments

    @staticmethod
    def filter(team_id=None, channel=None, params=None, data=None):
        result = Commands_Helper(Graph_Filters,with_slack_support=True).invoke(team_id, channel, params)
        if channel is None:                 # cases when filter is invoked directly (from example from Jupyter)
            return result

    @staticmethod
    def nodes(team_id, channel, params, data):
        Commands_Helper(Nodes).invoke(team_id, channel, params)

    @staticmethod
    def expand(team_id=None, channel=None, params=None, data=None, only_create=False, save_graph=True):

        if len(params) < 3:
            text            = ':red_circle: Hi, for the `expand` command, you need to provide the following parameters: '
            attachment_text =  '- *graph_name*: the graph to expand\n'  \
                               '- *depth* : how many cycles to expand\n'  \
                               '- *links to expand*: as a comma-delimited list '
            slack_message(text, [{'text': attachment_text}],channel, team_id)
            return
        create_params       = ["expand"] + list(params)                      # create copy of array so that we don't lose data with the pops below
        graph_or_key        = params.pop(0)
        depth               = int(params.pop(0))
        link_types_to_add   = ' '.join(params).split(',')

        graph = Lambda_Graph().get_gs_graph___by_name(graph_or_key)
        if graph is None:
            graph = GS_Graph()                                  # if it wasn't a graph
            graph.add_node(graph_or_key)                        # use it as key

        (graph.set_puml_link_types_to_add(link_types_to_add)
              .add_all_linked_issues([],depth)
              .set_create_params(create_params))
        if save_graph:
            new_graph_name = graph.reset_puml().render_and_save_to_elk()
        else:
            return graph

        if only_create:
            return graph, new_graph_name, graph_or_key, depth, link_types_to_add

        if channel:                                             # if the channel value is provided render the new graph and send it to slack, if not, just return the new graph data
            text = "Rendering new graph called `{0}`,\n Which was created by expanding the graph/key `{1}` with depth `{2}`, for link types `{3}` (`{4}` nodes, `{5}` edges)"\
                        .format(new_graph_name, graph_or_key, depth, link_types_to_add,
                                len(graph.nodes), len(graph.edges))
            slack_message(text, [],channel, team_id)

            Lambda('gw_bot.lambdas.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
        else:
            data = {
                "graph_or_key" : graph_or_key   ,
                "depth"        : depth          ,
                "nodes"        : graph.nodes    ,
                "edges"        : graph.edges    ,
                "puml"         : graph.puml.puml,
                "graph_name"   : new_graph_name
            }
            return json.dumps(data, indent=4)



    @staticmethod
    def last(team_id, channel, params, data=None):
        n = 10
        if len(params) == 1:
            n =  int(params.pop())

        graphs = Lambda_Graph().get_last_n_graphs_of_type('lambda_graph', n)
        row_separator = '|{0}|\n'.format("-" * 72)
        row_format    = '| {0:2} | {1:9} | {2:5} | {3:5} | {4:24} | {5:10} |\n'
        graphs_text   =  '```'
        graphs_text  += row_format.format('#','   who   ', 'nodes', 'edges', '            type', ' name')
        graphs_text  += row_separator
        count         = 1
        for graph in graphs:
            graph_value = graph.get('value')
            graph_name  = graph_value.get('doc_data').get('name'      )
            graph_type  = graph_value.get('doc_data').get('type'      )
            extra_data  = graph_value.get('doc_data').get('extra_data')
            user        = extra_data.get('user')
            nodes       = extra_data.get('stats').get('count_nodes')
            edges       = extra_data.get('stats').get('count_edges')
            if user       is None: user       = "...."
            if graph_type is None: graph_type = "...."
            if graph_name is None: graph_name = ""
            graphs_text += row_format.format(count, user, nodes, edges, graph_type[0:24], graph_name[0:10])
            count       += 1
        graphs_text += '```'
        attachments = API_Slack_Attachment(graphs_text, 'good').render()
        if channel:
            slack_message('*Here are the last {0} graphs generated* (use `graph last n` to see more results)'.format(n), attachments, channel, team_id)
        else:
            return attachments


    # @staticmethod
    # def save(team_id, channel, params, data):
    #     if len(params) !=2:
    #         text            = ':red_circle: Hi, for the `save` command, you need to provide 2 parameters: '
    #         attachment_text =  '*graph index or key* - use the command `graph last_10` to get these values\n'  \
    #                            '*name* - the key you are going to use the future to load the graph'
    #         slack_message(text, [{'text': attachment_text}], channel, team_id)
    #         return
    #     index = int(params.pop(0))
    #     name  = params.pop(0)
    #     last_10_graphs = Lambda_Graph().get_last_n_graphs_of_type('lambda_graph', index)
    #     graph = last_10_graphs[index - 1]
    #     graph_id = graph.get('id')
    #     puml     = graph.get('value').get('doc_data').get('extra_data').get('puml')
    #
    #     doc_type = graph.get('value').get('doc_type')
    #     doc_data = graph.get('value').get('doc_data')
    #
    #     doc_data['name'] = name
    #     result = Save_To_ELK().add_document(doc_type, doc_data)
    #
    #     text = "Saved graph `#{0}` (id = `{1}`, puml size = `{2}`) with name `{3}`".format(index, graph_id, len(puml), name)
    #     slack_message(text,[], channel, team_id)

    @staticmethod
    def show(team_id, channel, params, data=None):

        if len(params) < 1:
            text            = ':red_circle: Hi, for the `show` command, you need to provide an `graph_name`'
            slack_message(text,[], channel, team_id)
            return

        graph_name = array_pop(params,0)
        graph = Lambda_Graph().get_gs_graph___by_name(graph_name)
        if graph is None:
            text = ':red_circle: Graph with name `{0}` not found'.format(graph_name)
            slack_message(text, [], channel, team_id)
        else:
            default_engine = 'viva_graph'
            engines = array_pop(params,0)
            if engines is None: engines = default_engine

            if engines != default_engine:                     # only show in case there is more than one engine
                text = f":point_right: Showing graph with name `{graph_name}`, with `{len(graph.nodes)}` nodes and `{len(graph.edges)}` edges)"
                slack_message(text, [], channel, team_id)

            if 'plantuml' in engines:
                slack_message('...using `plantuml`', [], channel, team_id)
                Lambda('gw_bot.lambdas.puml_to_slack').invoke_async({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})

            if 'vis_js' in engines:
                slack_message('...using `vis_js`', [], channel, team_id)
                params = ['graph', graph_name, 'default']
                Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({"params": params, 'data': {'team_id': team_id, 'channel': channel}})

            if 'viva_graph' in engines:
                if engines != default_engine:   # only show in case there is more than one engine
                    slack_message('...using `viva_graph`', [], channel, team_id)
                params = ['viva_graph',graph_name,'default']
                Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({"params": params, 'data': {'team_id': team_id, 'channel': channel}})

            if 'go_js' in engines:
                slack_message('...using `go_js`', [], channel, team_id)
                params = ['go_js', graph_name, 'circular']
                Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({"params": params, 'data': {'team_id': team_id, 'channel': channel}})

    @staticmethod
    def mindmap(team_id, channel, params, data=None):
        if len(params) < 1:
            text   = ':red_circle: Hi, for the `mindmap` command, you need to provide an `graph_name`'
            slack_message(text,[], channel, team_id)
            return
        graph_name = params.pop(0)
        if len(graph_name.split('-')) == 2:                       # hacked way to see if it is an issue (vs a saved graph name)
            action = 'mindmap_issue'
        else:
            action = 'mindmap'
        graph_params = ['go_js', graph_name, action]
        graph_params.extend(params)
        Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({"params": graph_params, 'data': {'team_id': team_id, 'channel': channel}})

    # @staticmethod
    # def epic(team_id, channel, params, data):
    #     if len(params) == 1:
    #         keys = params.pop().split(',')
    #         graph = GS_Graph()
    #         (graph.set_links_path_mode_to_down()
    #               .add_all_linked_issues(keys, 1)
    #               .add_nodes_from_epics()
    #               .add_all_linked_issues()
    #          )
    #         graph.render_puml()
    #         graph_name = Lambda_Graph().save_gs_graph(graph)
    #         slack_message(":point_right: created graph called `{0}` for issues in epic(s)".format(graph_name), [], channel, team_id)
    #         Lambda('gw_bot.lambdas.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #         return
    #     text = ':red_circle: Hi, you need to provide an issue ID to find the epics'
    #     slack_message(text, [], channel, team_id)

    # @staticmethod
    # def gs_okrs(team_id, channel, params, data=None):
    #     graph = GS_Graph()
    #     (graph.add_all_linked_issues(['GSOKR-924'])
    #          .add_nodes_from_epics()
    #          .set_link_paths_to_ignore(['is child of', 'has Stakeholder'])
    #          .set_links_path_mode_to_up()
    #          .add_all_linked_issues(depth=5)
    #     )
    #     graph.render_puml()
    #     Lambda('gw_bot.lambdas.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})

    @staticmethod
    def raw_data(team_id=None, channel=None, params=None, data=None):
        data        = None
        text        = None
        attachments = []

        if len(params) < 1:
            text = ':red_circle: Hi, for the `data` command, you need to provide a graph name'
        else:
            graph_name = params.pop(0)
            graph      = Lambda_Graph().get_gs_graph___by_name(graph_name)

            if graph:
                data = {
                    'graph_name' : graph_name,
                    'nodes'      : graph.nodes,
                    'edges'      : graph.edges
                }
                if len(params) == 1 and params.pop(0)=='details':
                    data['nodes'] = graph.get_nodes_issues()
                    s3_bucket = 'gw-bot-lambdas'
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.json') as temp:
                        temp.write(str.encode(json.dumps(data)))
                        temp.flush()
                        data = S3().file_upload_as_temp_file(temp.name, s3_bucket)

                attachments = [{"color": "good", "text": "{0}".format(pprint.pformat(data))}]
            else:
                from osbot_jira.api.API_Issues import API_Issues        # if a graph wasn't found try to get the issue with that name
                issue = API_Issues().issue(graph_name)
                if issue:
                    data = {
                        'nodes': {graph_name : issue},          # return as the first node
                        'edges': []                             # with no edges
                    }
                else:
                    text = ':red_circle: Graph or issue with name `{0}` not found! Use the command `graph last` to see a list of the latest graphs generated'.format(graph_name)

        slack_message(text, attachments, channel, team_id)
        return data

    @staticmethod
    def plantuml(team_id, channel, params, data):
        puml = ''
        attachments = []

        if len(params) < 1:
            text = ':red_circle: Hi, for the `plantuml` command, you need to provide a graph name'
        else:
            graph_name = params.pop()
            graph = Lambda_Graph().get_gs_graph___by_name(graph_name)

            if graph:
                puml = graph.puml.puml
                text = 'Here is the PlantUml code for `{0}`'.format(graph_name)
                attachments = [{"color": "good", "text": "```{0}```".format(puml)}]
            else:
                text = ':red_circle: Graph with name `{0}` not found! Use the command `graph last` to see a list of the latest graphs generated'.format(
                    graph_name)

        slack_message(text, attachments, channel, team_id)
        return puml

    @staticmethod
    def view(team_id, channel, params, data):

        from osbot_jira.api.graph.Graph_View import Graph_View # check if it needs to be done locally

        if len(params) < 1:
            text = ':red_circle: Hi, for the `view` command, you need to provide a graph name (use `graph last` to see a list of graphs names you can use)'
            return slack_message(text, [], channel, team_id)

        if len(params) == 1:

            text = Graph_View().bad_params_message()
            return slack_message(text, [], channel, team_id)


        graph = Graph_View().handle_lambda_request(params, channel, team_id)

        if graph:
            puml = graph.get_puml()
            if channel:
                Lambda('gw_bot.lambdas.puml_to_slack').invoke({"puml": puml, "channel": channel, "team_id": team_id})
            return puml

    # @staticmethod
    # def vis_js(team_id, channel, params, data):
    #     return Slack_Commands_Helper(Vis_JS).invoke(team_id, channel, params)

    @staticmethod
    def version(team_id, channel, params, data):
        if channel:
            slack_message(Lambda_Graph_Commands_version, [], channel, team_id)
        else:
            return Lambda_Graph_Commands_version
