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
        self.puml         = graph.puml
        self.skin_params  = graph.skin_params

    def render_puml(self, using_jira_nodes=True, reload_issues=False):
        node_text_value = self.puml_options['node-text-value' ]

        if self.puml_options['left-to-right']: self.puml.add_line('left to right direction')
        if self.puml_options['width'        ]: self.puml.add_line('scale {0} width '.format(self.puml_options['width' ]))
        if self.puml_options['height'       ]: self.puml.add_line('scale {0} height'.format(self.puml_options['height']))

        for skin_param in self.skin_params:
            line = "skinparam {0} {1}".format(skin_param[0], skin_param[1])
            self.puml.add_line(line)
        self.puml.add_line('')

        if using_jira_nodes is False:
            self.issues = {}
        else:
            if self.issues is None or reload_issues is True:            # only reload if the issue object is not set or reload_issues is set to True
                self.issues =  self.graph.get_nodes_issues()

        for key in self.nodes:
            if node_text_value is None:
                self.puml.add_card(key, key)
            else:
                issue = self.issues.get(key)
                if issue and type(issue) is dict:
                    key_text = issue.get(node_text_value)
                    if self.puml_options['show-key-in-text']:
                        line = f"={key_text}\\n<color:grey><size:10><i>{key}</i></size></color>"        # note: if getting weird formating errors take a look at Puml.max_title
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
            key      = self.puml.fix_id(note[1])
            text     = note[2]
            line     = f'\n\n\t note {position} of "{key}" \n {text} \n end note'
            self.puml.add_line(line)

        self.puml.enduml()
        self.graph.puml = self.puml
        return self.puml