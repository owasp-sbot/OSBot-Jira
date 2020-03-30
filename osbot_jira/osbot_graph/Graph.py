from osbot_utils.decorators.Lists import index_by, group_by


class Graph:

    def __init__(self):
        self._nodes = {}
        self._edges = {}
        self.options = self.default_options()

    def add_edge(self, from_key:str, label:str, to_key:str, params:dict=None):
        self.edge_add(from_key, label, to_key, params)
        return self

    def add_node(self, key:str, data:dict=None):
        self.node_add(key, data)
        return self

    def default_options(self):
        return {} #{ "Unique_Node_IDs": True}

    def edge_add(self, from_key:str, label:str, to_key:str, params:dict=None):
        edge_key = f"{from_key}__{label}__{to_key}"
        edge = {'from'  : from_key ,
                'label' : label    ,
                'to'    : to_key   }
        if params:
            edge['params'] = params
        self._edges[edge_key] = edge
        return edge

    @group_by
    def edges(self):
        return list(self._edges.values())

    def node_add(self, key:str, data:dict=None):
        node = {}
        if type(data) is dict:
            for key,value in data.items():
                node[key] = value
        else:
            if data:
                node['value'] = str(data)
            else:
                node['value'] = key
        node['key'] = key
        self._nodes[key] = node
        return node

    @index_by
    def nodes(self):
        return list(self._nodes.values())

