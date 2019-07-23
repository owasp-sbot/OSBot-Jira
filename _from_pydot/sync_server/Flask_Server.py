import pprint
import sys

sys.path.append('.')
sys.path.append('../libs/pbx-gs-python-utils')

from pbx_gs_python_utils.utils.Lambdas_Helpers  import log_to_elk, slack_message
from flask                                      import Flask,request
from sync_server.rest_apis                      import api

app = Flask(__name__)


@app.before_request
def before_request():
    log_entry = {
                    'args'           : pprint.pformat(request.args),
                    'x_forwarded_for': request.headers.get('X-Forwarded-For'),
                    'form'           : pprint.pformat(request.form),
                    'method'         : request.method,
                    'path'           : request.path,
                    'url'            : request.url
    }

    log_to_elk("Flask log entry", data = log_entry, index='elastic_logs', category='server')

@app.route("/")
def home_page():
    return "the home page"

api.init_app(app)


if __name__ == '__main__':
    print("\nFlask Server starting")        # BUG this is being called twice
    log_to_elk("Flask Server starting", index='elastic_logs', category='start-up')
    slack_message(':robot_face: Sync Server started :point_left:', [], "...", '...')

    app.run(debug=True)
