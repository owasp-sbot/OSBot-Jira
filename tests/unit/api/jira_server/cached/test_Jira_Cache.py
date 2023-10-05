from unittest import TestCase

from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import parent_folder, file_name
from osbot_utils.utils.Json import json_load_file
from osbot_utils.utils.Misc import random_text, lower, list_set, upper

from osbot_jira.api.jira_server.cached.Jira_Cache import Jira_Cache


class test_Jira_Cache(TestCase):
    caches_name = random_text("test_jira_cache")
    jira_cache  : Jira_Cache

    @classmethod
    def setUpClass(cls) -> None:
        cls.jira_cache = Jira_Cache(caches_name=cls.caches_name)
        cls.cached_issues = cls.jira_cache.cached_issues
        cls.cached_jql    = cls.jira_cache.cached_jql

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.jira_cache.caches.delete() is True

    def setUp(self):
        self.issue_id  = 'RISK-333'
        self.issue_ids = ['', 'INCIDENT-299', self.issue_id]                        # todo: need to find a test jira server that has valid data

    def test__init__(self):
        assert self.cached_issues.name()          == "cached_issues"
        assert self.cached_jql   .name()          == "cached_jql"
        assert self.cached_issues.cache_exists()  is True
        assert self.cached_jql   .cache_exists()  is True
        assert self.jira_cache.caches.caches_name == self.caches_name

    def test_issue(self):
        with Duration(print_result=False) as duration_fetch:
            issue_fetch = self.jira_cache.issue(self.issue_id)
        with Duration(print_result=False) as duration_cache:
            issue_cache = self.jira_cache.issue(self.issue_id)

        assert issue_fetch.get('Description').startswith('description_')
        assert issue_fetch.get('Summary'    ).startswith('summary_'    )
        assert issue_fetch.get('Creator'    ).startswith('creator_'    )

        assert issue_fetch == issue_cache
        assert duration_fetch.seconds() > 0.5
        assert duration_cache.seconds() < 0.1

        cached_issues = self.jira_cache.cached_issues
        file_path     = cached_issues.path_cache_file()
        file_json     = json_load_file(file_path)
        assert file_json.get(self.issue_id) == issue_cache
        assert self.jira_cache.issue_delete(self.issue_id) is True

    def test_issue_create(self):
        new_issue_data =  {"project"    : "project"                     ,
                           "summary"    : "summary"                     ,
                           "description": "description"                 ,
                           "issue_type" : "issue_type"                  ,
                           "extra_fields": {"Extra_1": "extra_1_value"  ,
                                            "Extra_2": "extra_2_value" }}

        issue = self.jira_cache.issue_create(**new_issue_data)
        key   = issue.get('Key')
        assert self.jira_cache.issue (key) == issue
        assert self.jira_cache.issue_exists(key) is True
        assert self.jira_cache.issue_delete(key) is True
        assert self.jira_cache.issue_exists(key) is False
        assert issue.get('Description').startswith('description_')
        assert issue.get('Extra_1'    ).startswith('extra_1_'    )
        assert issue.get('Extra_2'    ).startswith('extra_2_'    )
        assert issue.get('Summary'    ).startswith('summary_'    )
        assert issue.get('Key'        ).startswith(upper(new_issue_data.get('project')))
        assert issue.get('Issue Type' ) == new_issue_data.get('issue_type'             )
        assert issue.get('Project'    ) == new_issue_data.get('project'                )


    def test_issue_update_fields(self):
        fields       = {"Summary": random_text("summary_edited"), "Updated_Field" : random_text('updated_field') }
        issue_update = self.jira_cache.issue_update_fields(self.issue_id, fields)

        assert issue_update.get('Summary'      ).startswith("summary_edited")
        assert issue_update.get('Updated_Field').startswith("updated_field" )  # note: this is actually a potential bug, since this behaviour doesn't exist in the main Jira Server (i.e. we can't add new fields like this)
        assert issue_update == self.jira_cache.issue(self.issue_id)

        assert self.jira_cache.issue_delete(self.issue_id)
    def test_search(self):
        jql = 'KEY=RISK-333 or KEY=RISK-313'
        self.jira_cache.jql_remove(jql)

        assert self.jira_cache.jqls() == {}

        with Duration(print_result=False) as duration_no_cache:
            issues = self.jira_cache.search(jql=jql, max_to_fetch=10)
            assert len(issues) == 2
            for issue in issues:
                assert issue.get('Summary').startswith('summary_')
                assert issue.get('Creator').startswith('creator_')

            cached_jqls = self.jira_cache.cached_jql.data()
            assert list_set(cached_jqls) == [jql]
            assert cached_jqls.get(jql)  == issues

        with Duration(print_result=False) as duration_cache:
            self.jira_cache.search(jql=jql, max_to_fetch=1000)

        assert duration_no_cache.seconds() > 0.5
        assert duration_cache   .seconds() < 0.1

        assert self.jira_cache.cached_jql.get   (jql) is not None
        assert self.jira_cache.cached_jql.remove(jql) is True
        assert self.jira_cache.cached_jql.get   (jql) is None

    def test_randomize(self):
        # handle errors
        assert self.jira_cache.randomize(None) == {}
        assert self.jira_cache.randomize(42  ) == {}
        assert self.jira_cache.randomize('42') == {}

        def assert_recursive_randomization(data, preserved_fields):
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        assert_recursive_randomization(value, preserved_fields)
                    else:
                        if key not in preserved_fields:
                            assert value.startswith(lower(key))

        assert self.jira_cache.issues() == {}

        for issue_id in self.issue_ids:                                       # handle real data
            real_data        = self.jira_cache.issue(issue_id=issue_id)
            issue            = self.jira_cache.randomize(real_data)
            preserved_fields = self.jira_cache.FIELDS_TO_PRESERVE
            assert_recursive_randomization(issue, preserved_fields)

        assert list_set(self.jira_cache.issues()) ==  self.issue_ids

    def test_cached_issues__path_cache_file(self):
        cached_issues = self.jira_cache.cached_issues
        path_cached_issues = cached_issues.path_cache_file()
        assert parent_folder(path_cached_issues) == cached_issues.path_root_folder()
        assert file_name    (path_cached_issues) == cached_issues.cache_name + '.json'

    def test_cached_issues__path_cache_jlq(self):
        cached_jql      = self.jira_cache.cached_jql
        path_cached_jql = cached_jql.path_cache_file()
        assert parent_folder(path_cached_jql) == cached_jql.path_root_folder()
        assert file_name    (path_cached_jql) == cached_jql.cache_name + '.json'

    def test__non_randomised_results(self):
        temp_jira_cache = Jira_Cache()
        temp_jira_cache.randomise_issue = False
        assert temp_jira_cache.caches.exists() is True

        raw_issue = temp_jira_cache.issue(self.issue_id)
        assert raw_issue.get('Summary').startswith('summary_') is False
        assert raw_issue.get('Creator').startswith('creator_') is False

        raw_issues =  temp_jira_cache.search(f"Key={self.issue_id}")
        for raw_issue in raw_issues:
            assert raw_issue.get('Summary').startswith('summary_') is False
            assert raw_issue.get('Creator').startswith('creator_') is False

        assert temp_jira_cache.caches.delete() is True
        assert temp_jira_cache.caches.exists() is False