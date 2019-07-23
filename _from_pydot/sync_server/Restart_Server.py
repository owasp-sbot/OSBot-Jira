import subprocess
import sys

sys.path.append('.')
sys.path.append('../libs/pbx-gs-python-utils/src')
from flask import Flask

app = Flask(__name__)

@app.route('/')
def reboot_server():
    #run_params = ['sh','reload-docker.sh']
    run_params = ['sh', 'docker/update-docker-src-folder.sh']
    cwd = '../../gs-pydot-risk'
    subprocess.Popen(run_params, cwd=cwd)
    #return 'Rebooting server.... (using ./reload-docker.sh)'
    return 'Reloading docker source code.... (using ./docker/update-docker-src-folder.sh)'

if __name__ == '__main__':
    app.run(debug=True, port=21112)
