from pbx_gs_python_utils.utils.Process import Process


def an_method(params):
    return Process.run('echo', [params])

def run(event, context):
    an_method('this is an method')
    return "ssh test..."