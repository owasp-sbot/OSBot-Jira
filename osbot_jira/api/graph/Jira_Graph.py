import json
from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from osbot_utils.decorators.lists.index_by import index_by

from osbot_jira.api.graph.GS_Graph_Puml import GS_Graph_Puml
from osbot_jira.api.plantuml.Puml import Puml
from osbot_jira.osbot_graph.Graph import Graph
from osbot_utils.utils.Files import Files
from osbot_utils.utils.Json import Json

# this is very similar to the GS_Graph class, but loads data directly from Jira instead of ElasticSearch
class Jira_Graph:
    def __init__(self):
        self.api_jira              = API_Jira_Rest()
        self.puml                  = Puml().startuml()
        self.puml_options          = {
                                        'node-text-value'     : "Summary",
                                        'link-types-to-add'   : []       ,
                                        'left-to-right'       : True     ,
                                        'show-key-in-text'    : True     ,
                                        'show-edge-labels'    : True     ,
                                        'width'               : None     ,
                                        'height'              : None
                                      }
        self.nodes                 = []
        self.edges                 = []
        self.issues                = None
        self._link_types           = None
        self.use_cache             = False
        self.notes                 = []
        self.node_type             = {}
        self.skin_params           = []
        self.create_params         = []

    def add_issue(self, key, issue):
        if issue:
            if self.issues is None:
                self.issues = {}
            self.issues[key] = issue

    def add_node(self, key,issue=None):
        if key not in self.nodes:
            self.nodes.append(key)
            self.add_issue(key,issue)
        return self

    def add_nodes(self, keys):
        for key in keys:
            self.add_node(key)
        return self

    def add_edge(self, from_key, link_type, to_key):
        edge = (from_key, link_type, to_key)
        if edge not in self.edges:
            self.edges.append(edge)                      # this operation is very expensive with 10k+ edges (I wonder how does pydot performance looks like
        return self

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

    def add_all_linked_issues(self, keys=None, depth = 1):
        if keys is None:
            keys = []
        link_types_to_add    = self.puml_options['link-types-to-add' ]                                  # get mapping of link types to add
        self.add_nodes(keys)                                                                            # add extra nodes provided in method param (to the nodes that already exist in the graph)
        for i in range(0,depth):                                                                        # loop the amount defined in depth
            link_types_per_key = self.jira_get_link_types_for_existing_nodes()
            for key in list(self.nodes):                                                                # for each key in the current nodes
                data = link_types_per_key.get(key)                                                      # get the
                if data:
                    for issue_type, items in data.items():
                        for item in items:
                            if link_types_to_add    and issue_type             not in link_types_to_add   : continue
                            self.add_edge(key, issue_type, item)
                            self.add_node(item)
        return self

    def add_linked_issues_of_types(self, link_types):
        for link_type in link_types:
            self.add_linked_issues_of_type(link_type)
        return self

    # todo: needs fixing since all_link_types doesn't exist anymore
    def add_linked_issues_of_type(self, link_type):
        link_type = link_type.strip()                                       # remove any spaces
        mappings = self.all_link_types().get(link_type)
        if mappings:
            for key in list(self.nodes):                                    # for each key provided (it is important to pin the self.nodes here since that value is changed below)
                linked_issues = mappings.get(key)
                if linked_issues:
                    for linked_issue in linked_issues:
                        edge = (key, link_type, linked_issue)
                        if not edge in self.edges:
                            self.edges.append(edge)
                            self.nodes.append(linked_issue)
        return self

    # todo: needs fixing since api_issues doesn't exist in this class
    def add_link_types_as_nodes(self, issue_types_to_ignore=None):
        if issue_types_to_ignore is None:
            issue_types_to_ignore = []
        if self.issues is None:
            self.issues = self.api_issues.issues(self.nodes)
        issue_types_to_ignore.append('_all')
        for key in self.nodes:
            issue = self.issues.get(key)
            if issue:
                for link_type, items in issue['Issue Links'].items():
                    if link_type not in issue_types_to_ignore:
                        link_type_node_key = "{0} - {1}".format(key,link_type)
                        for item in items:
                            self.add_edge(key, "", link_type_node_key)
                            self.add_edge(link_type_node_key , "" , item)
        return self

    # def add_nodes_from_epics(self):
    #     issues = self.jira_get_nodes_issues()
    #     self.api_issues.set_default_indexes()
    #     for key, issue in issues.items():
    #         if issue and issue.get('Issue Type') == 'Epic':
    #             for epic_key in self.api_issues.epic_issues(key):
    #                 self.add_edge(key, 'epic issue', epic_key)
    #                 self.add_node(epic_key)
    #     return self

    def edges__link_types(self):
        return sorted(list(set([edge[1] for edge in self.edges])))

    def get_graph_data(self):
        return { "nodes": self.jira_get_nodes_issues(True),
                 "edges" : self.edges}
    @index_by
    def jira_get_issues(self,reload=False,fields=None):                          # better name for the method
        return list(self.jira_get_nodes_issues(reload=reload, fields=fields).values())

    def jira_get_nodes_issues(self,reload=False, fields=None):
        if self.issues is None or reload is True:
            self.issues = self.api_jira.issues(issues_ids=self.nodes, fields=fields)
        else:
            # if we already have some issues fetched see if we have data for all of them
            missing_nodes = []
            for node_id in self.nodes:
                if node_id not in self.issues:
                    missing_nodes.append(node_id)
            if len(missing_nodes) > 0:
                missing_issues = self.api_jira.issues(issues_ids=missing_nodes, fields=fields)
                self.issues.update(missing_issues)

        return self.issues

    def get_puml             (self):
        return self.puml.puml

    def graph(self):
        return Graph().add_nodes(self.nodes) \
                      .add_edges(self.edges)

    def issues__values_by_field(self, field_name):
        results = []
        issues = self.jira_get_nodes_issues()
        for node in self.nodes:
            issue = issues.get(node)
            if issue:
                results.append(issue.get(field_name))
        return list(set(results))

    def issues__issue_types(self):
        return self.issues__values_by_field('Issue Type')

    def jira_get_link_types_for_existing_nodes(self, reload=False):              # in most calls of this method there are new nodes, and we want to make sure that we get the missing nodes
        issues_links = {}
        jira_issues_links = self.jira_get_issues(reload=reload, fields='issuelinks')

        for issue in jira_issues_links:
            key         = issue.get('Key')
            issue_links = issue.get('Issue Links')
            issues_links[key] = issue_links
        return issues_links

    def set_link_types_from_issues(self, issues):
        self._link_types = self.api_issues.link_types_from_issues(issues.values(),issues.keys())
        return self

    def load(self, path):
        data = Json.load_file(path)
        if data:
            self.nodes = data['nodes']
            self.edges = data['edges']
        return self

    def nodes__ratings(self):
        return self.nodes__field_values('Rating')

    def nodes__field_values(self,field):
        values = []
        issues = self.jira_get_nodes_issues()
        for node in self.nodes:
            issue = issues.get(node)
            if issue:
                value = issue.get(field)
                if value:
                    values.append(value)
        return sorted(list(set(values)))

    def remove_link_type(self, link_type_to_remove):
        for edge in list(self.edges):                       # create new list so that it is not affected by the remove action
            (from_key, link_type, to_key) = edge
            if link_type in link_type_to_remove:
                self.edges.remove(edge)
        return self

    def remove_no_links(self):
        nodes_with_links    = []
        nodes_with_no_links = []

        for edge in list(self.edges):                       # get list of all nodes that have an edge
            (from_key, link_type, to_key) = edge
            nodes_with_links.append(from_key)
            nodes_with_links.append(to_key)

        for key in self.nodes:                              # diff it with the current list of nodes
            if key not in nodes_with_links:
                nodes_with_no_links.append(key)

        self.remove_nodes(nodes_with_no_links)              # remove nodes

        return self

    def remove_with_links(self):
        nodes_with_links    = []

        for edge in list(self.edges):                       # get list of all nodes that have an edge
            (from_key, link_type, to_key) = edge
            nodes_with_links.append(from_key)
            nodes_with_links.append(to_key)

        new_nodes = []
        for key in self.nodes:                              # only add the nodes that are not in the
            if key not in nodes_with_links:                 # nodes_with_links array
                new_nodes.append(key)

        self.nodes = new_nodes
        self.edges = []

        return self

    # replace with filter only_edges_with_both_nodes
    def remove_no_links_with_no_nodes(self):
        new_edges = []
        nodes = self.nodes
        for edge in list(self.edges):
            if edge[0] in nodes and edge[2] in nodes:       # if both edges exist in the current list of nodes
                new_edges.append(edge)                    # keep the edge
        self.edges = new_edges
        return self

    def remove_node(self,key):
        if key in self.nodes:
            self.nodes.remove(key)
            for edge in list(self.edges):
                (from_key, link_type, to_key) = edge
                if from_key == key or to_key == key:
                    self.edges.remove(edge)
        if self.issues and self.issues.get(key) is not None:
            del self.issues[key]
        return self

    def remove_nodes(self, keys):
        for key in keys:
            self.remove_node(key)
        return self

    def remove_node_and_its_childen(self,key):
        nodes_to_remove = [key]

        for edge in list(self.edges):
            (from_key, link_type, to_key) = edge
            if from_key in nodes_to_remove:                 # check if there are blind spots in this logic
                nodes_to_remove.append(to_key)
        print('nodes_to_remove: {0}'.format(nodes_to_remove))
        self.remove_nodes(nodes_to_remove)
        return self

    def save(self, path=None):
        if path is None: path = Files.temp_file('graph.json')
        data = { 'nodes': self.nodes, 'edges': self.edges }
        return Json.save_file_pretty(path, data)

    def render_and_save_to_elk(self, graph_name=None, graph_type=None, channel= None, user = None):      # might need to move this to a Lambda function
        from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph                                       # todo: find out why this needs to be here of it fail to load the dependency (could be caused by a cyclic dependency)
        lambda_graph = Lambda_Graph()
        graph_name = lambda_graph.save_gs_graph(self, graph_name, graph_type, channel, user)
        if lambda_graph.wait_for_elk_to_index_graph(graph_name):                                         # wait for ELK to index the graph (to prevent a fetch before the data is available in ELK)
            return graph_name
        return None


    def render_puml(self):
        self.reset_puml()
        return GS_Graph_Puml(self).render_puml()

    def render_puml_and_save_tmp(self):
        self.render_puml()
        return self.puml.save_tmp()

    def render_puml_save_to_elk_and_to_tmp(self, graph_name=None):
        self.render_and_save_to_elk(graph_name)
        return self.puml.save_tmp()

    def reset_puml(self):
        self.puml.puml = "@startuml\n"
        return self

    def to_json(self, puml_config=True, store_issues=False):
        if puml_config:
            data = {
                        "nodes"        : self.nodes         ,
                        "edges"        : self.edges         ,
                        "notes"        : self.notes         ,
                        "node_type"    : self.node_type     ,
                        "skin_params"  : self.skin_params   ,
                        "create_params": self.create_params ,
                        "puml_options" : self.puml_options  ,
                        "puml_config"  : True               }
        else:
            data = {    "nodes": self.nodes                 ,
                        "edges": self.edges                 }
        if store_issues:
            data['issues'] = self.jira_get_nodes_issues()

        return json.dumps(data)

    def from_json(self, json_data):
        data = json.loads(json_data)
        if data.get('puml_config') is True:
            self.nodes          = data.get("nodes")
            self.edges          = data.get("edges")
            self.notes          = data.get("notes")
            self.node_type      = data.get("node_type")
            self.skin_params    = data.get("skin_params")
            self.create_params  = data.get("create_params")
            self.puml_options   = data.get("puml_options")
        else:
            self.nodes = data.get("nodes")
            self.edges = data.get("edges")

        self.issues = data.get('issues')
        return self


    def set_puml_node_text_value    (self,value        ): self.puml_options['node-text-value'     ] = value             ; return self
    def set_puml_link_types_to_add  (self,value        ): self.puml_options['link-types-to-add'   ] = value             ; return self
    def set_puml_left_to_right      (self,value        ): self.puml_options['left-to-right'       ] = value             ; return self
    def set_puml_direction_top_down (self              ): self.puml_options['left-to-right'       ] = False             ; return self
    def set_puml_show_key_in_text   (self,value        ): self.puml_options['show-key-in-text'    ] = value             ; return self
    def set_puml_show_edge_labels   (self,value        ): self.puml_options['show-edge-labels'    ] = value             ; return self
    def set_puml_width              (self,value        ): self.puml_options['width'               ] = value             ; return self
    def set_puml_height             (self,value        ): self.puml_options['height'              ] = value             ; return self
    def set_puml_on_add_node        (self, callback    ): self.puml.set_on_add_node(callback)                           ; return self
    def set_nodes_and_edges         (self, nodes, edges): self.nodes = nodes; self.edges = edges                        ; return self
    def set_skin_param              (self, name, value ): self.skin_params.append((name, value))                        ; return self
    def set_create_params           (self, value       ): self.create_params = value                                    ; return self
    def set_edges                   (self, edges       ): self.edges         = edges                                    ; return self
    def set_nodes                   (self, nodes       ): self.nodes         = nodes                                    ; return self

    def stats(self):
        return  {
                 "count_nodes" : len(self.nodes    ),
                 "count_edges" : len(self.edges    ),
                 "size_puml"   : len(self.puml.puml)
                }

    def filter(self):
        from osbot_jira.api.graph.Filters import Filters
        return Filters().setup(graph=self)

    # view

    def view_nodes(self,label_key=None,show_key=False, key_id='id', label_id='label'):
        nodes = []
        issues = self.issues or {}
        for key in self.nodes:
            issue = issues.get(key)
            if issue and label_key is not None:
                label = issue.get(label_key)
                if label is None:
                    label = key
                if show_key:
                    label = f'{key} - {label}'
            else:
                label = key
            nodes.append({key_id: key, label_id: label})
        return nodes

    def view_nodes_and_edges(self,label_key=None,show_key=False):

        nodes = self.view_nodes(label_key, show_key)
        edges = []

        for edge in self.edges:
            edges.append({'from': edge[0], 'to': edge[2]})

        return nodes,edges