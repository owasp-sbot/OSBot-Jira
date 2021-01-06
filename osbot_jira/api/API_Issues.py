from osbot_aws.helpers.Lambda_Helpers import log_error
from osbot_elastic.Elastic_Search import Elastic_Search

from osbot_jira.api.plantuml.Puml import Puml
from osbot_jira.api.plantuml.Puml_Table import Puml_Table


class API_Issues:
    def __init__(self, index = 'jira'):
        self.secrets_id = 'gw-elastic-server-1'
        self.index      = index
        self._elastic   = None

    def elastic(self):
        if self._elastic is None:
            #current_host_online()
            self._elastic = Elastic_Search(aws_secret_id=self.secrets_id, index=self.index)
        return self._elastic

    def epic_issues(self, epic_key):
        query = {"_source": ["Key"], "query": {"wildcard": {"Epic Link.keyword": epic_key}}}
        return [result.get('Key') for result in self.elastic().search_using_query(query)]

    def issue(self,key):
        try:
            #self.elastic().index = self.resolve_es_index(key)
            #if self.elastic().index:
            data = self.elastic().get_data(key.upper())
            if data:
                return data['_source']
        except Exception as error:
            log_error(str(error),'API_Elastic_Lambda.issue')
        return {}

    def issues(self, keys):
        keys = list(filter(None, keys))               # remove null values (which will cause elastic to throw an exception)
        if len(keys)  == 0:
            return []
        return self.elastic().get_many(keys)

        # the code below was needed when the issue were distributed across multiple elastic indexes, which is something we shouldn't support here
        # issues = {}
        # keys_by_index = {}
        # for key in keys:
        #     index = self.resolve_es_index(key)
        #     if index:
        #         if keys_by_index.get(index) is None: keys_by_index[index]=[]
        #         keys_by_index[index].append(key)
        # for index, keys in keys_by_index.items():
        #     matches = self.elastic().set_index(index).get_many(keys)
        #     issues.update(matches)
        # return issues
        #return self.api.elastic.get_many(keys)              # need to add support for fetching multiple indexes

    def issues_created_in_last_seconds(self, seconds): return self.issues_created_in_last("{0}s".format(seconds))
    def issues_created_in_last_minutes(self, minutes): return self.issues_created_in_last("{0}m".format(minutes))
    def issues_created_in_last_hours  (self, hours  ): return self.issues_created_in_last("{0}h".format(hours  ))
    def issues_created_in_last_days   (self, days   ): return self.issues_created_in_last("{0}d".format(days   ))
    def issues_created_in_last_weeks  (self, weeks  ): return self.issues_created_in_last("{0}w".format(weeks  ))
    def issues_created_in_last_months (self, months ): return self.issues_created_in_last("{0}M".format(months ))
    def issues_created_in_last_years  (self, years  ): return self.issues_created_in_last("{0}y".format(years  ))

    def issues_created_in_last(self,period):        # can be 1h , 1d, 1w
        return self.elastic().get_data_between_dates("Created","now-{0}".format(period),"now")


    def issues_updated_in_last(self,period):        # can be 1h , 1d, 1w
        return self.elastic().get_data_between_dates("Updated","now-{0}".format(period),"now")

    def issues_all(self, index = 'jira'):
        self.elastic().index = index
        query = { "query": {"match_all": {}}}
        results = {}
        for issue in self.elastic().search_using_query(query):
            results[issue['Key']] = issue
        return results

    def issues_all_indexes(self):
        issues = {}
        issues.update(self.issues_all('jira'))
        issues.update(self.issues_all('it_assets'))
        issues.update(self.issues_all('sec_project'))
        return issues

    # def issues_all_cached(self, index='jira'):
    #     return self.issues_all(index)

    # def issues_all_indexes_cached(self):
    #     issues = {}
    #     issues.update(self.issues_all_cached('jira'))
    #     issues.update(self.issues_all_cached('it_assets'))
    #     issues.update(self.issues_all_cached('sec_project'))
    #     return issues

    def labels(self):
        query = { "_source": ["Key","Labels"]}
        data  = {}
        for item in self.elastic().search_using_query(query):
            key    = item.get('Key')
            labels = item.get('Labels')
            if labels:
                for label in labels:
                    if data.get(label) is None: data[label] = []
                    data[label].append(key)
        return data

    def link_types(self, index="all"):
        query   = {"_source": ["Key", "Issue Links"], }
        original_index = self.elastic().get_index()
        results = []
        if index == "all":
            #results += self.elastic().set_index('it_assets'  ).search_using_query(query)
            #results += self.elastic().set_index('sec_project').search_using_query(query)
            results += self.elastic().set_index('jira'       ).search_using_query(query)
        else:
            results += self.elastic().set_index(index).search_using_query(query)

        self.elastic().set_index(original_index)
        return self.link_types_from_issues(results)

    def link_types_from_issues(self, issues, only_link_to = []):
        data = {}
        for item in issues:
            if item is None: continue
            key         = item.get('Key')
            issue_links = item.get('Issue Links')
            if issue_links:
                for issue_type, child_keys in issue_links.items():
                    if issue_type == '_all': continue
                    if data.get(issue_type) is None: data[issue_type] = {}
                    if len(only_link_to) == 0:
                        data[issue_type][key] = child_keys
                    else:
                        data[issue_type][key] = []
                        for child_key in child_keys:                                    # for all keys in the current issue_type
                            if child_key in only_link_to:                               # check if it is there before adding it
                                data[issue_type][key].append(child_key)
        return data

    def keys(self):
        query = { "_source": ["Key"], "query": {"match_all": {}} }
        return [ item['Key'] for item in self.elastic().search_using_query(query) ]


    def search(self, raw_text = "", field=None, size=None):
        if size is None  : size = 10000
        if field is None : field = "Summary"

        text = "{0}".format(raw_text.lower())  # ES seems to provide better results in lower case
        if field != "Labels":
            text = "*{0}*".format(text)         # when not searching on Labels do an wider search

        query = {
            "_source": ["Key", "Summary", field],
            "query"  : { "bool": {
                            "should": [ {"wildcard": { field     : text}},
                                        {"match": { "Key.keyword": { "query": raw_text.upper()}}}
                                      ] }},
            "sort"   : ["Summary.keyword"]
        }
        results = self.elastic().search_using_query(query, size)
        return list(results)

    def search_using_lucene(self, query, size=None):
        if size is None  : size = 10000
        results = self.elastic().search_using_lucene(query, size)
        return list(results)                                        # convert to list due since it seems easier for callers to have it already normalised (and not in a generator)

    def resolve_es_index(self, key):
        return 'jira'
        # if key:
        #     if "SEC-"   in key:  return 'sec_project'
        #     if "GSP-"   in key:  return 'it_assets'
        #     if "IA-"    in key:  return 'it_assets'
        #     if "TM-"    in key:  return 'it_assets'
        #     if "GDPR-"  in key:  return 'it_assets'
        #     if "GSOKR-" in key:  return 'it_assets'
        #     if "SC-"    in key:  return 'it_assets'
        #     if "GSSP-"  in key:  return 'it_assets'
        #     if "RT-"    in key:  return 'it_assets'
        #     if "SL-"    in key:  return 'it_assets'
        #     if 'GSOS-'  in key:  return 'it_assets'
        #     if 'GSCS-'  in key:  return 'it_assets'
        #     if 'GSBOT-' in key:  return 'it_assets'
        #     if 'GSED-'  in key:  return 'it_assets'
        #    return "jira"

    def set_default_indexes(self):
        self.elastic().index = 'jira'

    ### move these to separate analysis file

    # def graph_issue_links(self,key):
    #     issue = self.issue(key)
    #     graph = API_Pydot()
    #     root_node = graph.add_node(issue['Key'])
    #     for key, links in issue['Issue Links'].items():
    #         type_node = graph.add_node(key)
    #         graph.add_edge(root_node,type_node)
    #         for link in links:
    #             graph.add_edge(type_node, link)
    #     #Dev.pprint(issue)
    #     return graph


    def graph_issue_links_plant_uml(self,key):
        issue = self.issue(key)
        if issue == {}:
            return None


        root_key = issue['Key']
        root_summary = "{0} - {1} ".format(root_key, issue['Summary'])
        puml = Puml()
        puml.startuml()
        puml.add_card(root_summary,root_key)
        #if issue['Issue Links'].get('_all'):
        #    del issue['Issue Links']['_all']
        for key, links in issue['Issue Links'].items():
            puml.add_card(key,key).add_edge(root_key,key)
            for link in links:
                link_issue = self.issue(link)
                summary = link_issue.get('Summary')
                if (summary):
                    if len(summary) > 30:
                        summary = "{0} - {1}".format(link, summary[0:30] + "...")
                else:
                    summary = link
                puml.add_card(summary, link).add_edge(key, link)
        puml.enduml()

        return puml

    def create_issue_table(self, key):
        issue = self.issue(key)
        table = Puml_Table()

        (table.set_title("Details for Issue: <b>{0}</b>".format(key))
                   .set_object(issue)
                   .render())
        return table

    def server_url(self):
        host = self.elastic().host
        if '5766d93460d' in host: return "https://glasswall.atlassian.net"
        return host


    # def graph_issue_links_plant_uml(self,key):
    #     issue = self.issue(key)
    #     del issue['Issue Links']['_all']
    #     root_key = issue['Key']
    #
    #     puml = Puml()
    #     puml.startuml()
    #
    #     puml.add_card(root_key,root_key)
    #     for key, links in issue['Issue Links'].items():
    #         puml.add_card(key,key).add_edge(root_key,key)
    #         for link in links:
    #             puml.add_card(link, link).add_edge(key, link)
    #     puml.enduml()
    #
    #     return puml


    # def slack_buttons_for_linked_issues(self,key):
    #     issue       = self.issue(key)
    #     callback_id = 'view-jira-issue'
    #
    #
    #     #text        = "JIRA Helper (v0.1)"
    #     attachments = [
    #                      {
    #                          "text"             : "What Jira ID you want to see",
    #                          "fallback"         : "Not supported",
    #                          "callback_id"      : "{0}".format(callback_id),
    #                          "color"            : "#3AA3E3",
    #                          "attachment_type"  : "default",
    #                          "actions"          : []
    #
    #                      }
    #                   ]
    #
    #     for issue_link in issue['Issue Links']['_all']:
    #         attachments[0]['actions'].append( {
    #                         "name" : "key",
    #                         "text" : issue_link,
    #                         "type" : "button",
    #                         "value": issue_link
    #                     })
    #
    #     return attachments


