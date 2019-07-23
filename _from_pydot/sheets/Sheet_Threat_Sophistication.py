from api_jira.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync
from utils.Dev import Dev
from utils.Local_Cache import use_local_cache_if_available
from utils.Misc import Misc


class Sheet_Threat_Sophistication(API_Jira_Sheets_Sync):

    def __init__(self):
        self.file_id            = '1yDxu5YxL9FxY5wQ1EEQlAYGt3flIsm2VTyWwPny5RLA'
        super().__init__(self.file_id)
        self.issue_id           = 'IA-366'        # GSuite - Photobox Group
        self.sheet_title        = 'Vuln Data'
        self.backup_sheet_title = '(Original Data)'
        self.sophistication = { 'id_to_text' : { 'TM-38' : 'Advanced' ,
                                                 'TM-35' : 'Moderate' ,
                                                 'TM-34' : 'Low'     },
                                 'text_to_id': { 'Advanced' : 'TM-38' ,
                                                 'Moderate' : 'TM-35' ,
                                                 'Low'      : 'TM-34' }}
        self.used_at        = { 'id_to_text' : { 'TM-36'   : 'Internal' , 'TM-37'   : 'External'},
                                'text_to_id' : { 'Internal': 'TM-36'    , 'External': 'TM-37'   }}

    def get_issue_it_asset__jira_data(self):
        return self.jira().issue(self.issue_id)

    def get_vuln_data(self):
        issue = self.get_issue_it_asset__jira_data()
        linked_vulns = [('Key','Jira Link','Summary')]
        for key,linked_issues in issue.get('Issue Links').items():
            for linked_issue in linked_issues:
                if linked_issue.get('Issue Type') == 'Vulnerability':
                    link = '=HYPERLINK("https://jira.photobox.com/browse/{0}","{0}")'.format(key)
                    linked_vulns.append((key, link, linked_issue.get('Summary')))
        return linked_vulns

    # def set_sheet_with_vuln_data(self,vuln_data):
    #     result = self.gsheets().set_values(self.file_id,self.sheet_title,vuln_data)
    #     Dev.pprint(result)

    #def get_threats_mappings_status(self):
    #     sheet_data = self.get_sheet_raw_data()
    #     Dev.pprint(sheet_data)

    def set_sheet_threat_data_status(self,vuln_data):
        self.sheet_name()                           # ensures that the sheets exists
        self.sheet_name_backup()
        sheet_id = self.sheet_id()
        sheet_id_backup = self.sheet_id_backup()
        #request = self.gsheets().request_cell_set_value(sheet_id,3,2,'Low')

        #return
        #max = 10
        keys     = [item[0] for item in vuln_data[1:]]
        issues   = self.elastic().issues(keys)
        requests = []
        for index,key in enumerate(keys):
            issue               = issues.get(key)
            issue_links         = issue.get('Issue Links')
            can_be_exploited_at = issue_links.get('Can be exploited at')
            is_used_by          = issue_links.get('is used by')

            value = 'Not Known'
            if can_be_exploited_at:
                for link_key in can_be_exploited_at:
                    value = self.sophistication.get('id_to_text').get(link_key)
            requests.append(self.gsheets().request_cell_set_value(sheet_id       , 3, index+1, value))
            requests.append(self.gsheets().request_cell_set_value(sheet_id_backup, 3, index + 1, value))

            value_internal = 'Not Known'
            value_external = 'Not Known'
            if is_used_by:
                value_internal = 'No'
                value_external = 'No'
                for link_key in is_used_by:
                    value = self.used_at.get('id_to_text').get(link_key)
                    if value == 'Internal':
                        value_internal = 'Yes'
                    if value == 'External':
                        value_external = 'Yes'

            requests.append(self.gsheets().request_cell_set_value(sheet_id       , 4, index + 1, value_internal))
            requests.append(self.gsheets().request_cell_set_value(sheet_id       , 5, index + 1, value_external))
            requests.append(self.gsheets().request_cell_set_value(sheet_id_backup, 4, index + 1, value_internal))
            requests.append(self.gsheets().request_cell_set_value(sheet_id_backup, 5, index + 1, value_external))


        self.gsheets().execute_requests(self.file_id,requests)

    def get_diff_actions(self):
        actions = []
        sheet_data = self.get_sheet_raw_data(self.sheet_name())
        backup_data = self.get_sheet_raw_data(self.sheet_name_backup())
        for index, row in enumerate(sheet_data[1:]):
            backup_row = Misc.array_get(backup_data,index+1)
            if len(row) == 6 and backup_row:
                key = row[0]
                if row[3] != backup_row[3]:
                    sophistication_id = self.sophistication.get('text_to_id').get(row[3])
                    if sophistication_id is None:
                        actions.append({'value':row[3],'row':3, 'col':index+1,'key':key, 'action': 'delete-sophistication'})
                    else:
                        actions.append({'value':row[3],'row':3, 'col':index+1,'key':key, 'action': 'set-sophistication', 'link_key': sophistication_id })

                if row[4] != backup_row[4]:
                    internal_id = self.used_at.get('text_to_id').get('Internal')
                    if row[4] == 'Yes':
                        actions.append({'value':row[4],'row':4, 'col':index+1,'key': key, 'action': 'set-used-by-internal'   , 'link_key': internal_id})
                    else:
                        actions.append({'value':row[4],'row':4, 'col':index+1,'key': key, 'action': 'delete-used-by-internal', 'link_key': internal_id})

                if row[5] != backup_row[5]:
                    internal_id = self.used_at.get('text_to_id').get('External')
                    if row[5] == 'Yes':
                        actions.append({'value':row[5],'row':5, 'col':index+1,'key': key, 'action': 'set-used-by-external'   , 'link_key': internal_id })
                    else:
                        actions.append({'value':row[5],'row':5, 'col':index+1,'key': key, 'action': 'delete-used-by-external', 'link_key': internal_id })

        return actions

    def remove_links(self, from_id, link_type):
        try:
            issue_links = self.jira().issue_links(from_id).get(link_type)
            if issue_links:
                for issue_link in issue_links:
                    link_id = issue_link.get('Id')
                    self.jira().issue_delete_link(link_id)
                    print('deleting link', from_id, link_type, link_id)

            return "ok"
        except Exception as error:
            return "Error: {0}".format(error)

    def remove_links_to_target(self, from_id, link_type, to_id):
        try:
            issue_links = self.jira().issue_links(from_id).get(link_type)
            if issue_links:
                for issue_link in issue_links:
                    if to_id == issue_link.get('Key'):
                        link_id = issue_link.get('Id')
                        print('deleting link', from_id, link_type, link_id)
                        self.jira().issue_delete_link(link_id)
            return "ok"
        except Exception as error:
            return "Error: {0}".format(error)

    def remove_links_and_add_new_link(self, from_id, link_type, to_id):
        try:
            status = self.remove_links(from_id,link_type)
            if status != 'ok':
                return status

            print('adding link',from_id, link_type, to_id)
            self.jira().issue_add_link(from_id, link_type, to_id)
            return "ok"
        except Exception as error:
            return "Error: {0}".format(error)

    def add_new_link(self, from_id, link_type, to_id):
        try:
            print('adding link',from_id, link_type, to_id)
            self.jira().issue_add_link(from_id, link_type, to_id)
            return "ok"
        except Exception as error:
            return "Error: {0}".format(error)


    def apply_diff_actions(self,diff_actions):
        sheet_id        = self.sheet_id()
        sheet_id_backup = self.sheet_id_backup()

        action_sheet_data = [("(col)","(row)","Key","Action","Link Type","Link_Key","Value","Update Status")]
        requests          = []
        for diff_action in diff_actions:
            action    = diff_action.get('action')
            key       = diff_action.get('key')
            key_link  = '=HYPERLINK("https://jira.photobox.com/browse/{0}","{0}")'.format(key)
            link_key  = diff_action.get('link_key','')
            value     = diff_action.get('value')
            col       = diff_action.get('row')  # BUG these are wrong in the whole script!!!
            row       = diff_action.get('col')
            link_type = None
            if action == 'set-sophistication':
                link_type = 'Can be exploited at'
                status = self.remove_links_and_add_new_link(key, link_type,link_key)
            elif action == 'delete-sophistication':
                link_type = 'Can be exploited at'
                status = self.remove_links(key, link_type)
            elif action == 'delete-used-by-internal' or  action == 'delete-used-by-external':
                link_type = 'is used by'
                status = self.remove_links_to_target(key, link_type,link_key)
            elif action == 'set-used-by-internal' or action == 'set-used-by-external':
                link_type = 'is used by'
                status = self.add_new_link(key,link_type,link_key)
            else:
                status = 'Error: action not implemented:'.format(action)

            action_sheet_data.append((col, row, key_link, action, link_type, link_key, value, status))            # update the actions sheet requests

            if status == 'ok':                                                                                    # if the action went ok,
                requests.append(self.gsheets().request_cell_set_value(sheet_id_backup, col, row, value))          #   update the backup sheet with the new value
                requests.append(self.gsheets().request_cell_set_background_color(sheet_id_backup, col, row,0.5,0.5,1.0)) # provide a visual update that the update worked ok

        if len(requests) > 0:
            self.gsheets().execute_requests(self.file_id,requests)

        action_sheet = 'Actions'
        self.gsheets().clear_values(self.file_id, action_sheet)
        from time import sleep
        sleep(0.5)                  # DC: I think I saw a race condition with some gsuite updates
        self.gsheets().set_values(self.file_id,action_sheet,action_sheet_data)

    def load_data(self):
        vuln_data = self.get_vuln_data()
        self.set_sheet_threat_data_status(vuln_data)

    def sync_data(self):
        diff_actions = self.get_diff_actions()
        self.apply_diff_actions(diff_actions)