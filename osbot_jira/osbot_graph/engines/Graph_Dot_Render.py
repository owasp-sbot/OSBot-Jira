LEFT_PADDING  = '             '      # using spaces instead of tabs ('/t') creates more consistent results
#DIGRAPH_START = 'digraph G { \n'
DIGRAPH_END   = '          }'        # todo: fix padding for sub-graphs

class Graph_Dot_Render:
    def __init__(self, graph, sub_graphs, graph_name='G', graph_type='digraph'):
        self.graph_name      = graph_name
        self.graph_type      = graph_type
        self.dot_code        = ""
        self.extra_dot_code  = ""
        self.label           = ""
        self.node_params     = {}
        self.concentrate     = None
        self.size            = None
        self.rank_dir        = None
        self.rank_sep        = None
        self.ranks           = {}
        self.graph           = graph
        self.sub_graphs      = sub_graphs
        pass
        #self.graph_dot = graph_dot

    # helpers

    def join_params(self,params):
        return ' '.join([f'{key}="{value}"' for key, value in params.items()])

    def parse_into_params(self, source, skip_names):
        params = ""
        for param_name,param_value in source.items():
            if param_name in skip_names   : continue
            if param_value:
                params += f'{param_name}="{param_value}" '

        return params

    def edge_link(self, edge_node):     # add support for record shape linking in edges
        if ':' in edge_node:
            items = edge_node.split(':')            # todo: refactor how this is done
            return f'"{items[0]}":"{items[1]}"'
        else:
            return f'"{edge_node}"'

    # render main

    def render(self):
        self.dot_code = f'{self.graph_type} {self.graph_name} {{'
        (
            self.add_rand_dir()
                .add_rank_sep()
                .add_size()
                .add_label()
                .add_node_params()
                .add_concentrate()
                .add_sub_graphs()
         )
        self.add_line().add_comment ('###### Nodes #######')
        for node in self.graph.nodes():
            key    = node.get('key')
            label  = node.get('value') or key
            params = self.parse_into_params(node, ['key'])

            if params:
                self.add_line(f'"{key}" [{params}]')
            else:
                self.add_line(f'"{key}" ["label"="{label}"]')

        self.add_line().add_comment('###### Edges #######')

        for edge in self.graph.edges():
            from_key = self.edge_link(edge.get('from'))
            to_key   = self.edge_link(edge.get('to'))
            params = self.parse_into_params(edge, ['from','to'])
            self.add_line(f' {from_key} -> {to_key} [{params}]')

        (self.add_ranks()
             .add_extra_dot_code())

        self.dot_code += DIGRAPH_END
        return self.dot_code

    def add_sub_graphs(self):
        for sub_graph in self.sub_graphs:
            self.add_line().add_line(sub_graph.render.render())
        return self


    # render methods

    def add_concentrate(self):
        if self.concentrate:
            self.add_line('concentrate=true')
        return self
    def add_extra_dot_code(self):
        if self.extra_dot_code:
            self.dot_code += self.extra_dot_code
        return self

    def add_label(self):
        if self.label:
            self.add_line(f'label="{self.label}";')    \
                .add_line('labelloc = "t"')            # default to put label at the top
        return self

    def add_line(self, value=''):                      # todo: refactor all add_*** methods into separate 'build' class
        self.dot_code += f'{LEFT_PADDING}{value} \n'
        return self

    def add_size(self):
        if self.size:
            self.add_line(f'size = "{self.size},{self.size}"')
        return self

    def add_rand_dir(self):
        if self.rank_dir:
            self.add_line(f'rankdir={self.rank_dir};')
        return self

    def add_rank_sep(self):
        if self.rank_sep:
            self.add_line(f'ranksep={self.rank_sep};')
        return self

    def add_comment(self, value):
        return self.add_line(f'#{value} \n')

    def add_node_params(self):
        if self.node_params:
            self.add_line(f'node [{self.join_params(self.node_params)}]')
        return self

    def add_ranks(self):
        for rank, node_ids in self.ranks.items():
            node_list = ', '.join(['"%s"' % node_id for node_id in node_ids])
            self.add_line(f'{{ rank={rank}; {node_list} }}')
        return self