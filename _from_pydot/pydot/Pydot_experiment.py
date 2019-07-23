from   API_GS_Jira import API_GS_Jira
from   utils.Dev import Dev
import pydot

class Map_Issue_Graph:
    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.gs_jira = API_GS_Jira()

    def issue(self):
        return self.gs_jira.issue(self.issue_id)

    def issue_links(self, issue_id):
        return self.gs_jira.issue(issue_id)['Issue Links']

    def issue_links_types(self, issue_id):
        links_types = {}
        for key,issue_link in self.gs_jira.issue(issue_id)['Issue Links'].items():
            link_type = issue_link['Link Type']
            if links_types.get(link_type) is None: links_types[link_type] = {}
            links_types[link_type][key] = issue_link
        return links_types

    def map_triplets(self, root_id, link_type_sequence):
        triplets = []

        def map_issue(issue_id, link_type):
            matches = self.issue_links_types(issue_id).get(link_type)
            if matches:
                for key, value in matches.items():
                    triplets.append((issue_id, link_type, key))
                return set(matches)
            return {}

        def map_issues(issues_ids, link_types):
            keys = []
            for link_type in link_types.split(','):
                for issue_id in issues_ids:
                    keys += map_issue(issue_id, link_type)
            return keys
        next_keys = [root_id]
        for link_types in link_type_sequence:
            next_keys = map_issues(next_keys, link_types)


        return triplets

    def create_graph_from_triplets(self, triplets):
        node_label = 'Issue Type' # 'Key'# 'Summary' #''Issue Type' #
        Dev.pprint('==== Creating GRAPH file =====')
        graph = pydot.Dot(graph_type='digraph')
        for item in triplets:
            issue_1 = self.gs_jira.issue(item[0])
            issue_2 = self.gs_jira.issue(item[2])
            node_1 = pydot.Node(item[0],shape='box' , label = '{1}'.format(issue_1[node_label][0:50], issue_1['Key']))

            label  = '  ' + item[1]
            node_2 = pydot.Node(item[2],shape='box' , label= '{1}'.format(issue_2[node_label][0:50], issue_2['Key']))

            edge = pydot.Edge(node_1,node_2, label=label   ,
                                             fontsize='9.0',
                                             color='blue'  ,
                                             labelfontcolor = '009933')

            edge.set_labelfontcolor("blue")  # not working
            graph.add_node(node_1)
            graph.add_node(node_2)
            graph.add_edge(edge)
        return graph

    def save_graph(self, graph):
        filename = '../../data/sec-9195/test_graph'
        graph.write_png(filename + '.png', prog='dot')
        return graph

    # def map_graph_using_pydot(self):
    #     graph = pydot.Dot(graph_type='graph')
    #
    #     def map_issue(issue_id):
    #
    #         graph.add_node(pydot.Node(issue_id))
    #         for link_id in self.gs_jira.issue(issue_id)['Issue Links']:
    #             graph.add_node(pydot.Node(link_id))
    #             graph.add_edge(pydot.Edge(self.issue_id,link_id))
    #             graph.add_edge(pydot.Edge(link_id, self.issue_id))
    #             graph.add_edge(pydot.Edge(link_id, self.issue_id))
    #
    #     #graph.add_node(pydot.Node('test'))
    #     #graph.add_node(pydot.Node('123'))
    #
    #     map_issue(self.issue_id)
    #     return graph
    # def map_graph(self):
    #
    #     graph = {}
    #     def map_issue(node , root_id):
    #         print("mapping: {0}".format(root_id))
    #         node[root_id] = {}
    #         links   = self.gs_jira.issue(root_id)['Issue Links']
    #
    #         for key,link in links.items():
    #             print("issue {0} links to {1} ({2})".format(root_id, key, link['Direction']))
    #             if link['Direction'] == 'Outward':
    #                 #print(link)
    #                 node[root_id][key] = map_issue({}, key)
    #                 #break
    #         return node
    #
    #     map_issue(graph, self.issue_id)
    #
    #     return graph

class Security_Story:
    def __init__(self, story_id):
        self.story_id = story_id
        self.gs_jira  = API_GS_Jira()
        self._issue   = None

    def find_all_issues_linked_from_story_id(self):
        def default_node():
            return { 'calls' : {} , 'is_called_by': {} }

        issues_Id  = {}

        issues_Id[self.story_id] = default_node()
        for id in set(self.issue()['Issue Links']):
            issues_Id[self.story_id]['calls'        ][id           ] = default_node()
            if issues_Id.get(id) is None: issues_Id[id]= default_node()
            issues_Id[id            ]['is_called_by'][self.story_id] = default_node()

        return []

    def issue(self):
        if self._issue is None:
            self._issue = self.gs_jira.issue(self.story_id)
        return self._issue

    def stakeholders(self):
        results = {}
        for key,linked_issue in self.issue()['Issue Links'].items():
            if linked_issue['Link Type'] == 'has Stakeholder':
                results[key] = self.gs_jira.issue(key)
        return results