from osbot_aws.apis.Lambda import Lambda
from osbot_utils.utils.Files import file_create


class Graph_Dot:

    def __init__(self,graph):
        self.graph         = graph
        self.layout_engine = 'fdp'
        self.dot_code      = ""
        self.label         = ""
        self.node_params   = {}
        self.rank_dir      = None
        self.ranks         = {}

    def add_label(self):
        if self.label:
            self.add_line(f'label="{self.label}";')    \
                .add_line('labelloc = "t"')            # default to put label at the top
        return self

    def add_line(self, value):                      # todo: refactor all add_*** methods into separate 'build' class
        self.dot_code += f'\t\t\t{value} \n'
        return self

    def add_rand_dir(self):
        if self.rank_dir:
            self.add_line(f'rankdir={self.rank_dir};')
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
        self.dot_code = "digraph G { \n"
        (
            self.add_rand_dir()
                .add_label()
                .add_node_params()
                .add_line('mynode [image="/tmp/ACCESS.png" label="" shape="box"];')
                .add_comment ('###### Nodes #######')
         )

        for node in self.graph.nodes():
            shape  = node.get('shape')
            color  = node.get('color')
            params = ""
            if shape: params += f'shape="{shape}" '
            if color: params += f'color="{color}" '
            key = node.get('key')
            if params:
                self.add_line(f'"{key}" ["label"="{key}" {params}]')
            else:
            #self.dot_code += f'\t\t\t"{key}"\n'
                self.add_line(f'"{key}" ["label"="{key}"]')

        self.dot_code += '\t\t\t####### Edges #######\n'
        for edge in self.graph.edges():
            from_key = edge.get('from')
            to_key   = edge.get('to')
            self.dot_code += f'\t\t\t"{from_key}" -> "{to_key}"\n'

        self.add_ranks()

        self.dot_code +='\t\t   }'
        return self.dot_code

    def set_layout_engine(self, engine):
        self.layout_engine = engine
        return self

    def set_layout_engine_circo(self): return self.set_layout_engine('circo')
    def set_layout_engine_dot  (self): return self.set_layout_engine('dot'  )
    def set_layout_engine_fdp  (self): return self.set_layout_engine('fdp'  )  # current default one
    def set_layout_engine_osage(self): return self.set_layout_engine('osage')
    def set_layout_engine_neato(self): return self.set_layout_engine('neato')

    def set_label      (self,      value ): self.label            = value       ; return self
    def set_node_params(self,      params): self.node_params      = params      ; return self
    def set_node_param (self, key, value ): self.node_params[key] = value       ; return self
    def set_node_shape (self,      value ): self.set_node_param('shape', value) ; return self
    def set_rank_dir   (self,      value ): self.rank_dir         = value       ; return self

    def set_rank       (self, rank, node_ids): self.ranks[rank] = node_ids; return self
    def set_rank_same  (self,       node_ids): return self.set_rank('same' , node_ids)
    def set_rank_min   (self,       node_ids): return self.set_rank('min'  , node_ids)
    def set_rank_max   (self,       node_ids): return self.set_rank('max'  , node_ids)
    def set_rank_sink  (self,       node_ids): return self.set_rank('sink' , node_ids)
    def set_rank_source(self,       node_ids): return self.set_rank('source', node_ids)

    def render_svg(self):
        params = { 'dot':self.render(), 'layout_engine' : self.layout_engine}
        return Lambda('gw_bot.lambdas.dot_to_png').invoke(params)

    def render_svg_to_file(self, target_file):
        result = self.render_svg()
        svg = result.get('svg')
        if svg:
            file_create(target_file, svg)
            return {'status:':'ok', 'svg_file': target_file }
        print(result.get('error'))
        return {'status:':'error', 'error': result.get('error') }

