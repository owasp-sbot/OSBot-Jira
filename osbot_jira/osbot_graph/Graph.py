from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by


class Graph:

    def __init__(self):
        self._nodes = {}
        self._edges = []
        self.options = self.default_options()

    def add_edge(self, from_key:str, to_key:str, params:dict=None):
        self.edge_add(from_key, None, to_key, params)
        return self

    def add_edge_with_label(self, from_key:str, label:str, to_key:str, params:dict=None):
        self.edge_add(from_key, label, to_key, params)
        return self

    def add_edge_in_direction(self, from_key:str, to_key:str, direction:str, params:dict=None):
        if params is None:
            params = {}
        params['dir'] = direction
        return self.add_edge(from_key, to_key, params)

    def add_edge__back   (self, from_key:str, to_key:str, params:dict=None): return self.add_edge_in_direction(from_key, to_key, 'back'   , params)
    def add_edge__both   (self, from_key:str, to_key:str, params:dict=None): return self.add_edge_in_direction(from_key, to_key, 'both'   , params)
    def add_edge__forward(self, from_key:str, to_key:str, params:dict=None): return self.add_edge_in_direction(from_key, to_key, 'forward', params)
    def add_edge__none   (self, from_key:str, to_key:str, params:dict=None): return self.add_edge_in_direction(from_key, to_key, 'none'   , params)


    def add_edges(self, edges):
        for edge in edges:
            if len(edge) == 2:
                self.add_edge(edge[0],edge[1])
            if len(edge) == 3:
                self.add_edge_with_label(*edge)
        return self

    def add_node(self, key:str, params=None):
        self.node_add(key, params)
        return self

    def add_node_record(self, key, label):                  # to do add label parser
        self.node_add(key, {'shape':'record','label':label})
        return self

    def add_nodes(self, keys: list):
        for key in keys:
            self.add_node(key)
        return self

    def default_options(self):
        return {} #{ "Unique_Node_IDs": True}

    def edge_add(self, from_key:str, label:str, to_key:str, params:dict=None):
        #edge_key = f"{from_key}__{label}__{to_key}"
        edge = {'from'  : from_key ,
                'label' : label    ,
                'to'    : to_key   }

        if type(params) is dict:
            for item_key,item_value in params.items():
                edge[item_key] = item_value

        self._edges.append(edge)
        return edge

    @group_by
    def edges(self):
        return self._edges
        #return list(self._edges.values())

    def node_add(self, key:str, params=None):
        node = {'key': key , 'label':key }
        if type(params) is dict:
            for item_key,item_value in params.items():
                node[item_key] = item_value
        else:
            if params:
                node['label'] = str(params)
        self._nodes[key] = node
        return node

    @index_by
    def nodes(self):
        return list(self._nodes.values())

    def nodes_items(self):
        return self._nodes.items()

