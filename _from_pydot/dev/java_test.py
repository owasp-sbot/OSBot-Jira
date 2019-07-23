import base64
import os
import subprocess
import tempfile

from pbx_gs_python_utils.utils.Files import Files


def run(event, context):
    code = event.get('code')
    (fd, puml_file) = tempfile.mkstemp('.puml')
    png_file = puml_file.replace(".puml",".png")
    #(fd, png_file) = tempfile.mkstemp('png')
    Files.write(puml_file, code)
    os.environ['GRAPHVIZ_DOT'] = './dot_static'

    result_1 = subprocess.run(['java', '-jar', './plantuml.jar', '-tpng', '-o', '/tmp', puml_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result_2 = subprocess.run(['ls', '-l', '/tmp'], stdout=subprocess.PIPE)
    if os.path.exists(png_file):
        with open(png_file, "rb") as image_file:
            png =  base64.b64encode(image_file.read()).decode()
    else:
            png = None

    result  = {
                "puml_file"        : puml_file                ,
                "png_file"         : png_file                 ,
                 "result_1_stdout" : result_1.stdout.decode() ,
                 "result_1_stderr" : result_1.stderr.decode() ,
                 "result_2_stdout" : result_2.stdout.decode() ,
                 "png"             : png
             }
    return result

    # result_1 = subprocess.run(['java', '-jar', './plantuml.jar', '-testdot'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
    # result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # result = subprocess.run(['java', '-jar','./plantuml.jar','-help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #return result_1.stdout.decode() + "\n1)\n" + result_1.stderr.decode() +"\n2)\n" + result_2.stdout.decode()


