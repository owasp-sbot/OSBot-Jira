import  datetime
from    time import time, localtime, strftime

from osbot_aws.helpers.Lambda_Helpers import log_info, log_error
from osbot_elastic.Elastic_Search import Elastic_Search
from osbot_utils.utils.Dev import Dev

from osbot_jira.api.jira_server.API_Jira import API_Jira
from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest


class GW_Elastic_Jira:
    def __init__(self, index_id = 'jira', projects = None):
        self.secrets_id     = 'gw-elastic-server-1'
        self.index_id       = index_id
        self.elastic        = None
        self.api_Jira       = API_Jira()
        self.projects       = projects #'IA, TM,GDPR'

    def reload_all_data_from_jira_project(self): # todo: find better location to do this (reloading of elastic data)
        self.re_create_index()
        self.send_data_from_project()

    def re_create_index(self):         # note that this will delete the index and recreate it
        self.elastic.delete_index()               \
                    .create_index()
        # self.elastic.delete_index()             \
        #             .delete_index_pattern()     \
        #             .create_index()             \
        #             .create_index_pattern(add_time_field=False)
        return self

    def setup(self):
        if self.elastic is None:
            self.elastic = Elastic_Search(self.index_id,self.secrets_id)
        return self

    def fix_issues_for_elk(self,issues):
        return [self.fix_issue_for_elk(issue) for issue in issues]

    def fix_issue_for_elk(self,issue):
        items = {} #{'_all': [] }                                  # fix issue links
        for key, issue_links in issue['Issue Links'].items():
            #items['_all'].append(key)                          # capture a list of all ids
            for issue_link in issue_links:
                link_type = issue_link['Link Type']
                if items.get(link_type) is None:                   # and index them by link_type
                    items[link_type] = []
                items[link_type].append(key)
        issue['Issue Links'] = items

        if issue['Rating'] ==  'To be determined':
            issue['Rating']= 'TBD'
        if issue['Project'] == 'VULN (Vulnerability)':
            issue['Project'] = 'VULN'

        #Dev.pprint(issue)

        return issue

    def send_data_from_project(self, project=None):
        if project:
            jql = 'project={0}'.format(project)
        else:
            jql = ''                                                        # todo: find a better way to get all results from Jira

        api_jira_rest = API_Jira_Rest()
        issues = api_jira_rest.search(jql)

        return self.elastic.add_bulk(issues, "Key")

    def issue_get(self,issue_id):
        try:
            data = self.elastic.get_data(issue_id)
            return data['_source']
        except Exception as error:
            log_error(str(error),'API_Elastic_Jira.issue_get')
            return {}

    def issue_update(self, issue):
        return self.elastic.add(issue, "Key")

    def reset_update_index_value(self):
        update_key = '_update_details'
        self.elastic.delete_data_by_id(update_key)
        return self

    def update_index_from_jira_changes(self):
        if self.projects is None:
            log_error("Cannot update ELK since self.projects value is not configured")
            return
        update_key = '_update_details'              # code to store last updated time in the index (move this to a dedicated location)
        data       = self.elastic.get_data(update_key)
        if data is None:
            update_key_data = {
                                  "Key": update_key,
                                  "last_updated_at": None
                              }
            epoch = (datetime.datetime.now() - datetime.timedelta(0, 60 * 1440)).timestamp()         # if the value is not set , go back 24 h
            when            = strftime("%Y/%m/%d %H:%M", localtime(epoch))
        else:
            update_key_data = data['_source']
            when            = update_key_data['last_updated_at']

        now_epoch = time() - 120 # due to the current issue with the sync server, remove 2 minutes from the time() value (which is the current time in seconds since the Epoch)

        now    = strftime("%Y/%m/%d %H:%M", localtime(now_epoch))                      # capture this value here (as soon as possible)

        now_server = strftime("%Y/%m/%d %H:%M",localtime(time()))
        print(" > using {0}  , localtime: {1}".format(now,now_server))

        query  = 'project in ({0}) AND updated >= "{1}"'.format(self.projects,when)
        changes = self.api_Jira.search_no_cache(query)
        if len(changes) == 0:
            log_info("No issues updated since: {0}".format(when),"API_Elastic_Jira.update_index_from_jira_changes")
            return



        log_info(Dev.pprint("Since {0}, there where {1} issues updated: {2}".format(when, len(set(changes)),set(changes))),
                            "API_Elastic_Jira.update_index_from_jira_changes")

        issues = self.fix_issues_for_elk(changes.values())

        result = self.elastic.add_bulk(issues, "Key")
        log_info(Dev.pprint("sent {0} issues to elk instance: {1}".format(result, self.secrets_id)),
                            "API_Elastic_Jira.update_index_from_jira_changes")

        update_key_data['last_updated_at'] = now
        self.elastic.add(update_key_data, "Key")


    def add_changed_log_status(self, project, start_at=0, max =-1):
        jql = "Project={0}".format(project)
        statuses = self.api_Jira.issue_changes_log_only_status(jql, start_at, max)
        data = []
        for key,items in statuses.items():
            for entry in items:
                entry['Key'    ] = key
                entry['Project'] = project
                data.append(entry)

        self.elastic.add_bulk(data, "Entry_Id")
        return data


    # def reload_jira_index__jira(self):           # need to do also do this for the SEC project
    #     index = 'jira'
    #
    #     query = {  "query": { "match_all": {} } }
    #     self.elastic.index = index
    #     result     = self.elastic.delete_using_query(query)     # delete all items
    #     fact_issues = self.send_data_from_project('FACT')       # add all issues from FACT project
    #     risk_issues = self.send_data_from_project('RISK')       # add all issues from RISK project
    #     vuln_issues = self.send_data_from_project('VULN')       # add all issues from VULN project
    #
    #
    #     stats =  { "stats": {
    #                         "index"             : index             ,
    #                         "delete_issues"     : result['deleted'] ,
    #                         "fact_issues_added" : fact_issues       ,
    #                         "risk_issues_added" : risk_issues       ,
    #                         "vuln_issues_added" : vuln_issues
    #                       }}
    #     Dev.pprint(stats)
    #     return stats

    # def reload_jira_index__sec_project(self):
    #     index = 'sec_project'
    #     query = {"query": {"match_all": {}}}
    #     self.elastic.index = index
    #     result = self.elastic.delete_using_query(query)  # delete all items
    #     step_by    = 500
    #     sec_issues = 0
    #     max        = 22         # do up to 11000        - at the moment there are 8k
    #     for i in range(0, max):
    #         start_at = i * step_by
    #         last_count = self.send_data_from_project('SEC', start_at, step_by)
    #         sec_issues += last_count
    #         Dev.print("[{0}/{1}] reload_jira_index__sec_project - added {2} (total: {3}".format(i,max, last_count, sec_issues))
    #         if last_count == 0:
    #             break;
    #     stats = { "stats": {
    #                         "index"             : index             ,
    #                         "delete_issues"     : result['deleted'] ,
    #                         "sec_issues_added"  : sec_issues        ,
    #                       }}
    #     Dev.pprint(stats)
    #     return stats

    # def reload_jira_index__it_Assets(self):           # need to do also do this for the SEC project
    #     index = 'it_assets'
    #     self.elastic.index = index
    #     query = {  "query": { "match_all": {} } }
    #     result     = self.elastic.delete_using_query(query)     # delete all items
    #
    #     slack_message(':point_right: starting reload_jira_index__it_Assets', [], 'DDKUZTK6X', 'T7F3AUXGV')
    #
    #     ia_issues    = self.send_data_from_project('IA')
    #     tm_issues    = self.send_data_from_project('TM')
    #     gdpr_issues  = self.send_data_from_project('GDPR')
    #     gsp_issues   = self.send_data_from_project('GSP')
    #     gsokr_issues = self.send_data_from_project('GSOKR')
    #     rt_issues    = self.send_data_from_project('RT')
    #     fix_issues   = self.send_data_from_project('FIX')
    #     sc_issues    = self.send_data_from_project('SC')
    #     gssp_issues  = self.send_data_from_project('GSSP')
    #     sl_issues    = self.send_data_from_project('SL')
    #     gsos_issues  = self.send_data_from_project('GSOS')
    #     gscs_issues  = self.send_data_from_project('GSCS')
    #     gsbot_issues = self.send_data_from_project('GSBOT')
    #     gsed_issues  = self.send_data_from_project('GSED')
    #
    #     stats = { "stats": {
    #                         "index"             : index             ,
    #                         "delete_issues"     : result['deleted'] ,
    #                         "ia_issues_added"   : ia_issues         ,
    #                         "tm_issues_added"   : tm_issues         ,
    #                         "gdpr_issues_added" : gdpr_issues       ,
    #                         "gsp_issues_added"  : gsp_issues        ,
    #                         "gskr_issues_added" : gsokr_issues      ,
    #                         "rt_issues_added"   : rt_issues         ,
    #                         "fix_issues_added"  : fix_issues        ,
    #                         "sc_issues"         : sc_issues         ,
    #                         "gssp_issues"       : gssp_issues       ,
    #                         "sl_issues"         : sl_issues         ,
    #                         "gsos_issues"       : gsos_issues       ,
    #                         "gscs_issues"       : gscs_issues       ,
    #                         "gsbot_issues"      : gsbot_issues      ,
    #                         "gsed_issues"       : gsed_issues
    #                       }}
    #     Dev.pprint(stats)
    #     slack_message(json.dumps(stats), [], 'DDKUZTK6X','T7F3AUXGV')
    #     return stats


    # def find_deleted_keys(self, project):
    #     jql           = 'project={0}'.format(project)
    #     count         = 0
    #     max_per_query = 100
    #     #data          = self.api_gs_jira.api_Jira.jira().search_issues(
    #     #                    jql,
    #     #                    startAt    = count,
    #     #                    maxResults = max_per_query,
    #     #                    fields     = 'Key'
    #     #                    )
    #     issues = self.api_gs_jira.api_Jira.search_no_cache(jql,max = 2, fields=['key', 'summary'])
    #
    #     Dev.pprint(len(issues))
    #     #Dev.pprint(len(data))

