class GS_Graph_Puml:

    edges    : list
    nodes    : list
    node_type: dict

    def __init__(self,graph):
        self.graph        = graph
        self.puml_options = graph.puml_options
        self.issues       = graph.issues
        self.nodes        = graph.nodes
        self.edges        = graph.edges
        self.notes        = graph.notes
        self.node_type    = graph.node_type

    def render_and_save_to_elk(self, graph_name=None, graph_type=None, channel= None, user = None):                                    # might need to move this to a Lambda function
        #from pbx_gs_python_utils.gs_elk.Lambda_Graph import Lambda_Graph
        from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph                                                                      # needs to be here of it fail to load the dependency (could be caused by a cyclic dependency)
        return Lambda_Graph().save_gs_graph(self.graph, graph_name, graph_type, channel, user)


    def render_puml(self):
        node_text_value = self.puml_options['node-text-value' ]

        if self.puml_options['left-to-right']: self.puml.add_line('left to right direction')
        if self.puml_options['width'        ]: self.puml.add_line('scale {0} width '.format(self.puml_options['width' ]))
        if self.puml_options['height'       ]: self.puml.add_line('scale {0} height'.format(self.puml_options['height']))

        if self.issues is None:
            self.issues =  self.graph.get_nodes_issues()
        for key in self.nodes:
            if node_text_value is None:
                self.puml.add_card(key, key)
            else:
                issue = self.issues.get(key)
                if issue:
                    key_text = issue.get(node_text_value)   #[0:30]
                    if self.puml_options['show-key-in-text']:
                        line = '{1} \\n<font:10><i>{0}</i></font>'.format(key,key_text)
                        if self.node_type.get(key):
                            self.puml.add_node(self.node_type.get(key),line, key)
                        else:
                            self.puml.add_card(line, key)
                    else:
                        line = '{0}'.format(key_text)
                        if self.node_type.get(key):
                            self.puml.add_node(self.node_type.get(key), line, key)
                        else:
                            self.puml.add_card(line, key)
                else:
                    self.puml.add_card(key, key)

        for edge in self.edges:
            from_key  = edge[0]
            link_type = edge[1]
            to_key    = edge[2]
            if self.puml_options['show-edge-labels'] is False:
                link_type = ""
            self.puml.add_edge(from_key, to_key, 'down', link_type)

        for note in self.notes:
            position = note[0]
            key      = note[1]
            text     = note[2]
            line     = "\n\n\t note {0} of {1} \n {2} \n end note".format(position, key, text)
            self.puml.add_line(line)

        self.puml.add_line('')
        for skin_param in self.skin_params:
            line = "skinparam {0} {1}".format(skin_param[0],skin_param[1])
            self.puml.add_line(line)

        self.puml.enduml()
        return self.puml

    def render_puml_and_save_tmp(self):
        self.render_puml()
        return self.puml.save_tmp()

    def render_puml_save_to_elk_and_to_tmp(self, graph_name=None):
        self.render_and_save_to_elk(graph_name)
        return self.puml.save_tmp()

    def reset_puml(self):
        self.puml = Puml().startuml()
        return self