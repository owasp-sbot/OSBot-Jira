from osbot_jira.api.API_Issues import API_Issues
from osbot_jira.api.GS_Bot_Jira import GS_Bot_Jira
from osbot_jira.api.elk.Elk_To_Slack import ELK_to_Slack
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph
from osbot_jira.api.graph.Lambda_Graph_Commands import Lambda_Graph_Commands


def set_up_ctor_cache(base_obj, target_class):
    variable_name = "_" + target_class.__name__             # temp variable to store object
    if getattr(base_obj, variable_name,None) is None:       # check if it exists
        setattr(base_obj, variable_name, target_class())    # created it by calling ctor
    return getattr(base_obj, variable_name)                 # return value


class Jira:
    #def __init__(self):

    # helper classes
    def api_issues    (self): return set_up_ctor_cache(self, API_Issues)
    def elk_to_slack  (self): return set_up_ctor_cache(self, ELK_to_Slack)
    def gs_bot_jira   (self): return set_up_ctor_cache(self, GS_Bot_Jira)
    def graph_commands(self): return set_up_ctor_cache(self, Lambda_Graph_Commands)
    def lambda_graph  (self): return set_up_ctor_cache(self, Lambda_Graph)



    # methods
    def issue(self, issue_id):
        return self.api_issues().issue(issue_id)


    def issues(self, issue_id):
        return self.api_issues().issues(issue_id)


    def search(self, query):
        params = query.split(' ')
        query = self.elk_to_slack().get_search_query(params)
        return self.api_issues().search_using_lucene(query)

    def graph_links(self, target, direction, depth):
        return self.lambda_graph().graph_links(target, direction, depth)

        #params = ['links', source, direction, depth]
        #€return self.gs_bot_jira.cmd_links(params, save_graph=False)


    def graph_expand(self, source, depth, link_types):
        params = [source, depth, link_types]
        return self.graph_commands().expand(params=params, save_graph=False)