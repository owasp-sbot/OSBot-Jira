from functools      import wraps
from unittest.mock  import patch

from osbot_jira.api.jira_server.cached.Jira_Cache import Jira_Cache


def patch_api_jira_rest(original_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_init = original_class.__init__

            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                self.api_jira_rest = Jira_Cache()

            with patch.object(original_class, '__init__', new_init):
                return func(*args, **kwargs)
        return wrapper
    return decorator