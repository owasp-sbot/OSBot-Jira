import json
import pprint
import requests
from   osbot_aws.apis.Secrets import Secrets

from pbx_gs_python_utils.utils.Lambdas_Helpers              import slack_message
from pbx_gs_python_utils.utils.Misc                         import Misc
from pbx_gs_python_utils.utils.slack.API_Slack_Attachment   import API_Slack_Attachment

from osbot_aws.apis.Lambda                                  import Lambda
from osbot_jira.api.API_Issues                              import API_Issues
from osbot_jira.api.elk.Elk_To_Slack                        import ELK_to_Slack
from osbot_jira.api.graph.GS_Graph                          import GS_Graph
from osbot_jira.api.graph.Lambda_Graph                      import Lambda_Graph


class GS_Bot_Jira:

    def __init__(self):
        self.version = "v0.30"

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
            issues   = API_Issues().elastic.get_data_between_dates("Created",from_date, to_date)


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

    def cmd_issue(self, params, team_id, channel):
        #log_to_elk('in cmd_issue', {'params' : params, 'channel': channel})
        attachments = []
        if len(params) == 1:
            text = ":exclamation: you must provide an issue id "
        else:
            key         = params[1].upper()
            jira_link   = "https://jira.photobox.com/browse/{0}".format(key)
            api_issues = API_Issues()
            es_index   = api_issues.resolve_es_index(key)
            if es_index:
                text        = "....._fetching data for *<{0}|{1}>* _from index:_ *{2}*".format(jira_link, key, es_index)

                table       = api_issues.create_issue_table(key)

                if channel:
                    payload = {"puml": table.puml ,
                               "channel": channel,
                               "team_id": team_id }
                    Lambda('utils.puml_to_slack').invoke_async(payload)
            else:
                text = ":exclamation: could not find index for issue "
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

                graph = Lambda_Graph().get_gs_graph___by_name(target)       # check if the value provided is a saved graph
                if graph is not None:                                       # if it exists
                    keys = graph.nodes                                      # set keys to graph nodes
                else:                                                       # if not
                    keys      = target.upper().split(",")                   #    use value as keys


                graph = GS_Graph()

                if   direction == 'up'      : graph.set_links_path_mode_to_up()
                elif direction == 'down'    : graph.set_links_path_mode_to_down()
                elif direction == 'children': graph.set_puml_link_types_to_add(['is parent of'])
                elif direction == 'parents' : graph.set_puml_link_types_to_add(['is child of'])
                elif direction != 'all'     :
                    text = ':red_circle: Unsupported direction `{0}` for `jira links` command. Current supported values are: `all`, `up`, `down`, `children` and `parents`'.format(direction)
                    return {"text": text, "attachments": attachments}

                #if direction == 'risks'   : graph.set_puml_link_types_to_add(['has RISK','creates RISK','creates R4','creates R3','creates R2','creates R1'])

                graph.add_all_linked_issues(keys, depth)
                graph_type = "{0}__{1}___depth_{2}".format(keys, direction, depth)
                if save_graph is False:
                    return graph
                graph_name = graph.render_and_save_to_elk(None, graph_type, channel, user)
                if only_create:
                    return graph, graph_name, depth, direction, target
                #slack_message("Created Graph with name: '{0}'".format(graph_name), [], channel)
                puml = graph.puml.puml
                max_size = 60000
                if channel and (not view) and len(puml) > max_size:            # only do this check when there is a channel and no view (meaning that the graph will be generated)
                    text = ':red_circle: for the graph `{0}` with `{1}` nodes and `{2}` edges, the PlantUML code generated from your query was too big `{3}` and rendering this type of large graphs doesn\'t work well in PlantUML (max allowed is `{4}`)'\
                                    .format(graph_name, len(graph.nodes), len(graph.edges), len(puml),max_size)
                else:
                    if view:            # if we have defined a view, render it here
                        graph_view          = Graph_View()
                        graph_view.graph    = graph
                        graph_view.graph.reset_puml()
                        graph_view.render_view(view,channel,team_id,graph_name)
                        puml = graph_view.graph.puml.puml
                        #slack_message('',[{'text':'```{0}```'.format(puml)}], channel)
                    else:
                        view = 'default'

                    if channel:  # if the channel value is provided return a user friendly message, if not, return the data
                        text = ':point_right: Created graph with name `{4}`, based on _{0}_ in the direction `{1}`, with depth `{2}`, with plantuml size: `{3}`, with view `{5}`, with `{6}` nodes and `{7}` edges'\
                                        .format(target, direction, depth, len(puml), graph_name, view, len(graph.nodes), len(graph.edges))
                        Lambda('utils.puml_to_slack').invoke_async({"puml": puml,"channel": channel, 'team_id' : team_id})
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
        Lambda('gs.elk_to_slack').invoke_async(event)
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

    def cmd_server(self, params, team_id=None, channel=None):
        attachments = []
        if len(params) < 2:
            text = ":exclamation: you must provide an server command"
        else:
            params.pop(0)                           # remove 1st command since it is 'server'
            command  = params.pop(0)
            data     = Secrets('sync-server-ngrok').value_from_json_string()
            username = data.get('username')
            password = data.get('password')
            if command[0] !='/':
                url = "https://gs-jira.ngrok.io/server/{0}".format(command)
            else:
                url = "https://gs-jira.ngrok.io{0}".format(command)
            result   = requests.get(url, auth=(username, password)).text
            text     = "{0}".format(result)
            #attachments = [{'text':url}]

        return {"text": text, "attachments": attachments}

    def cmd_down(self, params, team_id=None, channel=None, user=None):
        self.up_down("down", params, team_id, channel, user)

    def cmd_up(self, params, team_id=None, channel=None, user=None):
        self.up_down("up", params, team_id, channel, user)

    def cmd_load_sheet(self, params, team_id=None, channel=None):
        def send_slack_message(message):
            slack_message(message, [], channel, team_id)

        # def show_pdf(file_id,icon, when):
        #     send_slack_message('{0} this is what the file currently looks `{1}` the sync'.format(icon, when))
        #     Lambda('gsbot_gsuite.lambdas.gdocs').invoke({"params":['pdf', file_id], 'data':{'team_id':team_id,'channel': channel}})


        if len(params) < 2:
            text = ":exclamation: you must provide an gsuite `file_id` (you can find this on the url of the document you want to sync)"
            send_slack_message(text)
        else:
            params.pop(0)  # remove 1st command since it is 'server'
            file_id = params.pop(0)

            #send_slack_message(':point_right: Staring syncing workflow for file `{0}`'.format(file_id))
            #show_pdf          (file_id, ':one:', 'BEFORE')
            #send_slack_message(':two: syncing data ...')

            result = self.cmd_server(['server','/jira-sync/load-jira/{0}'.format(file_id)])
            #[trigger_sync_jira_sheets]
            status = json.loads(result.get('text')).get('status')
            send_slack_message('Execution result: `{0}`'.format(status))

            #show_pdf(file_id, ':three:','AFTER')

        return None,None


    def cmd_diff_sheet(self, params, team_id=None, channel=None):
        def send_slack_message(message):
            slack_message(message, [], channel, team_id)

        if len(params) < 2:
            text = ":exclamation: you must provide an gsuite `file_id` (you can find this on the url of the document you want to sync)"
            send_slack_message(text)
        else:
            params.pop(0)  # remove 1st command since it is 'server'
            file_id = params.pop(0)
            send_slack_message(':one: diffing data ...')
            result = self.cmd_server(['server','/jira-sync/diff-sheet/{0}'.format(file_id)])
            send_slack_message(result)

        return None,None

    def cmd_sync_sheet(self, params, team_id=None, channel=None):
        def send_slack_message(message):
            slack_message(message, [], channel, team_id)

        if len(params) < 2:
            text = ":exclamation: you must provide an gsuite `file_id` (you can find this on the url of the document you want to sync)"
            send_slack_message(text)
        else:
            params.pop(0)  # remove 1st command since it is 'server'
            file_id = params.pop(0)
            #send_slack_message(':one: diffing data ...')
            result = self.cmd_server(['server','/jira-sync/sync-sheet/{0}'.format(file_id)])
            status = Misc.get_value(Misc.json_load(result.get('text')),'status',result)
            send_slack_message('Execution result: `{0}`'.format(status))

        return None,None


    def cmd_version(self, params, team_id=None, channel=None):
        if team_id:
            slack_message(self.version, [], channel, team_id)
        else:
            return self.version


    # helpers

    def up_down(self, direction, params, team_id=None, channel=None, user=None):
        if len(params) != 3:
            text = ':red_circle: for the `jira {0}` command, you need to provide 2 parameters: ' \
                   '\n\t\t - `jira key or graph` '                                              \
                   '\n\t\t - `depth` '.format(direction)
            slack_message(text, [], channel, team_id)
            return

        target = params[1]
        depth  = int(params[2])
        params = ['links', target, direction, depth]


        (graph, graph_name, depth, direction, target) = self.cmd_links(params, team_id, channel, user, only_create=True)
        if graph:
            text = ':point_right: Created graph for `{0}` in the direction `{1}`, with depth `{2}`, with name `{3}`, with `{4}` nodes and `{5}` edges' \
                            .format(target, direction, depth, graph_name, len(graph.nodes), len(graph.edges))
            slack_message(text, [], channel, team_id)
            Lambda('lambdas.browser.lambda_browser').invoke_async({"data": {"team_id": team_id, "channel": channel}, "params": ['viva_graph', graph_name, 'default']})


    # main method

    def handle_request(self,event):
        #log_to_elk('in handle_request', event)
        params      = event.get('params')
        channel     = event.get('channel')
        team_id     = event.get('team_id')
        user        = event.get('user')
        attachments = []
        if params is None or len(params) < 1:
            text   = ":point_right: no command received, see `jira help` for a list of available commands`"
        else:
            command = params[0]
            try:
                if command == 'help'               : return self.cmd_help           ()
                if command == 'created_in_last'    : return self.cmd_created_in_last(params, team_id, channel)
                if command == 'created_between'    : return self.cmd_created_between(params, team_id, channel)
                if command == 'updated_in_last'    : return self.cmd_updated_in_last(params, team_id, channel)
                if command == 'issue'              : return self.cmd_issue          (params, team_id, channel)
                if command == 'links'              : return self.cmd_links          (params, team_id, channel, user)
                if command == 'up'                 : return self.cmd_up             (params, team_id, channel, user)
                if command == 'down'               : return self.cmd_down           (params, team_id, channel, user)
                if command == 'search'             : return self.cmd_search         (event          )
                if command == 'server'             : return self.cmd_server         (params, team_id, channel)
                if command == 'load_sheet'         : return self.cmd_load_sheet     (params, team_id, channel)
                if command == 'table'              : return self.cmd_table          (params, team_id, channel)
                if command == 'sync_sheet'         : return self.cmd_sync_sheet     (params, team_id, channel)
                if command == 'diff_sheet'         : return self.cmd_diff_sheet     (params, team_id, channel)
                if command == 'graph_sheet'        : return self.cmd_graph_sheet    (params, team_id, channel)
                if command == 'version'            : return self.cmd_version        (params, team_id, channel)

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