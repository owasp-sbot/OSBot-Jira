import pprint

from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph


class Nodes:
    @staticmethod
    def _check_params(params, expected_params):
        if len(params) != len(expected_params):
            text        = ':red_circle: For this command, you need to provide the following parameters: '
            attachment_text=''
            for expected_param in expected_params:
                attachment_text += '- {0} \n'.format(expected_param)
            attachments = [{'text': attachment_text }]
            return text,attachments
        return None,None

    @staticmethod
    def _get_graph(graph_name):
        return Lambda_Graph().get_gs_graph___by_name(graph_name)

    @staticmethod
    def _save_graph(graph):
        graph.reset_puml().render_puml()                        # re-render puml
        return Lambda_Graph().save_gs_graph(graph)              # save graph and return new graph name

    @staticmethod
    def add_edge(params):
        (text, attachments) = Nodes._check_params(params, ['Graph Name', 'Key (from)', 'link_type', 'Key (to)'])
        if text: return text, attachments

        graph_name , from_key , link_type , to_key = params

        link_type = link_type.replace('_',' ')                  # replace _ with a space in the link_type (since we can't pass the link_value with spaces due to the way the slack command parsing occurs)

        graph     = Nodes._get_graph(graph_name)                # get graph from elk
        graph.add_nodes([from_key,to_key])                      # add from and to nodes (in case they don't already exi
        graph.add_edge(from_key, link_type, to_key)             # add edge
        new_graph = Nodes._save_graph(graph)                    # save graph
        return 'added edge (`{0},{1},{2}`) to new graph `{3}`'.format(from_key,link_type,to_key, new_graph),[]

    @staticmethod
    def add_node(params):
        (text,attachments) = Nodes._check_params(params,['Graph Name','Jira Key'])
        if text: return text,attachments

        graph_name = params.pop(0)
        jira_key   = params.pop(0)

        graph = Nodes._get_graph(graph_name)
        graph.nodes.append(jira_key)
        new_graph = Nodes._save_graph(graph)
        return 'added node: `{0}` to new graph called `{1}`, which now has `{2}` nodes'.format(jira_key,new_graph,len(graph.nodes)),[]

    @staticmethod
    def list(params):
        (text, attachments) = Nodes._check_params(params, ['Graph Name'])
        if text: return text, attachments

        (graph_name) = params
        graph = Nodes._get_graph(graph_name)
        nodes_text = ''
        if graph:
            for node in graph.nodes:
                nodes_text += '{0}\n'.format(node)
            return "Here are the `{0}` nodes for the graph `{1}` \n```{2}```".format(len(graph.nodes),graph_name,nodes_text),[]
        return ":red_circle: graph not found: `{0}`".format(graph_name), []

    @staticmethod
    def list_edges(params):
        (text, attachments) = Nodes._check_params(params, ['Graph Name'])
        if text: return text, attachments

        (graph_name) = params
        graph = Nodes._get_graph(graph_name)
        edges_text = ''
        if graph:
            for edge in graph.edges:
                edges_text += '{0}\n'.format(edge)
            return "Here are the `{0}` edges for the graph `{1}` \n```{2}```".format(len(graph.edges), graph_name,
                                                                                     edges_text), []
        return ":red_circle: graph not found: `{0}`".format(graph_name), []

    @staticmethod
    def remove_link(params):
        (text, attachments) = Nodes._check_params(params, ['Graph Name', 'Link type'])
        if text: return text, attachments

        (graph_name, link_type) = params
        link_types = link_type.replace('_', ' ').split(',')
        graph     = Nodes._get_graph(graph_name)
        for link_type in link_types:
            graph.remove_link_type(link_type)
        graph.remove_no_links()
        new_graph = Nodes._save_graph(graph)
        return 'removed link type: `{0}`  from `{1}` and created new graph called `{2}`, which now has `{3}` nodes and `{4}` edges'.format(link_types, graph_name, new_graph, len(graph.nodes), len(graph.edges)), []

    # @staticmethod
    # def remove_no_links(params):
    #     (text, attachments) = Nodes._check_params(params, ['Graph Name'])
    #     if text: return text, attachments
    #
    #     (graph_name) = params
    #     graph = Nodes._get_graph(graph_name)
    #     graph.remove_no_links()
    #     new_graph = Nodes._save_graph(graph)
    #     return 'removed nodes with no links from `{0}` and created new graph called `{1}`, which now has `{2}` nodes and `{3}` edges'.format(
    #             graph_name, new_graph, len(graph.nodes), len(graph.edges)), []

    @staticmethod
    def remove_node(params):
        (text, attachments) = Nodes._check_params(params, ['Graph Name', 'Jira Key'])
        if text: return text, attachments

        (graph_name,keys) = params
        graph = Nodes._get_graph(graph_name)
        for key in keys.split(','):
            graph.remove_node_and_its_childen(key)
        new_graph = Nodes._save_graph(graph)
        return 'removed node(s): `{0}` (and its children) from `{1}` and created new graph called `{2}`, which now has `{3}` nodes and `{4}` edges'.format(key, graph_name, new_graph, len(graph.nodes),len(graph.edges)), []

    @staticmethod
    def stats(params):
        (text,attachments) = Nodes._check_params(params,['Graph Name'])
        if text is None:
            graph_name  = params.pop(0)
            graph       = Nodes._get_graph(graph_name)
            text        = "Here are the stats for the graph `{0}`".format(graph_name)
            attachments = [ { "text" : "*{0}x Nodes:* \n{1}".format(len(graph.nodes), pprint.pformat(graph.nodes))},
                            { "text" : "*{0}x Edges:* \n{1}".format(len(graph.edges), pprint.pformat(graph.edges))}]
        return text,attachments
