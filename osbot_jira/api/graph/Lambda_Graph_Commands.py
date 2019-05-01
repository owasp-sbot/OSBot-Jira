import json
import pprint

from osbot_aws.apis.S3 import S3
from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment
from pbx_gs_python_utils.utils.Lambdas_Helpers       import slack_message
from pbx_gs_python_utils.utils.Misc                  import Misc
from pbx_gs_python_utils.utils.Save_To_ELK           import Save_To_ELK
from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper
from osbot_aws.apis.Lambda           import Lambda

from osbot_jira.api.graph.GS_Graph import GS_Graph
from osbot_jira.api.graph.Graph_Commands.Commands_Helper import Commands_Helper
from osbot_jira.api.graph.Graph_Commands.Graph_Filters import Graph_Filters
from osbot_jira.api.graph.Graph_Commands.Nodes import Nodes
from osbot_jira.api.graph.Graph_Commands.Vis_JS import Vis_JS
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph

Lambda_Graph_Commands_version = "v0.24"

class Lambda_Graph_Commands:

    @staticmethod
    def create(team_id, channel, params, data):
        (graph, graph_name, graph_or_key, depth, link_types_to_add) = Lambda_Graph_Commands.expand(team_id, channel, params, data,only_create=True)
        if channel:
            text = "Created new graph called `{0}`,\n by expanding the graph/key `{1}` with depth `{2}`, for link types `{3}` (`{4}` nodes, `{5}` edges)" \
                .format(graph_name, graph_or_key, depth, link_types_to_add,
                        len(graph.nodes), len(graph.edges))
            slack_message(text, [], channel, team_id)
            Lambda('lambdas.browser.lambda_browser').invoke_async({ "data": {"team_id": team_id,"channel":channel},"params" :['viva_graph', graph_name ,'default']})
        else:
            return graph

    @staticmethod
    def edit(team_id, channel, params, data):
        def send_slack_message(message):
            slack_message(message, [], channel, team_id)

        if len(params) < 1:
            text = ":exclamation: you must provide an `graph_name`"
            send_slack_message(text)
        else:
            #params.pop(0)           # remove 1st command since it is 'server'
            graph_name = params.pop(0)
            send_slack_message(':one: creating Sheet from Graph data ...')

            response = Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke({"params":['server','/jira-sync/sheet-from-graph/{0}'.format(graph_name)]})
            if response:
                weblink = json.loads(response.get('text')).get('status')
                jira_id = weblink.split('=')[1]
                send_slack_message(":point_right: Here is the link to the sheet created: {0}. \n\n:point_right: You will need to run the `jira load_sheet {1}` command before syncing".format(weblink,jira_id))
            else:
                send_slack_message(":red_circle: Some error occurred on the sync server (no data received from it)")

            #Lambda('gs.lambda_gdocs').invoke({"params": ['pdf', file_id], 'data': {'team_id': team_id, 'channel': channel}})

    @staticmethod
    def help(team_id, channel, params,  data):
        commands        = [func for func in dir(Lambda_Graph_Commands) if callable(getattr(Lambda_Graph_Commands, func)) and not func.startswith("__")]

        help_text = ""
        for command in commands:
            help_text += " • {0}\n".format(command)
        attachments = API_Slack_Attachment(help_text, 'good')
        text = "*Here are the `graph` commands available:*"
        slack_message(text, attachments.render(), channel,team_id)

    @staticmethod
    def filter(team_id, channel, params, data):
        return Commands_Helper(Graph_Filters,with_slack_support=True).invoke(team_id, channel, params)

    @staticmethod
    def nodes(team_id, channel, params, data):
        Commands_Helper(Nodes).invoke(team_id, channel, params)

