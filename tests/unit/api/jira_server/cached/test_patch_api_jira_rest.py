from unittest import TestCase
from unittest.mock import patch

from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set, random_text, obj_info

from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from osbot_jira.api.jira_server.cached.Jira_Cache import Jira_Cache
from osbot_jira.api.jira_server.cached.patch_api_jira_rest import patch_api_jira_rest


class With_Patch:
    def __init__(self):
        self.api_jira_rest = API_Jira_Rest()

class Without_Patch:
    def __init__(self):
        self.api_jira_rest = API_Jira_Rest()

class One_Degree_Of_Separation:
    def __init__(self):
        self.with_patch    = With_Patch()
        self.without_patch = Without_Patch()


class test_patch_api_jira_rest(TestCase):

    @patch_api_jira_rest(With_Patch)
    def setUp(self) -> None:
        self.issue_id          = 'RISK-333'
        self.with_patch        = With_Patch()
        self.without_patch     = Without_Patch()
        self.one_degree_of_sep = One_Degree_Of_Separation()

    def tearDown(self) -> None:
        jira_caches_1 : Jira_Cache = self.with_patch.api_jira_rest
        jira_caches_2 : Jira_Cache = self.one_degree_of_sep.with_patch.api_jira_rest

        assert jira_caches_1.caches.delete() is True
        assert jira_caches_2.caches.delete() is True



    def test__one_degree_of_sep(self):
        assert type(self.one_degree_of_sep.with_patch   .api_jira_rest) == Jira_Cache
        assert type(self.one_degree_of_sep.without_patch.api_jira_rest) == API_Jira_Rest
        jira_cache: Jira_Cache = self.one_degree_of_sep.with_patch.api_jira_rest

    def test_with_patch(self):
        assert type(self.with_patch.api_jira_rest)     == Jira_Cache
        assert self.with_patch.api_jira_rest.issues()  == {}
        new_cached_issue = self.with_patch.api_jira_rest.issue_create('risk', 'risk', 'summary')
        new_issue_id     = new_cached_issue.get('Key')

        assert list_set(new_cached_issue)          == ['Description', 'Issue Type', 'Key', 'Project', 'Summary']
        assert new_cached_issue.get('Issue Type' ) == 'risk'
        assert new_cached_issue.get('Project'    ) == 'risk'
        assert new_cached_issue.get('Description').startswith('description_')
        assert new_cached_issue.get('Summary'    ).startswith('summary_'    )

        with patch("osbot_jira.api.jira_server.API_Jira_Rest.API_Jira_Rest.issue") as mocked_issue:
            with Duration(print_result=False) as duration:
                assert self.with_patch.api_jira_rest.issue(new_issue_id).get('Key') == new_issue_id
        assert duration.seconds() < 0.1
        assert mocked_issue.call_count == 0

    def test_without_patch(self):
        return_value = random_text('jira_id')
        assert type(self.without_patch.api_jira_rest    ) == API_Jira_Rest
        with patch("osbot_jira.api.jira_server.API_Jira_Rest.API_Jira_Rest.issue", return_value={'Key': return_value}) as mocked_issue:
            assert self.without_patch.api_jira_rest.issue(self.issue_id).get('Key') == return_value
            assert mocked_issue.call_count == 1