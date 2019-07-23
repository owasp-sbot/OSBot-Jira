from flask_restplus import Api

from .jira_issues  import api as jira_issues
from .sync_server  import api as sync_server
from .jira_sync    import api as jira_sync
from .gsbot_jira   import api as gsbot_jira

api = Api(
    title='Jira API',
    version='0.2',
    description='This API provides access to JIRA',
    doc='/api-docs/'
)

api.add_namespace(jira_issues)
api.add_namespace(sync_server)
api.add_namespace(jira_sync)
api.add_namespace(gsbot_jira)
