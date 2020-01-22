from osbot_aws.apis.Lambda import Lambda

def get_graph_data(graph_name):
    params = {'params': ['raw_data', graph_name, 'details'], 'data': {}}
    data = Lambda('lambdas.gsbot.gsbot_graph').invoke(params)
    if type(data) is str:
        s3_key = data
        s3_bucket = 'gs-lambda-tests'
        tmp_file = S3().file_download_and_delete(s3_bucket, s3_key)
        data = Json.load_json_and_delete(tmp_file)
        return data
    return data

def calculate_paths(graph_data, destination_node):
    all_paths = {}
    if graph_data and destination_node:
        load_dependency('networkx')
        import networkx as nx
        G = nx.DiGraph()

        nodes = graph_data.get('nodes')
        edges = graph_data.get('edges')

        for edge in edges:
            from_id = edge[0]
            to_id   = edge[2]
            G.add_edge(to_id, from_id)          # reverse order
        #return G.nodes

        for node_id in list(nodes):
            paths = list(nx.all_simple_paths(G, node_id, destination_node))
            if len(paths) > 0:
                all_paths[node_id] =  paths
    return all_paths

def run(event, context):
    try:
        graph_name       = event.get('graph_name')
        destination_node = event.get('destination_node')
        graph_data = get_graph_data(graph_name)
        return calculate_paths(graph_data,destination_node)
    except:
        return {}