from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment
from pbx_gs_python_utils.utils.Lambdas_Helpers            import slack_message, log_to_elk
from pbx_gs_python_utils.utils.Lists                      import Lists

from osbot_jira.api.API_Issues import API_Issues
from osbot_jira.api.graph.GS_Graph import GS_Graph
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph


class ELK_to_Slack:
    def __init__(self):
        self.api_issues  = API_Issues()
        self.attachments = API_Slack_Attachment()
        self.default_max =  20

    def set_default_max(self, value): self.default_max = value ; return self

    def get_search_mappings(self):
        return {
            'assign'   : 'Assignee:',
            'summary'  : 'Summary:',
            'asset'    : 'Issue\ Type:"IT Asset" AND Summary:',
            'entity'   : 'Issue\ Type:"Business Entity"  AND Summary:',
            'epic'     : 'Issue\ Type:"Epic"  AND Summary:',
            'incident' : 'Issue\ Type:"Incident" AND Summary:',
            'meeting'  : 'Issue\ Type:Meeting AND Summary:',
            'people'   : 'Issue\ Type:People AND Summary:',
            'project'  : 'Issue\ Type:"GS-Project" AND Summary:',
            'programme': 'Issue\ Type:"Programme" AND Summary:',
            'risk'     : 'Issue\ Type:Risk AND Summary:',
            'sc'       : 'Issue\ Type:"Security Controls AND Summary:',
            'service'  : 'Issue\ Type:"GS Service" AND Summary:',
            'task'     : 'Issue\ Type:"Task"  AND Summary:',

            'vuln'     : 'Issue\ Type:Vulnerability AND Summary:',

            'supplier': 'Project:"Supplier\ Log" AND Summary:',

            'label'   : 'Labels:',
            'high'    : 'Rating:High      AND Summary:',
            'low'     : 'Rating:Low      AND Summary:',
            'medium'  : 'Rating:Medium      AND Summary:',


        }

    def get_search_query(self,params):
        search_type  = Lists.first(params,strip=True)
        if search_type:
            query = self.get_search_mappings().get(search_type)
            if query:
                return query + ' '.join(params[1:])
            #if index_name.lower() in ['people']: return 'Issue\ Type:People AND Summary ' +' '.join[1:]

        return ' '.join(params)

    def get_text_with_issues_key_and_summary(self, results):
        issues_list = ""
        keys        = []
        for issue in results[0:self.default_max]:
            key         = issue['Key']
            summary     = issue['Summary']
            jira_link   = "https://jira.photobox.com/browse/{0}".format(key)
            issues_list += "<{0}|{1}>  {2} \n".format(jira_link, key, summary)
            keys.append(key)
        return issues_list

    def save_issues_as_new_graph(self, issues):
        all_keys = []
        for issue in issues:
            all_keys.append(issue['Key'])
        graph = GS_Graph()  # save results in graph
        graph.add_nodes(all_keys)
        return Lambda_Graph().save_gs_graph(graph, graph_type='graph-search')

    def get_slack_message(self, issues, graph_name):
        text = ":point_right: Elk search had `{0}` matches (results saved to graph `{1}` ) \n" \
            .format(len(issues), graph_name)
        if len(issues) > self.default_max:
            text += ":point_right: showing first `{0}`".format(self.default_max)
        return text

    def cmd_search(self, params, user=None, team_id=None, channel=None):
        if Lists.empty(params):
            text = ':red_circle: for the `search` command, please provide the type of search you want to do. \nHere are the the options:'
            for name in sorted(list(set(self.get_search_mappings()))):
                text +=  '\n\t\t • `{0}` '.format(name)
            text += '\n\n:point_right: the syntax is: `jira search {type} {what to search}` (note search is done on the Summary field)'
            slack_message(text, [], channel, team_id)
            return

        query       = self.get_search_query(params)
        issues      = self.api_issues.search_using_lucene(query)
        if team_id and channel:
            if len(issues) > 0:
                issues_text = self.get_text_with_issues_key_and_summary(issues)
                graph_name  = self.save_issues_as_new_graph(issues)
                text        = self.get_slack_message(issues, graph_name)

                self.attachments.set_text(issues_text)
                self.attachments.set_callback_id("search-results")

                slack_message(text, self.attachments.render(), channel, team_id)
            else:
                text = ":red_circle: Elk search for `{0}` had `{1}` matches".format(query, len(issues))
                slack_message(text, self.attachments.render(), channel, team_id)

        else:
            return issues
    # def cmd_search_graph(self, params, user, team_id, channel):
    #     results = self.api_issues.search_using_lucene(' '.join(params))
    #     keys = [issue.get('Key') for issue in results]
    #     if len(keys) == 0:
    #         text = ':black_circle: ELK search returned 0 results'
    #     else:
    #         text =  'ELK search resulted in `{0}` keys'.format(len(keys))
    #
    #         slack_cmd = 'links {0} all 1'.format(','.join(keys))
    #         params    = slack_cmd.split(' ')
    #         result    = Lambda('gs.elastic_jira').invoke({"params": params,  "user": user, "channel": channel})
    #         #slack_message(result.get('text'), result.get('attachments'), channel)
    #         self.attachments.set_text(result.get('text'))
    #
    #     slack_message(text, self.attachments.render(), channel, team_id)

    def handle_lambda_event(self, event):

        channel = event.get('channel' )
        params  = event.get("params"  )
        user    = event.get('user'    )
        team_id  = event.get('team_id')
        log_to_elk('[Elk_to_Slack.handle_lambda_event]: {0}'.format(event))
        try:
            if params:
                command = params.pop(0)
                if command == 'search'      : return self.cmd_search      (params, user, team_id, channel)
                #if command == 'search-graph': return self.cmd_search_graph(params, user, team_id, channel)

                #return slack_message(":point_right: in handle_lambda_event with params: {0}".format(event), [], channel)
            slack_message(":red_circle: in ELK_to_Slack, un-supported command :`{0}`. Data received was: {1}".format(command,event), [], channel)
        except Exception as error:
            message = ":red_circle: error in ELK_to_Slack:`{0}`. Data received was: {1}".format(error,event)
            log_to_elk(message, level = 'error')
            slack_message(message , [], channel)

    # def save_search_in_elk(self, message):
    #     index   = 'slack_interaction'
    #     item    = { 'data': message,
    #                 'date': datetime.datetime.utcnow() }
    #     elastic = Log_To_Elk().setup(index)
    #     return elastic.add(item)