import json

from osbot_aws.apis.Lambda import Lambda

from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph


class Vis_JS:

    @staticmethod
    def _render_graph(data, team_id, channel):
        lambda_browser = Lambda('lambdas.browser.lambda_browser')
        payload = {"params": ['vis_js', json.dumps(data)]}

        #print(payload)
        png_data = lambda_browser.invoke(payload)

        if channel and team_id:
            png_to_slack = Lambda('utils.png_to_slack')
            payload = {'png_data': png_data, 'team_id': team_id, 'channel': channel}
            png_to_slack.invoke(payload)

        else:
            return png_data

    @staticmethod
    def saved_graph(team_id, channel, params):

        if len(params) == 0:
            return ':red_circle: for the `saved_graph` command you need to provide an valid Issue ID'

        graph_name = params.pop(0)
        graph = Lambda_Graph().get_gs_graph___by_name(graph_name)
        if graph:
            nodes = []
            edges = []
            #for key, value in graph_data.get('nodes').items():
            for key in graph.nodes:
                #nodes.append({'id': key, 'label': value.get(label_key)})
                nodes.append({'id': key, 'label': key })
                # print(key,value)

            for edge in graph.edges:
                from_node = edge[0]
                link_type = edge[1]
                to_node = edge[2]
                edges.append({'from': from_node, 'to': to_node, 'label': link_type})

            data = {'nodes': nodes, 'edges': edges, 'options': {}}

            return Vis_JS._render_graph(data, team_id, channel)

            return 'graph {0} has {1} nodes and {2} edges'.format(graph_name, len(nodes), len(edges))
        else:
            return ':red_circle: graph `{0}` not found'.format(graph_name)

        # nodes = [{'id': '123', 'label': 'this is a label\n in two lines\n3 lines'},
        #          {'id': 'aaa', 'label': '123'}]
        # edges = [{'from': '123', 'to': 'aaa'}]
        #
        # options = {'nodes': {'shape': 'box'}}
        # data = {'nodes': nodes, 'edges': edges, 'options': options}
        #
        # # params = [json.dumps(data)]




    @staticmethod
    def simple_graph(team_id, channel, params):
        nodes = [{'id': '123', 'label': 'this is a label\n in two lines\n3 lines'},
                 {'id': 'aaa', 'label': '123'}]
        edges = [{'from': '123', 'to': 'aaa'}]

        options = {'nodes': {'shape': 'box'}}
        data = {'nodes': nodes, 'edges': edges, 'options': options}

        #params = [json.dumps(data)]

        lambda_browser = Lambda('lambdas.browser.lambda_browser')
        payload = {"params": ['vis_js', json.dumps(data)]}
        png_data = lambda_browser.invoke(payload)
        if channel and team_id:
            png_to_slack = Lambda('utils.png_to_slack')
            payload = {'png_data':png_data, 'team_id': team_id, 'channel': channel }
            png_to_slack.invoke(payload)

        else:
            return png_data
