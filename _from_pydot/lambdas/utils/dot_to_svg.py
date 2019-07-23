import  base64
import  tempfile
from pbx_gs_python_utils.utils.Files import Files
from    utils.Lambdas_Helpers import slack_message, log_to_elk
from utils.Process import Process
from    utils.aws.Lambdas     import load_dependency


def run(event, context):
    load_dependency('pydot')
    channel = event.get('channel')
    data    = event.get('dot')

    #slack_message("in dot to svg: {0}".format(event), [], channel)
    log_to_elk("in dot to svg: {0}".format(event))

    import dot_parser

    try:
        (fd, tmp_file) = tempfile.mkstemp('dot)')
        dot_static     = '/tmp/lambdas-dependencies/pydot/dot_static'
        Process.run("chmod", ['+x', dot_static])
        data           = data.replace('&lt;', '<').replace('&gt;','>')  # this solved a really nasty bug caused by the fact that Slack will html encode the < and >

        # graph          = pydot.graph_from_dot_data(data).pop()
        # <from pydot>  use code below (instead of above) to get a better error message from dot parser
        graphparser = dot_parser.graph_definition()
        graphparser.parseWithTabs()
        tokens      = graphparser.parseString(data)
        graph       = list(tokens).pop()
        # </from pydot>
        graph.write_svg(tmp_file, prog=dot_static)
        svg_raw        = Files.contents(tmp_file)
        return base64.b64encode(svg_raw.encode()).decode()
    except Exception as error:
        slack_message("[dot_to_svg] Error: {0} ".format(error), [], channel)
        return None