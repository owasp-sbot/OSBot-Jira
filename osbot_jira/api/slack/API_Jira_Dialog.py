from osbot_aws.helpers.Lambda_Helpers import slack_message, log_to_elk
from osbot_aws.apis.Lambda import Lambda
from osbot_jira.api.slack.API_Slack_Attachment import API_Slack_Attachment
from osbot_jira.api.slack.API_Slack_Dialog import API_Slack_Dialog


#todo: add unit tests and fix old PBX lambda references (those lambdas don't exist any more)
class API_Jira_Dialog():

    def get_dialog_issue(self):
        return  {
                    "callback_id"   : "jira-view-issue-dialogue",
                    "title"         : "JIRA issue viewer",
                    "submit_label"  : "Request",
                    "elements"      : [
                                         {
                                           "type": "text",
                                           "label": "key",
                                           "name": "key",
                                           "value" : "RISK-424",
                                           "hint": "What JIRA issue do you want to see"
                                         }
                                      ]}

    def get_dialog_graph_chooser(self):
        return {
                    "callback_id": "jira-graph-chooser",
                    "title": "JIRA Graph Chooser",
                    "submit_label": "View",
                    "elements": [
                        {
                          "label": "Graph to render:",
                          "type": "select",
                          "name": "graph_name",
                          "value": "org-chart",
                          "options": [
                            {
                              "label": "Org Chart",
                              "value": "org-chart"
                            },
                            {
                              "label": "SEC-9195",
                              "value": "sec-9195"
                            }
                          ]
                        },
                        # {
                        #     "type": "text",
                        #     "label": "key",
                        #     "name": "key",
                        #     "value": "RISK-424",
                        #     "hint": "What JIRA issue do you want to see"
                        #
                        # },
                    ]
                }

    def get_dialog_issue_links(self,keys='FACT-47'):
        return  {
                    "callback_id"   : "jira-view-issue-links",
                    "title"         : "JIRA issue Links viewer",
                    "submit_label"  : "Request",
                    "elements"      : [
                                         {
                                           "type": "text",
                                           "label": "keys ",
                                           "name": "keys",
                                           "value" : keys,
                                           "hint": "What are the seed Jira issues (comma-delimited list)"
                                         },
                                         {
                                             "type": "text",
                                             "label": "link's path",
                                             "name": "links_path",
                                             "value": "supports RISK, creates R3, creates R2, creates R1, has Stakeholder",
                                             "hint": "Describe the issue link's path you want to see (comma-delimited list)"
                                         }
                                        ,{
                                            "label": "View engine:",
                                            "type": "select",
                                            "name": "view_engine",
                                            "value": "normal",
                                            "options": [
                                              {
                                                "label": "Normal",
                                                "value": "normal"
                                              },{
                                                "label": "Normal (top down)",
                                                "value": "normal-top-down"
                                              },
                                              {
                                                "label": "with all links",
                                                "value": "with-all-links"
                                              }
                                            ]
                                          }]}


    ## METHODS ABOVE ARE LEGACY and need to be deleted

    def call_lambda_jira_view_issue_links(self,data, key, path, view_engine, channel):
        slack_message("Rendering issue-links graph for key `{0}` with path `{1}` and view engine `{2}`".format(key, path, view_engine), [], channel)

        data['submission']['keys'] = key
        data['submission']['links_path'] = path
        data['submission']['view_engine'] = view_engine
        self.handle_callback_jira_view_issue_links(data)


    def handle_button_dialog_test(self, data):
        trigger_id = data.get('trigger_id')
        slack_dialog = API_Slack_Dialog().test_render()
        self.show_dialog(trigger_id, slack_dialog)
        return {"text": "Opening test dialog ...", "attachments": [], 'replace_original': False}

    def handle_callback_issue_search_dialog(self, data):
        channel     = data['channel']['id']
        key         = data.get('submission').get('key')
        if key is None:
            key     = data.get('submission').get('key_direct')
        view_type   = data.get('submission').get('view-type')
        view_engine = data.get('submission').get('view-engine')

        user_id     = data['user']['id']

        if view_type == 'table':
            slack_message("Generating table for key: {0}".format(key), [], channel)
            Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke_async({"params": ["issue", key], "user": user_id, "channel": channel})
            #slack_message(result.get('text'), result.get('attachments'), channel)

        elif view_type == 'issue-links-vuln-path':
            path          = 'is parent of, supports RISK, creates R3, creates R2, creates R1, has Stakeholder'
            view_engine   = view_engine
            self.call_lambda_jira_view_issue_links(data, key, path, view_engine, channel)

        elif view_type == 'issue-links-stakeholder-path':
            path          = 'is Stakeholder,is created by R3, is created by R2, is created by R1'
            view_engine   = view_engine
            self.call_lambda_jira_view_issue_links(data, key, path, view_engine, channel)

        elif view_engine == 'issue-links-all-depth-1':
            view_engine = view_engine
            self.call_lambda_jira_view_issue_links(data, key, "", view_engine, channel)

        # elif view_type == 'issue-links-view-all':
        #     path          = 'is parent of, supports RISK, creates R3, creates R2, creates R1, has Stakeholder'
        #     view_engine   = view_engine
        #     self.call_lambda_jira_view_issue_links(data, key, path, view_engine, channel)

            #Lambdas('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke_async({"params": ["issue-links", key], "channel": channel})
        else:
            log_to_elk("Error: un-supported view engine `{0}` for key `{1}`".format(view_type,key),level= 'error')



    def handle_callback_jira_view_issue_links(self, data):
        submission  = data.get('submission')
        payload = {
            'type'       : 'show-issue-links'                             ,
            'channel'    : data['channel']['id']                          ,
            'keys'       : submission.get('keys')                         ,
            'links_path' : submission.get('links_path' ).replace('+', ' '),
            'view_engine': submission.get('view_engine').replace('+', ' '),
            'data'       : data
        }
        slack_message('invoking gs.jira_graphs for keys  {0}'.format(payload['keys']), [], payload['channel'])
        Lambda('gs.jira_graphs').invoke_async(payload)


    def handle_dialog_submission(self, data):
        callback_id = data['callback_id']
        channel     = data['channel']['id']
        user_id     = data['user']['id']

        if callback_id =='jira-graph-chooser':
            graph_name = data['submission'].get('graph_name')
            Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke_async({"params": ["graph", graph_name], "user": user_id, "channel": channel})

        elif callback_id == 'jira-view-issue-links':
            self.handle_callback_jira_view_issue_links(data)

        elif callback_id == 'jira-view-issue-dialogue':
            slack_message('jira-view-issue-dialogue: {0}'.format(data),[], channel)
            key     = data.get('submission').get('key')
            result  = Lambda('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke({"params": ["issue", key], "user": user_id, "channel": channel})
            slack_message(result.get('text'), result.get('attachments'), channel)

        # elif callback_id == 'issue-search-dialog':
        #     self.(data)

        else:
            error_message = ":red_circle: Dialog callback_id not supported: {0}".format(callback_id)
            slack_message(error_message, [], channel)
            #self.api_slack.send_message(error_message, channel=channel)

        return None

    def handle_jira_dialog_action(self, data):
        trigger_id = data.get('trigger_id')
        action = data.get('actions').pop(0).get('value')
        if action == 'search-for-issues' : self.show_dialog(trigger_id, self.get_dialog_search_for_issues())
        if action == 'show-fact-47-story': self.show_dialog(trigger_id, self.get_dialog_issue_links('FACT-47'))
        else                             : self.show_dialog(trigger_id, self.get_dialog_issue_links(None))

        return {"text": "Opening dialog window ... `{0}`".format(action), "attachments": [], 'replace_original': False}

    def handle_jira_slash_command(self, data):

        trigger_id = data.get('trigger_id')
        text       = data.get('text').replace('+', ' ') #hack: fix slack double encoding

        if   text == 'issue'            : return self.show_dialog(trigger_id, self.get_dialog_issue            ())
        elif text == 'links'            : return self.show_dialog(trigger_id, self.get_dialog_issue_links      ())
        elif text == 'graphs'           : return self.show_dialog(trigger_id, self.get_dialog_graph_chooser    ())
        elif text == 'search'           : return self.show_dialog(trigger_id, self.get_dialog_search_for_issues())
        else                            : return self.show_buttons_with_examples()

    def show_dialog(self,trigger_id,dialog):
        payload = {"trigger_id": trigger_id, "dialog": dialog}
        Lambda('utils.slack_dialog').invoke(payload)
        return "Opening up Jira Slack Dialog window..."  # for Slack Commands we need to send a message back (or the user sees a 'None' message

    def show_buttons_with_examples(self):

        attachments = API_Slack_Attachment()                                                                 \
                        .set_callback_id("jira-dialog-action"                                             )  \
                        .set_text       ('What would you like to do?'                                     )  \
                        .add_button     ("graph-type" , "Search for issues"   , "search-for-issues"       )  \
                        .add_button     ("graph-type" , "Fact-47 story"      , "show-fact-47-story"     )
                        #.add_button     ("graph-type" , "GS OKR example"      , "show-gs-okr-example"     )

        return {"text": "" , "attachments": attachments.render()}

