import base64
import os
import subprocess
import tempfile

from pbx_gs_python_utils.utils.Files import Files
from utils.Process import Process
from utils.aws.Lambdas import load_dependency


def run(event, context):
    load_dependency('plantuml')
    dot_static                 = '/tmp/lambdas-dependencies/plantuml/dot_static'
    plantuml_jar               = '/tmp/lambdas-dependencies/plantuml/plantuml.jar'

    Process.run("chmod", ['+x', dot_static  ])
    Process.run("chmod", ['+x', plantuml_jar])

    os.environ['PLANTUML_LIMIT_SIZE'] = str(4096 * 4)                       # set max with to 4 times the default (16,384)
    os.environ['GRAPHVIZ_DOT']        = dot_static
    (fd, puml_file)                   = tempfile.mkstemp('.puml')
    png_file                          = puml_file.replace(".puml",".png")
    code                              = event.get('puml')
    Files.write(puml_file, code)

    subprocess.run(['java', '-jar', plantuml_jar, '-Xmx2512m','-tpng', '-o', '/tmp', puml_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if os.path.exists(png_file):
        with open(png_file, "rb") as image_file:
            png =  base64.b64encode(image_file.read()).decode()
    else:
            png = None

    return {"png_base64"  : png }



