from osbot_aws.apis.Lambda import Lambda
from osbot_jira.osbot_graph.Graph import Graph
from osbot_jira.osbot_graph.engines.Graph_Dot_Render import Graph_Dot_Render
from osbot_utils.utils.Files import file_create


class Graph_Dot:

    def __init__(self, graph=None, graph_name='G'):
        self.graph           = graph or Graph()
        self.graph_name      = graph_name
        self.layout_engine   = 'fdp'
        self.sub_graphs      = []
        self.render = Graph_Dot_Render(self.graph, self.sub_graphs)


    def print_dot_code(self):
        print(self.render.dot_code)
        return self

    def set_layout_engine (self,      engine   ): self.layout_engine = engine                ; return self
    def set_node_shape    (self,      value    ): self.set_node_param('shape', value) ; return self

    def set_concentrate   (self,               ): self.render.concentrate      = True        ; return self
    def set_extra_dot_code(self,      value    ): self.render.extra_dot_code   = value       ; return self
    def set_label         (self,      value    ): self.render.label            = value       ; return self
    def set_node_params   (self,      params   ): self.render.node_params      = params      ; return self
    def set_node_param    (self, key, value    ): self.render.node_params[key] = value       ; return self
    def set_size          (self,      value    ): self.render.size             = value       ; return self
    def set_rank_dir      (self,      value    ): self.render.rank_dir         = value       ; return self
    def set_rank_sep      (self,      value    ): self.render.rank_sep         = value       ; return self
    def set_rank          (self, rank, node_ids): self.render.ranks[rank] = node_ids         ; return self


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
        params = { 'dot':self.render.render(), 'layout_engine' : self.layout_engine}
        return Lambda('gw_bot.lambdas.dot_to_svg').invoke(params)

    def render_svg_to_file(self, target_file):
        result = self.render_svg()
        svg = result.get('svg')
        print(result.get('error'))
        if svg:
            file_create(target_file, svg)
            return {'status:':'ok', 'svg_file': target_file }

        return {'status:':'error', 'error': result.get('error') }

