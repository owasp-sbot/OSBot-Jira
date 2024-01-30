from unittest import TestCase


from osbot_jira.api.jira_server.rest_api.Backup_Jira_to_Local_Folder import Backup_Jira_to_Local_Folder
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists


class test_Backup_Jira_to_Local_Folder(TestCase):

    def setUp(self) -> None:
        self.backup_jira = Backup_Jira_to_Local_Folder()

    def test__init__(self):
        pprint(self.backup_jira.target_folder)

    def test_setup(self):
        assert self.backup_jira.setup() == self.backup_jira
        assert folder_exists(self.backup_jira.target_folder)
        assert folder_exists(self.backup_jira.issues_folder)
        assert folder_exists(self.backup_jira.metadata_folder)

    def test_save_stats(self):
        self.backup_jira.save_stats()

    def test_save_projects_metadata(self):
        self.backup_jira.save_projects_metadata()


    def test_save_jira_data(self):
        stats_data = self.backup_jira.save_jira_data()
        pprint(stats_data)


    def test_save_jira_issues_updated_since_last_update(self):
        self.backup_jira.api_jira_rest.log_requests=True
        result = self.backup_jira.save_jira_issues_updated_since_last_update()
        pprint(result)

    # todo refactor into method (or class) that identifies issues that have been deleted
    #  (and deals with the issue links that point to them)
    def test___fix_gaps_caused_by_deleted_node(self):
        from osbot_jira.api.jira_server.local.Jira_Local_Cache import Jira_Local_Cache
        from osbot_jira.api.graph.Jira_Graph import Jira_Graph

        jira_local_cache =  Jira_Local_Cache()
        cached_issues    = jira_local_cache.all_issues(index_by='Key')
        graph            = Jira_Graph()
        graph.issues     = cached_issues
        result           = graph.jira_get_issue_link_types_per_key_for_issues__indexed_by_to_key()

        issues_ids_in_deleted_node = []

        deleted_key = 'OBJECTIVE-88'

        for link_type, from_keys in result.get(deleted_key,{}).items():
            issues_ids_in_deleted_node.extend(from_keys)
            #print(link_type, from_keys)

        self.backup_jira.api_jira_rest.log_requests = True
        pprint(self.backup_jira.save_issues_with_ids(issues_ids_in_deleted_node))

        # finally rebuild cache
        jira_local_cache.cache_create_all_issues()

        # todo: add the rest of the login to process all issues_ids_in_deleted_node

    #todo fix logic belo
    def test_find_xref_gaps_in_issue_links__using_local_data(self):
        from osbot_jira.api.jira_server.local.Jira_Local_Cache import Jira_Local_Cache
        from osbot_jira.api.graph.Jira_Graph import Jira_Graph

        cached_issues = Jira_Local_Cache().all_issues(index_by='Key')
        graph = Jira_Graph()
        graph.issues = cached_issues
        link_types_per_key                   = graph.jira_get_link_types_per_key_for_issues()
        #link_types_per_key_indexed_by_to_key = graph.jira_get_issue_link_types_per_key_for_issues__indexed_by_to_key()

        for from_key, item in link_types_per_key.items():
            for link_type, to_keys in item.items():
                for to_key in to_keys:
                    if to_key not in link_types_per_key:
                        print(to_key)

    def test_find_local_issues_that_dont_exist_in_jira(self):
        result = self.backup_jira.find_local_issues_that_dont_exist_in_jira()
        pprint(result)

    def test_find_local_issues_links_that_dont_exist_in_jira(self):
        result = self.backup_jira.find_local_issues_links_that_dont_exist_in_jira()
        pprint(result)

    def test_update_cache_of_issues_with_missing_ids(self):
        result = self.backup_jira.update_cache_of_issues_with_missing_ids()
        pprint(result)

    def test_find_xref_gaps_in_issue_links__using_jira_data(self):
        from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
        api_jira_rest = API_Jira_Rest()
        api_jira_rest.log_requests = True
        issues_ids = api_jira_rest.issues_get_all_ids()
        pprint(len(issues_ids))

        print()
        return


        with Duration(print_result=True):
            issues_ids = api_jira_rest.search__return_keys(jql='', max_to_fetch=200)
            pprint(len(issues_ids))
            #pprint(issues_ids)

        with Duration(print_result=True):
            issues_ids = api_jira_rest.search(jql='', max_to_fetch=500)
            pprint(len(issues_ids))
        #all_issues_ids = api_jira_rest.iss
        # graph = Jira_Graph()
        # graph.issues = jira_rest_api.jira_get_issues()
        # link_types_per_key                   = graph.jira_get_link_types_per_key_for_issues()
        # link_types_per_key_indexed_by_to_key = graph.jira_get_issue_link_types_per_key_for_issues__indexed_by_to_key()
        #
        # for from_key, item in link_types_per_key.items():
        #     for link_type, to_keys in item.items():
        #         for to_key in to_keys:
        #             if to_key not in link_types_per_key:
        #                 print(to_key)