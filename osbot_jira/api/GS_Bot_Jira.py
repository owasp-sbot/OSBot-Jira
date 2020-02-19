import json
import pprint

from gw_bot.helpers.Lambda_Helpers import slack_message, log_to_elk
from pbx_gs_python_utils.utils.Misc                         import Misc
from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment

from osbot_aws.apis.Lambda import Lambda
from osbot_jira.api.API_Issues                              import API_Issues
from osbot_jira.api.elk.Elk_To_Slack                        import ELK_to_Slack
from osbot_jira.api.graph.Graph_View                        import Graph_View
from osbot_jira.api.graph.Lambda_Graph                      import Lambda_Graph
from osbot_jira.api.slack.views.Jira_Slack_Actions          import Jira_Slack_Actions
from osbot_jira.api.slack.views.Jira_View_Issue             import Jira_View_Issue


class GS_Bot_Jira:

    def __init__(self):
        self.version = "v0.43 (GSBot)"

    def cmd_add_link(self, params, team_id=None, channel=None):
            if len(params) < 4:
                text = ":exclamation: Hi, to add a link, You must provide 3 params: `{from ID}` `{to ID}` `{link type}`"
                return {"text": text, "attachments": []}
            else:
                params.pop(0)           # position 0 is the 'issue' command
                from_key  = params.pop(0)
                to_key    = params.pop(0)
                link_type = " ".join(params)

                try:
                    from osbot_jira.api.jira_server.API_Jira import API_Jira
                    API_Jira().issue_add_link(from_key, link_type, to_key)
                    text = ':point_right: Added link: *{0}* `{1}` *{2}*'.format(from_key,link_type,to_key)
                except Exception as error:
                    text = ':red_circle: Error in `add_link`:  {0}'.format(error)
                return {"text": text, "attachments": []}

    def cmd_actions(self, params, team_id=None, channel=None):
        text, attachments = Jira_Slack_Actions().get_actions_ui()
        return {"text": text, "attachments": attachments}

    def cmd_create(self, params, team_id=None, channel=None):
        try:
            if len(params) < 3:
                text = ":exclamation: To create an issue you need to provide the `issue type` and `summary`. For example `jira create task abc"
                return {"text": text, "attachments": []}
            else:
                params.pop(0)           # the create command
                issue_type = params.pop(0)          #.title() # todo: find a better solution for this
                project    = issue_type.upper()               # todo: and to address the mapping of issue types to projects
                summary    = ' '.join(params)
                slack_message(':point_right: Going to create an `{0}` issue, in project `{1}` with summary `{2}`'.format(issue_type, project,summary), [], channel,team_id)

                #to do, move this feature to a separate lambda (which can be called to create issues
                from osbot_aws.Dependencies import load_dependency
                load_dependency('jira')
                from osbot_jira.api.jira_server.API_Jira import API_Jira

                # create issue
                result = API_Jira().issue_create(project,summary,'',issue_type)
                issue_id = "{0}".format(result)

                # show issue screenshot
                # payload = {'issue_id': issue_id,'channel': channel,'team_id': team_id, }
                # Lambda('osbot_browser.lambdas.jira_web').invoke_async(payload)

                # show issue UI
                payload = {'params': ['issue', issue_id], "channel": channel}
                Lambda('osbot_jira.lambdas.elastic_jira').invoke_async(payload)


                # show link of new issue to user
                jira_link = "https://glasswall.atlassian.net/browse/{0}".format(issue_id)
                text = ':point_right: New issue created with id <{0}|{1}>'.format(jira_link, issue_id)
            return {"text": text, "attachments": []}
        except Exception as error:
            log_to_elk('jira create error',f'{error}')
            return {'text': f':red_circle: Issue could not be created, please make sure that: \n - issue type exists\n - issue type = project type\n - Issue type CamelCase is correctly entered (you want `Task` and not `task`)', "attachments": []}

    def cmd_created_in_last(self, params, team_id=None, channel=None):
        elk_to_slack = ELK_to_Slack()
        if len(params) < 2:
            text = ":exclamation: you must provide an start date. You can use `1d`,`1w`,`1y` (d=day, w=week, y=year"
            return {"text": text, "attachments": []}

        from_date = params.pop()
        issues   = API_Issues().issues_created_in_last(from_date)


        issues_text = elk_to_slack.get_text_with_issues_key_and_summary(issues)
        graph_name  = elk_to_slack.save_issues_as_new_graph(issues)
        text        = elk_to_slack.get_slack_message(issues, graph_name)

        max_table = 100
        if len(issues) < max_table:
            text += "\n (Since there are less than {0} results also showing table with data)".format(max_table)
            self.cmd_table(["table", graph_name], team_id, channel)
        return {"text": text, "attachments": [{ 'text': issues_text , 'color':'good'}]}

    def cmd_created_between(self, params, team_id=None, channel=None):
        elk_to_slack = ELK_to_Slack()
        if len(params) < 3:
            text = ":exclamation: you must provide an start and end date. You can use `1d`,`1w`,`1y` (d=day, w=week, y=year"
            text += "\nTry `now-1d` and `now`"
            return {"text": text, "attachments": []}
        to_date = params.pop()
        from_date = params.pop()
        try:
            issues   = API_Issues().elastic().get_data_between_dates("Created",from_date, to_date)


            issues_text = elk_to_slack.get_text_with_issues_key_and_summary(issues)
            graph_name = elk_to_slack.save_issues_as_new_graph(issues)
            text        = elk_to_slack.get_slack_message(issues, graph_name)

            min_table = 100
            max_table = 100
            if min_table < len(issues) < max_table:
                text += "\n (Since there are less than {0} (and more than {1}) results also showing table with data)".format(max_table,min_table)
                self.cmd_table(["table", graph_name], team_id, channel)
            return {"text": text, "attachments": [{ 'text': issues_text , 'color':'good'}]}
        except Exception as error:
            text ="Error incmd_created_between: {0}".format(error)
            return {"text": text, "attachments": []}

    def cmd_updated_in_last(self, params, team_id=None, channel=None):  # refactor with cmd_created_in_last since 99% of the code is the same

        elk_to_slack = ELK_to_Slack()
        if len(params) < 2:
            text = ":exclamation: you must provide an start date. You can use `1d`,`1w`,`1y` (d=day, w=week, y=year"
            return {"text": text, "attachments": []}

        from_date = params.pop()
        issues   = API_Issues().issues_updated_in_last(from_date)


        issues_text = elk_to_slack.get_text_with_issues_key_and_summary(issues)
        graph_name = elk_to_slack.save_issues_as_new_graph(issues)
        text        = elk_to_slack.get_slack_message(issues, graph_name)

        max_table = 100
        if len(issues) < max_table:
            text += "\n (Since there are less than {0} results also showing table with data)".format(max_table)
            self.cmd_table(["table", graph_name], team_id, channel)
        return {"text": text, "attachments": [{ 'text': issues_text , 'color':'good'}]}

    def cmd_issue(self, params, team_id=None, channel=None):
        if len(params) < 2:
            text = ":exclamation: You must provide an issue id"
            return {"text": text, "attachments": []}
        else:
            issue_id = params.pop(1)            # position 0 is the 'issue' command
            #return {"text": issue_id, "attachments": []}
            Jira_View_Issue(issue_id,channel, team_id).create_and_send()

            #text, attachments = Jira_View_Issue(issue_id).get_actions_ui()
            #return {"text": text, "attachments": attachments}



    def cmd_screenshot(self, params, team_id=None, channel=None):
        attachments = []
        if len(params) < 2:
            text = ":exclamation: you must provide an issue id "
        else:
            params.pop(0) # remove 'issue' command

            issue_id = params.pop(0).upper()
            width    = Misc.to_int(Misc.array_pop(params, 0))
            height   = Misc.to_int(Misc.array_pop(params, 0))
            delay    = Misc.to_int(Misc.array_pop(params, 0))

            text = ':point_right: Getting screenshot for issue `{0}`'.format(issue_id)
            if width:
                text += ' with width `{0}`'.format(width)
            if height:
                text += ' and height `{0}`'.format(height)
            if delay:
                text += ' and delay `{0}`'.format(delay)

            payload = {
                            'issue_id': issue_id,
                            'channel' : channel ,
                            'team_id' : team_id ,
                            'width'   : width   ,
                            'height'  : height  ,
                            'delay'   : delay
                      }
            Lambda('osbot_browser.lambdas.jira_web').invoke_async(payload)

        return {"text": text, "attachments": attachments}

    def cmd_links(self, params, team_id=None, channel=None, user=None, only_create=False,save_graph=True):
        attachments = []
        if len(params) == 5: view = params.pop()
        else               : view = None

        if len(params) != 4:
            text = ':red_circle: for the `jira links` command, you need to provide 3 parameters: ' \
                   '\n\t\t - `jira key` ' \
                   '\n\t\t - `direction` (up, down or any) and ' \
                   '\n\t\t - `depth` '
            #text += '\n\n {0}'.format(params)
        else:
            depth = params.pop()
            if Misc.is_number(depth):
                depth     = int(depth)
                direction = params.pop()
                target    = params.pop()

                if direction not in ['up', 'down','children','parents', 'all']:
                    text = ':red_circle: Unsupported direction `{0}` for `jira links` command. Current supported values are: `all`, `up`, `down`, `children` and `parents`'.format(
                        direction)
                    return {"text": text, "attachments": attachments}

                graph = Lambda_Graph().graph_links(target, direction, depth)

                graph_type = "{0}__{1}___depth_{2}".format(target, direction, depth)

                if save_graph is False:
                    return graph
                graph_name = graph.render_and_save_to_elk(None, graph_type, channel, user)
                if only_create:
                    return graph, graph_name, depth, direction, target

                puml = graph.puml.puml
                max_size = 60000
                if channel and (not view) and len(puml) > max_size:            # only do this check when there is a channel and no view (meaning that the graph will be generated)
                    text = ':red_circle: for the graph `{0}` with `{1}` nodes and `{2}` edges, the PlantUML code generated from your query was too big `{3}` and rendering this type of large graphs doesn\'t work well in PlantUML (max allowed is `{4}`)'\
                                    .format(graph_name, len(graph.nodes), len(graph.edges), len(puml),max_size)
                else:
                    if view:                                        # if we have defined a view, render it here
                        graph_view          = Graph_View()
                        graph_view.graph    = graph
                        graph_view.graph.reset_puml()
                        graph_view.render_view(view,channel,team_id,graph_name)
                        puml = graph_view.graph.puml.puml
                    else:
                        view = 'default'

                    if channel:  # if the channel value is provided return a user friendly message, if not, return the data
                        text = ':point_right: Created graph with name `{4}`, based on _{0}_ in the direction `{1}`, with depth `{2}`, with plantuml size: `{3}`, with view `{5}`, with `{6}` nodes and `{7}` edges'\
                                        .format(target, direction, depth, len(puml), graph_name, view, len(graph.nodes), len(graph.edges))
                        Lambda('gw_bot.lambdas.puml_to_slack').invoke_async({"puml": puml,"channel": channel, 'team_id' : team_id})
                    else:
                        data = {
                            "target"    : target     ,
                            "direction" : direction  ,
                            "depth"     : depth      ,
                            "nodes"     : graph.nodes,
                            "edges"     : graph.edges,
                            "puml"      : puml       ,
                            "graph_name": graph_name ,
                            "view"      : view
                        }
                        text = json.dumps(data, indent=4)
            else:
                text = ':red_circle: error: invalid value provided for depth `{0}`. It must be an number'.format(depth)


        return {"text": text, "attachments": attachments}

    def cmd_help(self):
        commands = [func for func in dir(GS_Bot_Jira) if
                    callable(getattr(GS_Bot_Jira, func)) and func.startswith("cmd")]

        help_text = ""
        for command in commands:
            help_text += " • {0}\n".format(command.replace('cmd_',''))
        attachments = API_Slack_Attachment(help_text, 'good').render()
        text = "*Here are the `jira` commands available:*"
        return {"text": text, "attachments": attachments}

    def cmd_search(self, event):
        Lambda('osbot_jira.lambdas.elk_to_slack').invoke_async(event)
        return None

    def cmd_table(self, params, team_id=None, channel=None):
        attachments = []
        if len(params) < 2:
            text = ":exclamation: you must provide a graph_name to show in a table format"
        else:
            params.pop(0)                           # remove 1st command since it is 'server'
            graph_name = params.pop()
            text = ':point_right: Showing table with data created from graph `{0}`'.format(graph_name)
            Lambda('lambdas.browser.lambda_browser').invoke_async({"params": [ "table", graph_name , 'graph_simple'], "data":{"channel" : channel, "team_id": team_id}})
        return {"text": text, "attachments": attachments}

    # def cmd_server(self, params, team_id=None, channel=None):
    #     attachments = []
    #     if len(params) < 2:
    #         text = ":exclamation: you must provide an server command"
    #     else:
    #         params.pop(0)                           # remove 1st command since it is 'server'
    #         command  = params.pop(0)
    #         data     = Secrets('sync-server-ngrok').value_from_json_string()
    #         username = data.get('username')
    #         password = data.get('password')
    #         if command[0] !='/':
    #             url = "https://gs-jira.ngrok.io/server/{0}".format(command)
    #         else:
    #             url = "https://gs-jira.ngrok.io{0}".format(command)
    #         result   = requests.get(url, auth=(username, password)).text
    #         text     = "{0}".format(result)
    #         #attachments = [{'text':url}]
    #
    #     return {"text": text, "attachments": attachments}

    # def cmd_down(self, params, team_id=None, channel=None, user=None):
    #     self.up_down("down", params, team_id, channel, user)
    #
    # def cmd_up(self, params, team_id=None, channel=None, user=None):
    #     self.up_down("up", params, team_id, channel, user)

    # def cmd_load_sheet(self, params, team_id=None, channel=None):
    #     def send_slack_message(message):
    #         slack_message(message, [], channel, team_id)
    #
    #     # def show_pdf(file_id,icon, when):
    #     #     send_slack_message('{0} this is what the file currently looks `{1}` the sync'.format(icon, when))
    #     #     Lambda('gsbot_gsuite.lambdas.gdocs').invoke({"params":['pdf', file_id], 'data':{'team_id':team_id,'channel': channel}})
    #
    #
    #     if len(params) < 2:
    #         text = ":exclamation: you must provide an gsuite `file_id` (you can find this on the url of the document you want to sync)"
    #         send_slack_message(text)
    #     else:
    #         params.pop(0)  # remove 1st command since it is 'server'
    #         file_id = params.pop(0)
    #
    #         #send_slack_message(':point_right: Staring syncing workflow for file `{0}`'.format(file_id))
    #         #show_pdf          (file_id, ':one:', 'BEFORE')
    #         #send_slack_message(':two: syncing data ...')
    #
    #         result = self.cmd_server(['server','/jira-sync/load-jira/{0}'.format(file_id)])
    #         #[trigger_sync_jira_sheets]
    #         status = json.loads(result.get('text')).get('status')
    #         send_slack_message('Execution result: `{0}`'.format(status))
    #
    #         #show_pdf(file_id, ':three:','AFTER')
    #
    #     return None,None


    # def cmd_diff_sheet(self, params, team_id=None, channel=None):
    #     def send_slack_message(message):
    #         slack_message(message, [], channel, team_id)
    #
    #     if len(params) < 2:
    #         text = ":exclamation: you must provide an gsuite `file_id` (you can find this on the url of the document you want to sync)"
    #         send_slack_message(text)
    #     else:
    #         params.pop(0)  # remove 1st command since it is 'server'
    #         file_id = params.pop(0)
    #         send_slack_message(':one: diffing data ...')
    #         result = self.cmd_server(['server','/jira-sync/diff-sheet/{0}'.format(file_id)])
    #         send_slack_message(result)
    #
    #     return None,None

    # def cmd_sync_sheet(self, params, team_id=None, channel=None):
    #     def send_slack_message(message):
    #         slack_message(message, [], channel, team_id)
    #
    #     if len(params) < 2:
    #         text = ":exclamation: you must provide an gsuite `file_id` (you can find this on the url of the document you want to sync)"
    #         send_slack_message(text)
    #     else:
    #         params.pop(0)  # remove 1st command since it is 'server'
    #         file_id = params.pop(0)
    #         #send_slack_message(':one: diffing data ...')
    #         result = self.cmd_server(['server','/jira-sync/sync-sheet/{0}'.format(file_id)])
    #         status = Misc.get_value(Misc.json_load(result.get('text')),'status',result)
    #         send_slack_message('Execution result: `{0}`'.format(status))
    #
    #     return None,None


    def cmd_version(self, params, team_id=None, channel=None):
        if channel:
            slack_message(self.version, [], channel, team_id)
        else:
            return {"text": self.version, "attachments":[] }


    # helpers

    # def up_down(self, direction, params, team_id=None, channel=None, user=None):
    #     if len(params) != 3:
    #         text = ':red_circle: for the `jira {0}` command, you need to provide 2 parameters: ' \
    #                '\n\t\t - `jira key or graph` '                                              \
    #                '\n\t\t - `depth` '.format(direction)
    #         slack_message(text, [], channel, team_id)
    #         return
    #
    #     target = params[1]
    #     depth  = int(params[2])
    #     params = ['links', target, direction, depth]
    #
    #
    #     (graph, graph_name, depth, direction, target) = self.cmd_links(params, team_id, channel, user, only_create=True)
    #     if graph:
    #         text = ':point_right: Created graph for `{0}` in the direction `{1}`, with depth `{2}`, with name `{3}`, with `{4}` nodes and `{5}` edges' \
    #                         .format(target, direction, depth, graph_name, len(graph.nodes), len(graph.edges))
    #         slack_message(text, [], channel, team_id)
    #         Lambda('lambdas.browser.lambda_browser').invoke_async({"data": {"team_id": team_id, "channel": channel}, "params": ['viva_graph', graph_name, 'default']})
    #

    # main method

    # todo: refactor to use dynamic method generation (this is the legacy way to resolve methods)
    def handle_request(self,event):
        #log_to_elk('in handle_request', event)
        params      = event.get('params')
        channel     = event.get('channel')
        team_id     = event.get('team_id')
        user        = event.get('user')
        attachments = []
        if params is None or len(params) < 1:
            text   = ":point_right: no command received, see `jira help` for a list of available commands"
        else:
            command = params[0]
            try:
                if command == 'add_link'           : return self.cmd_add_link       (params, team_id, channel)
                if command == 'help'               : return self.cmd_help           ()
                if command == 'actions'            : return self.cmd_actions        (params, team_id, channel)
                if command == 'create'             : return self.cmd_create         (params, team_id, channel)
                if command == 'created_in_last'    : return self.cmd_created_in_last(params, team_id, channel)
                if command == 'created_between'    : return self.cmd_created_between(params, team_id, channel)
                if command == 'updated_in_last'    : return self.cmd_updated_in_last(params, team_id, channel)
                if command == 'screenshot'         : return self.cmd_screenshot     (params, team_id, channel)
                if command == 'issue'              : return self.cmd_issue          (params, team_id, channel)
                if command == 'links'              : return self.cmd_links          (params, team_id, channel, user)
                #if command == 'up'                 : return self.cmd_up             (params, team_id, channel, user)
                #if command == 'down'               : return self.cmd_down           (params, team_id, channel, user)
                if command == 'search'             : return self.cmd_search         (event          )
                #if command == 'server'             : return self.cmd_server         (params, team_id, channel)
                #if command == 'load_sheet'         : return self.cmd_load_sheet     (params, team_id, channel)
                if command == 'table'              : return self.cmd_table          (params, team_id, channel)
                #if command == 'sync_sheet'         : return self.cmd_sync_sheet     (params, team_id, channel)
                #if command == 'diff_sheet'         : return self.cmd_diff_sheet     (params, team_id, channel)
                #if command == 'graph_sheet'        : return self.cmd_graph_sheet    (params, team_id, channel)
                if command == 'version'            : return self.cmd_version        (params, team_id, channel)

                if '-' in command and ' ' not in command and len(command) < 10:  # if it looks like a Issue ID, call the cmd_issue function
                    params.insert(0,'issue')
                    return self.cmd_issue(params, team_id, channel)

                #return self.cmd_issue(['issue'] + params, channel)        # default to this one
                text = ':red_circle: Not supported command `{0}` , see all available using `jira help`'.format(command)
            except Exception as error:
                text = ':red_circle: Error processing command `{0}`: _{1}_'.format(command, pprint.pformat(error))
        return { "text": text, "attachments": attachments}

    # def resolve_es_index(self, key):
    #     if "SEC-" in key:  return 'sec_project'
    #     return "jira"



    # def send_test_button(self, params,channel):
    #     callback_id = 'view-jira-issue'
    #
    #     message = {
    #         "text": "JIRA Helper (v0.1)",
    #         "attachments": [
    #             {
    #                 "text": "What Jira ID you want to see",
    #                 "fallback": "Not supported",
    #                 "callback_id": "{0}".format(callback_id),
    #                 "color": "#3AA3E3",
    #                 "attachment_type": "default",
    #                 "actions": [
    #                     {
    #                         "name": "key",
    #                         "text": "RISK-424",
    #                         "type": "button",
    #                         "value": "RISK-424"
    #                     },
    #                     {
    #                         "name": "key",
    #                         "text": "SEC-9195",
    #                         "type": "button",
    #                         "value": "SEC-9195"
    #                     },
    #                     {
    #                         "name": "key",
    #                         "text": "GSP-42",
    #                         "type": "button",
    #                         "value": "GSP-42"
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #     #from utils.API_Slack import API_Slack
    #     #API_Slack(channel).send_message(message['text'], message['attachments'])
    #     return { "text": message['text'], "attachments" : message['attachments']}