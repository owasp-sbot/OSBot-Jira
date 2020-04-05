from osbot_aws.apis.Lambda import Lambda
from osbot_jira.osbot_graph.Graph import Graph
from osbot_utils.utils.Files import file_create

LEFT_PADDING  = '             '      # using spaces instead of tabs ('/t') creates more consistent results
DIGRAPH_START = 'digraph G { \n'
DIGRAPH_END   = '          }'

class Graph_Dot:

    def __init__(self,graph=None):
        self.graph           = graph or Graph()
        self.layout_engine   = 'fdp'
        self.dot_code        = ""
        self.extra_dot_code  = ""
        self.label           = ""
        self.node_params     = {}
        self.size            = None
        self.rank_dir        = None
        self.rank_sep        = None
        self.ranks           = {}

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

    def join_params(self,params):
        return ' '.join([f'{key}="{value}"' for key, value in params.items()])

    def print_dot_code(self):
        print(self.dot_code)
        return self

    def render(self):
        self.dot_code = DIGRAPH_START
        (
            self.add_rand_dir()
                .add_rank_sep()
                .add_size()
                .add_label()
                .add_node_params()
                .add_comment ('###### Nodes #######')
         )

        for node in self.graph.nodes():
            key    = node.get('key')
            label  = node.get('value') or key
            #shape  = node.get('shape')
            #color  = node.get('color')
            params = ""
            for param_name,param_value in node.items():
                if param_name == 'key'  : continue          # key should not be set here
                params += f'{param_name}="{param_value}" '

            #if shape: params += f'shape="{shape}" '
            #if color: params += f'color="{color}" '

            if params:
                self.add_line(f'"{key}" [{params}]')
            else:
                self.add_line(f'"{key}" ["label"="{label}"]')

        self.add_line().add_comment('###### Edges #######')

        for edge in self.graph.edges():
            from_key = self.edge_link(edge.get('from'))
            to_key   = self.edge_link(edge.get('to'))
            self.add_line(f' {from_key} -> {to_key}')

        self.add_ranks()
        self.add_extra_dot_code()
        self.dot_code += DIGRAPH_END
        return self.dot_code

    def edge_link(self, edge_node):     # add support for record shape linking in edges
        if ':' in edge_node:
            items = edge_node.split(':')            # todo: refactor how this is done
            return f'"{items[0]}":"{items[1]}"'
        else:
            return f'"{edge_node}"'

    def set_extra_dot_code(self,      value    ): self.extra_dot_code   = value       ; return self
    def set_label         (self,      value    ): self.label            = value       ; return self
    def set_layout_engine (self,      engine   ): self.layout_engine = engine         ; return self
    def set_node_params   (self,      params   ): self.node_params      = params      ; return self
    def set_node_param    (self, key, value    ): self.node_params[key] = value       ; return self
    def set_node_shape    (self,      value    ): self.set_node_param('shape', value) ; return self
    def set_size          (self,      value    ): self.size             = value       ; return self
    def set_rank_dir      (self,      value    ): self.rank_dir         = value       ; return self
    def set_rank_sep      (self,      value    ): self.rank_sep         = value       ; return self
    def set_rank          (self, rank, node_ids): self.ranks[rank] = node_ids         ; return self



    def set_rank_same           (self, node_ids): return self.set_rank('same' , node_ids)
    def set_rank_min            (self, node_ids): return self.set_rank('min'  , node_ids)
    def set_rank_max            (self, node_ids): return self.set_rank('max'  , node_ids)
    def set_rank_sink           (self, node_ids): return self.set_rank('sink' , node_ids)
    def set_rank_source         (self, node_ids): return self.set_rank('source', node_ids)

    def set_layout_engine_circo(self): return self.set_layout_engine('circo')
    def set_layout_engine_dot  (self): return self.set_layout_engine('dot'  )
    def set_layout_engine_fdp  (self): return self.set_layout_engine('fdp'  )  # current default one
    def set_layout_engine_osage(self): return self.set_layout_engine('osage')
    def set_layout_engine_neato(self): return self.set_layout_engine('neato')

    def set_node_shape_box     (self): return self.set_node_shape('box'   )
    def set_node_shape_circle  (self): return self.set_node_shape('circle')


    def render_svg(self):
        params = { 'dot':self.render(), 'layout_engine' : self.layout_engine}
        return Lambda('gw_bot.lambdas.dot_to_svg').invoke(params)

    def render_svg_to_file(self, target_file):
        result = self.render_svg()
        svg = result.get('svg')
        print(result.get('error'))
        if svg:
            file_create(target_file, svg)
            return {'status:':'ok', 'svg_file': target_file }

        return {'status:':'error', 'error': result.get('error') }

