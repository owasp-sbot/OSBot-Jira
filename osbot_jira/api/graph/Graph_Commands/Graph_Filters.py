from time import sleep

from pbx_gs_python_utils.utils.Lambdas_Helpers  import slack_message
from pbx_gs_python_utils.utils.Misc             import Misc
from osbot_aws.apis.Lambda           import Lambda

from osbot_jira.api.graph.GS_Graph import GS_Graph
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph


class Graph_Filters:
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
        if graph:
            graph.reset_puml().render_puml()                        # re-render puml
            return Lambda_Graph().save_gs_graph(graph)              # save graph and return new graph name

    @staticmethod
    def _get_graph_from_params(team_id, channel, params):
        if len(params) <2:
            text = ':red_circle: For this command, you need to provide two parameters: `graph_name` and `link types` (can be comma delimited)'
            slack_message(text, [], channel, team_id)
            return None,None,None
        graph_name = params.pop(0)
        params = " ".join(params).split(',')
        return graph_name, Graph_Filters._get_graph(graph_name), params

    @staticmethod
    def _save_graph_and_send_slack_message(team_id, channel, graph, graph_name):
        if channel and team_id:
            new_graph_name = Graph_Filters._save_graph(graph)
            text = ':point_right: Created new graph called `{0}` with `{1}` nodes and `{2}` edges (based on data from graph `{3}`) ' \
                        .format(new_graph_name, len(graph.nodes), len(graph.edges), graph_name)

            slack_message(text, [], channel, team_id)
            sleep(1)
            Lambda('lambdas.gsbot.gsbot_graph').invoke_async({"params": ["show", new_graph_name, "plantuml"], "data": {"channel": channel, "team_id": team_id}})
        return graph

    @staticmethod
    def only_with_issue_types(team_id, channel, params):
        (graph_name, graph, params) = Graph_Filters._get_graph_from_params(team_id, channel, params)

        new_nodes = []
        new_edges = []
        issues = graph.get_nodes_issues()
        for key, issue in issues.items():
            if issue:
                issue_type = issue.get('Issue Type')
                if issue_type in params:
                    new_nodes.append(key)

        for edge in graph.edges:
            from_key = edge[0]
            to_key  = edge[2]
            if from_key in new_nodes and to_key in new_nodes:
                new_edges.append(edge)

        graph.set_nodes(new_nodes).set_edges(new_edges)

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)

    @staticmethod
    def only_show_issue_types(team_id, channel, params):
        (graph_name, graph, params) = Graph_Filters._get_graph_from_params(team_id, channel, params)

        new_nodes = []
        issues = graph.get_nodes_issues()
        for key, issue in issues.items():
            if issue:
                issue_type = issue.get('Issue Type')
                if issue_type in params:
                    new_nodes.append(key)

        graph.set_nodes(new_nodes)  # this version as an interesting side effect since we are not removing the edges with no nodes

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)

    @staticmethod
    def only_with_link_types(team_id, channel, params):
        (graph_name,graph,params) = Graph_Filters._get_graph_from_params(team_id, channel, params)

        new_edges = []

        for index,edge in enumerate(graph.edges):
            link_type = edge[1]
            if link_type in params:
                new_edges.append(edge)

        graph.set_edges(new_edges).remove_no_links()

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)

    @staticmethod
    def only_with_ratings(team_id, channel, params):
        (graph_name, graph, params) = Graph_Filters._get_graph_from_params(team_id, channel, params)

        new_nodes = []
        issues = graph.get_nodes_issues()
        for key, issue in issues.items():
            issue_type = issue.get('Rating')
            if issue_type in params:
                new_nodes.append(key)

        graph.set_nodes(new_nodes)  # this version as an interesting side effect since we are not removing the edges with no nodes

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)

    # this filter will replace all edges with all links between the current nodes
    @staticmethod
    def only_links_between_nodes(team_id=None, channel=None, params=[]):
        (text, attachments) = Graph_Filters._check_params(params, ['Graph Name'])
        if text: return text, attachments
        graph_name  = params[0]
        graph       = Graph_Filters._get_graph(graph_name)
        graph.edges = []                                  # clear all edges from graphh

        if graph:
            issues = graph.get_nodes_issues().items()
            for key,issue in issues:
                issue_links = issue.get('Issue Links')
                for issue_link, targets in issue_links.items():
                    for target in targets:
                        if key in graph.nodes and target in graph.nodes:
                            graph.add_edge(key,issue_link,target)

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)

    @staticmethod
    def remove_issue_types(team_id, channel, params):
        (graph_name, graph, params) = Graph_Filters._get_graph_from_params(team_id, channel, params)

        new_nodes = []
        new_edges = []
        issues = graph.get_nodes_issues()
        for key, issue in issues.items():
            issue_type = issue.get('Issue Type')
            if issue_type not in params:
                new_nodes.append(key)

        for edge in graph.edges:
            from_key = edge[0]
            to_key  = edge[2]
            if from_key in new_nodes and to_key in new_nodes:
                new_edges.append(edge)

        graph.set_nodes(new_nodes).set_edges(new_edges)

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)

    @staticmethod
    def remove_link_types(team_id, channel, params):
        (graph_name,graph,params) = Graph_Filters._get_graph_from_params(team_id, channel, params)  # get graph object

        new_edges = []                                                                              # array to hold the new edges

        for index,edge in enumerate(graph.edges):                                                   # for each edge
            link_type = edge[1]                                                                     # get link_type from edge triplet: (from_node, link_type, to_node)
            if link_type not in params:                                                             # if link_type is NOT in the params passed
                new_edges.append(edge)                                                              # add edge from new_edges array

        graph.set_edges(new_edges).remove_no_links()                                                # update original graph with new edges and remove nodes with no links

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)       # save graph in ELK and send updates via Slack

    @staticmethod
    def remove_nodes_with_no_links(team_id, channel, params):
        (text, attachments) = Graph_Filters._check_params(params, ['Graph Name'])
        if text: return text, attachments
        graph_name = params[0]
        graph = Graph_Filters._get_graph(graph_name)
        if graph:
            graph.remove_no_links()
            return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)
        else:
            text = ':red_circle: Graph not found : {0}'.format(graph_name)
            slack_message(text,[], channel, team_id)

    @staticmethod
    def remove_nodes_with_links(team_id=None, channel=None, params=None):
        (text, attachments) = Graph_Filters._check_params(params, ['Graph Name'])
        if text: return text;

        graph_name = params[0]
        graph = Graph_Filters._get_graph(graph_name)

        if graph:

            graph.remove_with_links()               # main action (the rest is the same for most filters)

            return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)
        else:
            text = ':red_circle: Graph not found : {0}'.format(graph_name)
            slack_message(text, [], channel, team_id)

    @staticmethod
    def list_current_link_types(team_id, channel, params):
        (text, attachments) = Graph_Filters._check_params(params, ['Graph Name'])
        if text: return text, attachments
        graph_name = params[0]
        graph = Graph_Filters._get_graph(graph_name)
        link_types = []
        for edge in graph.edges:
            link_types.append(edge[1])
        text = 'Here are the current link types in the graph `{0}` '.format(graph_name)
        for name in list(set(link_types)):
            text += '\n\t\t • {0} '.format(name)
        slack_message(text, [], channel, team_id)


    # @use_local_cache_if_available
    # def offline_data(self,graph_name):
    #     graph = Graph_Filters._get_graph(graph_name)
    #     issues = graph.get_nodes_issues()
    #     return graph.nodes,graph.edges,issues



    @staticmethod
    def group_by_field(team_id=None, channel=None, params=None):
        if len(params) < 2:
            return slack_message(':red_circle: For this filter, you need to provide a `graph_name` and a `field` name: ', [], channel, team_id)


        graph_name = params.pop(0)
        field_name = ' '.join(params)

        slack_message(":point_right: Creating new graph using the `group_by_field` filter on the `{0}` field of the `{1}` graph".format(field_name,graph_name),[], channel, team_id)

        graph  = Graph_Filters._get_graph(graph_name)
        issues = graph.get_nodes_issues()
        nodes  = graph.nodes
        edges  = graph.edges
        graph  = GS_Graph()
        root_node = graph_name # nodes[0]
        graph.add_node(root_node)
        if field_name == 'Issue Links':
            for edge in edges:
                #from_key   = edge[0]
                link_type  = edge[1]
                to_key     = edge[2]
                #from_issue = Misc.get_value(issues,from_key,{})
                to_issue   = Misc.get_value(issues, to_key, {})
                #from_value = Misc.get_value(from_issue, field_name)
                to_summary = Misc.get_value(to_issue, 'Summary')
                to_key     = Misc.get_value(to_issue, 'Key'    )
                #to_value   = "{0} | {1}".format(to_summary,to_key)

                graph.add_node(link_type)
                graph.add_node(to_key)
                graph.add_edge(graph_name, '', link_type)
                graph.add_edge(link_type , '', to_key)

        else:
            for node in  nodes:
                issue = issues.get(node)
                if issue:
                    value = issue.get(field_name)
                    #if field_name == 'Issue Links':
                        # for link_name,issue_links in value.items():
                        #     for issue_link in issue_links:
                        #         graph.add_node(link_name)
                        #         graph.add_edge(root_node, field_name, link_name)
                        #         graph.add_edge(link_name, field_name, issue_link)
                        # pass
                    #else:
                    graph.add_node(node)
                    graph.add_edge(root_node, field_name, value)
                    graph.add_edge(value    ,  '' , node)

        return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)

    @staticmethod
    def search_by_field(team_id=None, channel=None, params=None):
        results = []
        (graph_name, graph, params) = Graph_Filters._get_graph_from_params(team_id, channel, params)
        if graph:                                    # todo : add better error handling for passing to correct params for the search
            params = params.pop()                     # todo : add better error handling for passing to correct params for the search
            issues = graph.get_nodes_issues()
            if "=" in params:
                field_name,value_to_find = "".join(params).split('=')
                for key,issue in issues.items():
                    if value_to_find.lower().strip() == issue.get(field_name.strip()).lower().strip():
                        results.append(key)
                        #results.append(issue.get(field_name))

            if "~" in params:
                field_name, value_to_find = "".join(params).split('~')
                #field_name = params.pop(0)
                for key, issue in issues.items():
                    if value_to_find.lower().strip() in issue.get(field_name.strip()).lower().strip():
                        results.append(key)
                        #results.append(issue.get(field_name))

            if "!" in params:
                field_name, value_to_find = "".join(params).split('!')
                #field_name = params.pop(0)
                for key, issue in issues.items():
                    if value_to_find.lower().strip() not in issue.get(field_name.strip()).lower().strip():
                        results.append(key)
                        #results.append(issue.get(field_name.strip()))
        if len(results) > 0:
            graph.set_nodes(results).remove_no_links_with_no_nodes()
            return Graph_Filters._save_graph_and_send_slack_message(team_id, channel, graph, graph_name)
        else:
            text = ':red_circle: no matches for the search query provided'
            slack_message(text, [], channel, team_id)

