import json

from osbot_utils.decorators.lists.index_by import index_by

#from osbot_jira.api.API_Issues          import API_Issues
from osbot_jira.api.graph.GS_Graph_Puml import GS_Graph_Puml
from osbot_jira.api.plantuml.Puml import Puml
from osbot_jira.osbot_graph.Graph import Graph
from osbot_utils.utils.Files import Files
from osbot_utils.utils.Json import Json


class Jira_Graph:
    def __init__(self):
        #self.api_issues            = API_Issues()
        self.puml                  = Puml().startuml()
        self.puml_options          = {
                                        'node-text-value'     : "Summary",
                                        'only-from-projects'  : []       ,
                                        'link-types-to-add'   : []       ,
                                        'link-types-to-ignore': []       ,
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

        #self.risk_links_paths_down       = [  'is affected by', 'Requires'     , 'is used by', 'delivered by' , 'causes'       , 'is Technical Owner' , 'is Management Owner' , 'is Business Owner' , 'RISK affects', 'is fixed by', 'is mitigated by', 'is created by VULN', 'risk reduced by', 'is Vulnerable to'   , 'has VULN'    , 'RISK supported by', 'VULN is created by', 'is Stakeholder' , 'is parent of', 'is manager of', 'is created by R2', 'is created by R3', 'is created by R4']
        #self.risk_links_paths_up         = [  'affects'       ,'Is Required by', 'uses'      , 'delivers'     , 'is caused by' , 'has Technical Owner', 'has Management Owner', 'has Business Owner', 'has RISK'    , 'fixes'      , 'mitigates'      , 'creates RISK'      , 'reduces risk of', 'is Vulnerability of', 'VULN affects', 'supports RISK'    , 'creates VULN'      , 'has Stakeholder', 'is child of' , 'is managed by', 'creates R1'      , 'creates R2'      , 'creates R3'      ]

        #, 'has to be done before',
        #, 'has to be done after',
        # self.link_paths_other            = [ 'is blocked by','VULNThreat is created by', 'is budget item', 'Failure Implicated by',
        #                                      'Data touches', 'Data sources used in', 'Needs','relates to', 'Missing High','Is missing',
        #                                      'has budget item',   'Has VULNThreat', 'Is Needed by', 'Present', 'requires answer to ',
        #                                      'Missing From (high)','Is Required by' , 'is cloned by', 'Data sources', 'duplicates',
        #                                      'blocks', 'Implicates Failure of', 'clones', 'is duplicated by', 'System used for','is answer to' ]
        # self.link_paths_mappings         = { 'r0_up'            : ['creates VULN'       , 'has RISK'    ,'creates RISK'    ,'creates R3'       , 'creates R2'      ,'creates R1'      ,'creates RISK'      ,'creates VULN'      ],
        #                                      'r0_down'          : ['VULN is created by' ,                                   'is created by R4' , 'is created by R3','is created by R2','is created by VULN','VULN is created by'],
        #                                      'risks_up'         : ['creates VULN'       ,'fixes'        ,'reduces risk of' ,'has RISK'    ,'creates RISK','creates R3'       , 'creates R2'      ,'creates R1'      ],
        #                                      'risks_down'       : ['VULN is created by' , 'is fixed by', 'risk reduced by' ,'RISK affects',               'is created by R4' , 'is created by R3','is created by R2'],
        #                                      'stakeholders_up'  : ['has Technical Owner', 'has Management Owner', 'has Business Owner', 'has Stakeholder', 'is managed by'],
        #                                      'stakeholders_down': ['is Technical Owner' , 'is Management Owner' , 'is Business Owner' , 'is Stakeholder' , 'is manager of']}


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

    # this needs to be refactored and improved (since there are now more than 10k issues)
    # and this is called by the .add_all_linked_issues method
    def all_link_types_per_key(self):
        link_types = self.all_link_types()

        result = {}
        for link_type, data in link_types.items():
            for key, items in data.items():
                if result.get(key)            is None : result[key] = {}
                if result[key].get(link_type) is None : result[key][link_type] = []
                result[key][link_type] += items
        return result

    def add_all_linked_issues(self, keys=None, depth = 1):
        if keys is None:
            keys = []
        self.expand_link_types_to_add()
        link_types_per_key   = self.all_link_types_per_key()        # this needs to be refactored and improved (since there are now more than 10k issues)
        only_from_projects   = self.puml_options['only-from-projects']
        link_types_to_add    = self.puml_options['link-types-to-add' ]
        link_types_to_ignore = self.puml_options['link-types-to-ignore']
        self.add_nodes(keys)
        for i in range(0,depth):
            for key in list(self.nodes):
                data = link_types_per_key.get(key)
                if data:
                    for issue_type, items in data.items():
                        for item in items:
                            if only_from_projects   and item.split('-').pop(0) not in only_from_projects  : continue
                            if link_types_to_add    and issue_type             not in link_types_to_add   : continue
                            if link_types_to_ignore and issue_type             in     link_types_to_ignore: continue
                            self.add_edge(key, issue_type, item)
                            self.add_node(item)
        return self

    def add_linked_issues_of_types(self, link_types):
        for link_type in link_types:
            self.add_linked_issues_of_type(link_type)
        return self

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

    def add_nodes_from_epics(self):
        issues = self.get_nodes_issues()
        self.api_issues.set_default_indexes()
        for key, issue in issues.items():
            if issue and issue.get('Issue Type') == 'Epic':
                for epic_key in self.api_issues.epic_issues(key):
                    self.add_edge(key, 'epic issue', epic_key)
                    self.add_node(epic_key)
        return self

    def edges__link_types(self):
        return sorted(list(set([edge[1] for edge in self.edges])))

    def expand_link_types_to_add(self):
        link_types_to_add = self.puml_options['link-types-to-add']
        extra_link_types = []
        for link in link_types_to_add:
            extra_links = self.link_paths_mappings.get(link)
            if extra_links:
                extra_link_types.extend(extra_links)
        link_types_to_add.extend(extra_link_types)
        self.puml_options['link-types-to-add'] = link_types_to_add
        return self

    def get_graph_data(self):
        return { "nodes": self.get_nodes_issues(True),
                 "edges" : self.edges}
    @index_by
    def get_issues(self,reload=False):                          # better name for the method
        return list(self.get_nodes_issues(reload).values())

    def get_nodes_issues(self,reload=False):                    # depreciate
        if self.issues is None or reload is True:
            self.issues = self.api_issues.issues(self.nodes)
        return self.issues

    def get_puml             (self):
        return self.puml.puml

    def graph(self):
        return Graph().add_nodes(self.nodes) \
                      .add_edges(self.edges)

    def issues__values_by_field(self, field_name):
        results = []
        issues = self.get_nodes_issues()
        for node in self.nodes:
            issue = issues.get(node)
            if issue:
                results.append(issue.get(field_name))
        return list(set(results))

    def issues__issue_types(self):
        return self.issues__values_by_field('Issue Type')


    # this needs to be refactored since it is quite an expensive call (invoked quite often)
    def all_link_types(self, index = "all"):
        if self._link_types is None:
            self._link_types = self.api_issues.link_types(index)
        return self._link_types

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
        issues = self.get_nodes_issues()
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

        # node_text_value = self.puml_options['node-text-value' ]
        #
        # if self.puml_options['left-to-right']: self.puml.add_line('left to right direction')
        # if self.puml_options['width'        ]: self.puml.add_line('scale {0} width '.format(self.puml_options['width' ]))
        # if self.puml_options['height'       ]: self.puml.add_line('scale {0} height'.format(self.puml_options['height']))
        #
        # if self.issues is None:
        #     self.issues =  self.get_nodes_issues()
        # for key in self.nodes:
        #     if node_text_value is None:
        #         self.puml.add_card(key, key)
        #     else:
        #         issue = self.issues.get(key)
        #         if issue:
        #             key_text = issue.get(node_text_value)   #[0:30]
        #             if self.puml_options['show-key-in-text']:
        #                 line = '{1} \\n<font:10><i>{0}</i></font>'.format(key,key_text)
        #                 if self.node_type.get(key):
        #                     self.puml.add_node(self.node_type.get(key),line, key)
        #                 else:
        #                     self.puml.add_card(line, key)
        #             else:
        #                 line = '{0}'.format(key_text)
        #                 if self.node_type.get(key):
        #                     self.puml.add_node(self.node_type.get(key), line, key)
        #                 else:
        #                     self.puml.add_card(line, key)
        #         else:
        #             self.puml.add_card(key, key)
        #
        # for edge in self.edges:
        #     from_key  = edge[0]
        #     link_type = edge[1]
        #     to_key    = edge[2]
        #     if self.puml_options['show-edge-labels'] is False:
        #         link_type = ""
        #     self.puml.add_edge(from_key, to_key, 'down', link_type)
        #
        # for note in self.notes:
        #     position = note[0]
        #     key      = note[1]
        #     text     = note[2]
        #     line     = "\n\n\t note {0} of {1} \n {2} \n end note".format(position, key, text)
        #     self.puml.add_line(line)
        #
        # self.puml.add_line('')
        # for skin_param in self.skin_params:
        #     line = "skinparam {0} {1}".format(skin_param[0],skin_param[1])
        #     self.puml.add_line(line)
        #
        # self.puml.enduml()
        #return self.puml

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
            data['issues'] = self.get_nodes_issues()

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
    def set_puml_only_from_projects (self,value        ): self.puml_options['only-from-projects'  ] = value             ; return self
    def set_puml_link_types_to_add  (self,value        ): self.puml_options['link-types-to-add'   ] = value             ; return self
    def set_puml_left_to_right      (self,value        ): self.puml_options['left-to-right'       ] = value             ; return self
    def set_puml_direction_top_down (self              ): self.puml_options['left-to-right'       ] = False             ; return self
    def set_puml_show_key_in_text   (self,value        ): self.puml_options['show-key-in-text'    ] = value             ; return self
    def set_puml_show_edge_labels   (self,value        ): self.puml_options['show-edge-labels'    ] = value             ; return self
    def set_puml_width              (self,value        ): self.puml_options['width'               ] = value             ; return self
    def set_puml_height             (self,value        ): self.puml_options['height'              ] = value             ; return self
    def set_puml_on_add_node        (self, callback    ): self.puml.set_on_add_node(callback)                           ; return self
    def set_links_path_mode_to_down (self              ): self.set_puml_link_types_to_add(self.risk_links_paths_down)   ; return self
    def set_links_path_mode_to_up   (self              ): self.set_puml_link_types_to_add(self.risk_links_paths_up  )   ; return self
    def set_nodes_and_edges         (self, nodes, edges): self.nodes = nodes; self.edges = edges                        ; return self
    def set_link_paths_to_ignore    (self, value       ): self.puml_options['link-types-to-ignore'] = value             ; return self
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
        # if issues is None:
        #     issues = {}
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


    # LEGACY (Check and delete)

    def create_sub_graph_from_start_node(self, graph_nodes, start_node, issue_types_paths):
        issues = self.api_issues.issues(graph_nodes)
        link_types = self.api_issues.link_types_from_issues(issues.values(), graph_nodes)

        self.issues = issues
        self._link_types = link_types
        self.puml_options['left-to-right'] = True
        self.puml.add_line("scale 1")
        self.add_node(start_node)
        self.add_linked_issues_of_types(issue_types_paths)

        self.render_puml()