#        from time import sleep                              # wait 1 sec (to allow ES index)
#        sleep(1)
#        Lambda_Graph_Commands.show(team_id, channel,["1"],None)      # show last graph created (this helps with the UX)

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

            Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
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
        attachments = API_Slack_Attachment(graphs_text, 'good')
        slack_message('*Here are the last {0} graphs generated* (use `graph last n` to see more results)'.format(n), attachments.render(), channel, team_id)


    @staticmethod
    def save(team_id, channel, params, data):
        if len(params) !=2:
            text            = ':red_circle: Hi, for the `save` command, you need to provide 2 parameters: '
            attachment_text =  '*graph index or key* - use the command `graph last_10` to get these values\n'  \
                               '*name* - the key you are going to use the future to load the graph'
            slack_message(text, [{'text': attachment_text}], channel, team_id)
            return
        index = int(params.pop(0))
        name  = params.pop(0)
        last_10_graphs = Lambda_Graph().get_last_n_graphs_of_type('lambda_graph', index)
        graph = last_10_graphs[index - 1]
        graph_id = graph.get('id')
        puml     = graph.get('value').get('doc_data').get('extra_data').get('puml')

        doc_type = graph.get('value').get('doc_type')
        doc_data = graph.get('value').get('doc_data')

        doc_data['name'] = name
        result = Save_To_ELK().add_document(doc_type, doc_data)

        text = "Saved graph `#{0}` (id = `{1}`, puml size = `{2}`) with name `{3}`".format(index, graph_id, len(puml), name)
        slack_message(text,[], channel, team_id)

    @staticmethod
    def show(team_id, channel, params, data=None):

        if len(params) < 1:
            text            = ':red_circle: Hi, for the `show` command, you need to provide an `graph_name`'
            slack_message(text,[], channel, team_id)
            return

        graph_name = Misc.array_pop(params,0)
        graph = Lambda_Graph().get_gs_graph___by_name(graph_name)
        if graph is None:
            text = ':red_circle: Graph with name `{0}` not found'.format(graph_name)
            slack_message(text, [], channel, team_id)
        else:

            engines = Misc.array_pop(params,0)
            if engines is None: engines = 'plantuml,vis_js,viva_graph,go_js'
            text = ":point_right: Showing graph with name `{0}`, with `{1}` nodes and `{2}` edges)".format(
                graph_name, len(graph.nodes), len(graph.edges))
            slack_message(text, [], channel, team_id)

            if 'plantuml' in engines:
                slack_message('...using `plantuml`', [], channel, team_id)
                Lambda('utils.puml_to_slack').invoke_async({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})

            if 'vis_js' in engines:
                slack_message('...using `vis_js`', [], channel, team_id)
                params = ['graph', graph_name, 'default']
                Lambda('lambdas.browser.lambda_browser').invoke_async({"params": params, 'data': {'team_id': team_id, 'channel': channel}})

            if 'viva_graph' in engines:
                slack_message('...using `viva_graph`', [], channel, team_id)
                params = ['viva_graph',graph_name,'default']
                Lambda('lambdas.browser.lambda_browser').invoke_async({"params": params, 'data': {'team_id': team_id, 'channel': channel}})

            if 'go_js' in engines:
                slack_message('...using `go_js`', [], channel, team_id)
                params = ['go_js', graph_name, 'circular']
                Lambda('lambdas.browser.lambda_browser').invoke_async({"params": params, 'data': {'team_id': team_id, 'channel': channel}})


        # if len(params) !=1:
        #     text            = ':red_circle: Hi, for the `show` command, you need to provide an `id`. Use `graph last` to see the `ids` available'
        #     slack_message(text,[], channel, team_id)
        #     return
        #
        # target = "".join(params)
        #
        # from utils.Dev import Dev
        # if target.isdigit():                        # if it is a number use it has the index of the last executed query
        #     index          = int(target)
        #     last_10_graphs = Lambda_Graph().get_last_n_graphs_of_type('lambda_graph', index)
        #     graph          = last_10_graphs[index -1]
        #
        #     puml           = graph.get('value').get('doc_data').get('extra_data').get('puml')
        #     slack_message('*Showing last graph `#{0}` with size `{1}`*'.format(index, len(puml)), [], channel, team_id)
        #     Lambda('utils.puml_to_slack').invoke({"puml": puml, "channel": channel , "team_id": team_id})
        # else:                                       # if is a string try to use it as story
        #     Lambda_Graph_Commands.story(team_id, channel,params,data)

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
        Lambda('lambdas.browser.lambda_browser').invoke_async({"params": graph_params, 'data': {'team_id': team_id, 'channel': channel}})


    # @staticmethod
    # def story(team_id, channel, params, data):
    #
    #     from gs_elk.security_stories.Sec_9195 import SEC_9155
    #     sec_9195 = SEC_9155()
    #     if len(params) == 2 and params[1] == 'stakeholders':
    #         graph_name = params[0]
    #         text = "showing stakeholders for story: {0}".format(graph_name)
    #         slack_message(text, [], channel, team_id)
    #         graph = Lambda_Graph().get_gs_graph___by_name(graph_name)
    #         if graph is None:
    #             text = ':red_circle: Graph with name `{0}` not found'.format(graph_name)
    #             slack_message(text, [], channel, team_id)
    #         else:
    #             sec_9195.story_nodes = graph.nodes
    #             stakeholders = sec_9195.get_stakeholders()
    #             attach_text = ""
    #             graph = GS_Graph()
    #             for key, value in stakeholders.items():
    #                graph.puml.add_actor("{0} - {1}".format(key, value), key)
    #                attach_text += "• {0:5} - {1}\n".format(key, value)
    #
    #             text = "here is the list of stakeholders found in graph"
    #             slack_message(text, [{'text': attach_text}], channel, team_id)
    #             graph.render_puml()
    #             Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #         return
    #
    #     if len(params) == 4 and params[1] == 'stakeholder':
    #         graph_name       = params[0]
    #         stakeholder = params[2]
    #         depth       = int(params[3])
    #         text = "showing stakeholder `{0}` for story: `{1}` with depth `{2}`".format(stakeholder,graph_name, depth)
    #         slack_message(text, [], channel, team_id)
    #
    #         graph = Lambda_Graph().get_gs_graph___by_name(graph_name)
    #         if graph is None:
    #             text = ':red_circle: Graph with name `{0}` not found'.format(graph_name)
    #             slack_message(text, [], channel, team_id)
    #         else:
    #             sec_9195.story_nodes = graph.nodes
    #             graph = sec_9195.render_stakeholder(stakeholder, depth)
    #
    #             graph.render_and_save_to_elk(graph_type = '_'.join(params))  # will not render if puml is already there
    #
    #             Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #
    #         return
    #
    #
    #     if len(params) == 1:
    #         graph_name = params.pop()
    #         graph = Lambda_Graph().get_gs_graph___by_name(graph_name)
    #         if graph is None:
    #             text = ':red_circle: Graph with name `{0}` not found'.format(graph_name)
    #             slack_message(text, [], channel, team_id)
    #         else:
    #             text = "Showing graph with name `{0}`, with `{1}` nodes and `{2}` edges".format(graph_name, len(graph.nodes), len(graph.edges))
    #             slack_message(text, [], channel, team_id)
    #             Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #         return
    #     text = ':red_circle: Hi, command not recognised: {0}'.format(params)
    #     slack_message(text, [], channel, team_id)

    @staticmethod
    def epic(team_id, channel, params, data):
        if len(params) == 1:
            keys = params.pop().split(',')
            graph = GS_Graph()
            (graph.set_links_path_mode_to_down()
                  .add_all_linked_issues(keys, 1)
                  .add_nodes_from_epics()
                  .add_all_linked_issues()
             )
            graph.render_puml()
            graph_name = Lambda_Graph().save_gs_graph(graph)
            slack_message(":point_right: created graph called `{0}` for issues in epic(s)".format(graph_name), [], channel, team_id)
            Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
            return
        text = ':red_circle: Hi, you need to provide an issue ID to find the epics'
        slack_message(text, [], channel, team_id)

    # @staticmethod
    # def epics_details(team_id, channel, params, data):
    #     if len(params) == 1:
    #         keys = params.pop().split(',')
    #         graph = GS_Graph()
    #         graph.create_epic_graph_with_details(keys)
    #
    #         Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #         return
    #     text = ':red_circle: Hi, you need to provide an issue ID to find the epics'
    #     slack_message(text, [], channel, team_id)

    @staticmethod
    def gs_okrs(team_id, channel, params, data=None):
        graph = GS_Graph()
        (graph.add_all_linked_issues(['GSOKR-924'])
             .add_nodes_from_epics()
             .set_link_paths_to_ignore(['is child of', 'has Stakeholder'])
             .set_links_path_mode_to_up()
             .add_all_linked_issues(depth=5)
        )
        graph.render_puml()
        Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})

    # @staticmethod
    # def gs_sec_8694(team_id, channel, params, data):
    #     graph = GS_Graph()
    #     (graph.add_all_linked_issues(['SEC-8694'])
    #          .add_nodes_from_epics()
    #          .set_links_path_mode_to_up()
    #          .add_all_linked_issues(depth=2)
    #     )
    #     graph.render_and_save_to_elk('gs_sec_8694','gs_sec_8694')
    #     Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})

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
                    s3_bucket = 'gs-lambda-tests'
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.json') as temp:
                        temp.write(str.encode(json.dumps(data)))
                        temp.flush()
                        data = S3().file_upload_as_temp_file(temp.name, s3_bucket)

                attachments = [{"color": "good", "text": "{0}".format(pprint.pformat(data))}]
            else:
                from pbx_gs_python_utils.gs.API_Issues import API_Issues            # if a graph wasn't found try to get the issue with that name
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
        from pbx_gs_python_utils.gs_elk.Graph_View import Graph_View  # has to be done locally

        if len(params) < 1:
            text = ':red_circle: Hi, for the `view` command, you need to provide a graph name (use `graph last` to see a list of graphs names you can use)'
            slack_message(text, [], channel, team_id)
            return

        if len(params) == 1:
            text = Graph_View().bad_params_message()
            slack_message(text, [], channel, team_id)
            return


        graph = Graph_View().handle_lambda_request(params, channel, team_id)

        if graph:
            Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})

    @staticmethod
    def vis_js(team_id, channel, params, data):
        return Slack_Commands_Helper(Vis_JS).invoke(team_id, channel, params)

    @staticmethod
    def version(team_id, channel, params, data):
        slack_message(Lambda_Graph_Commands_version, [], channel, team_id)



    #LEGACY TO REMOVE
    # @staticmethod
    # def story_jira_sec_9195(team_id, channel, params, data):
    #     from gs_elk.security_stories.Sec_9195 import SEC_9155
    #     sec_9195 = SEC_9155()
    #
    #     if len(params)==1 and params[0] == 'stakeholders':
    #         text = "...creating stakeholders graph"
    #         slack_message(text, [], channel, team_id)
    #
    #         graph = GS_Graph()                              # move this to a stakeholders_render method
    #         sec_9195.get_all_nodes_for_story(2, 4)
    #         stakeholders = sec_9195.get_stakeholders()
    #         attach_text = ""
    #         for key, value in stakeholders.items():
    #             graph.puml.add_actor("{0} - {1}".format(key,value), key)
    #             attach_text += "• {0:5} - {1}\n".format(key,value)
    #
    #         text = "here is the list of stakeholders found in graph"
    #         slack_message(text, [{'text': attach_text }], channel, team_id)
    #
    #         graph.render_puml()
    #         Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #         return
    #
    #     #graph = self.sec_9195.render_stakeholder(stakeholder, 4)
    #     if len(params) == 2 and params[0] == 'stakeholder':
    #         stakeholder = params[1]
    #         text = "...creating stakeholders graph for `{0}`".format(stakeholder)
    #         slack_message(text, [], channel, team_id)
    #         graph = sec_9195.render_stakeholder(stakeholder, 4)
    #         Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #         return
    #
    #     if len(params) == 3 and params[0] == 'stakeholder':
    #         stakeholder = params[1]
    #         depth       = int(params[2])
    #         text        = "...creating stakeholders graph for `{0}` with depth `{1}`".format(stakeholder, depth)
    #         slack_message(text, [], channel, team_id)
    #         graph = sec_9195.render_stakeholder(stakeholder, depth)
    #         Lambda('utils.puml_to_slack').invoke({"puml": graph.get_puml(), "channel": channel, "team_id": team_id})
    #         return
    #
    #     if len(params) == 1 and params[0] == 'save':
    #         user        = data.get('user')
    #         graph_name  = 'sec_9195'
    #         graph_type  = 'sec_9195'
    #
    #         sec_9195.get_all_nodes_for_story()
    #         sec_9195.all_nodes_graph.render_and_save_to_elk(graph_name, graph_type, channel, user)
    #         text = "Graph for Story SEC-9195 has been rendered"
    #         slack_message(text, [], channel, team_id)
    #         return
    #
    #     text = ':red_circle: Hi, command not recognised: {0}'.format(params)
    #     slack_message(text, [], channel, team_id)