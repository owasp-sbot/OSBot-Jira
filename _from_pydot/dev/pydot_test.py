from os.path import abspath, join

import pydot

from pbx_gs_python_utils.utils.Files import Files


def run(event, context):
    d = 'digraph {\na -> b[label="hi", decorate];\n}'
    graph = pydot.graph_from_dot_data(d).pop()
    node = pydot.Node('AAAAAA', shape="box")
    graph.add_node(node)
    #tmp_file = '/tmp/dot_temp.dot'
    #graph.write(tmp_file)

    #return Files.contents(tmp_file)

    # this will excute the actual dot app
    data = Files.contents('./data/TM_Graph.dot')

    graph = pydot.graph_from_dot_data(data).pop()
    node = pydot.Node('aaa', shape="box")
    graph.add_node(node)
    graph.add_edge(pydot.Edge('aaa', 'Webserver',label='from aaaa'))

    filename = '/tmp/test_dot.svg'

    dot_static = abspath(join('./','dot_static'))


    graph.write_svg(filename, prog=dot_static)
    return Files.contents(filename)