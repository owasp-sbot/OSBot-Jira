from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from osbot_utils.decorators.Method_Wrappers   import cache
from osbot_utils.utils.Files                  import folder_create, save_bytes_as_file, file_exists, file_not_exists


class Jira_Icons:
    def __init__(self):
        self.jira_rest_api = API_Jira_Rest()
        self.icons_folder_name = 'jira_icons'

    def icon_local(self,name:str):
        name = name.upper()
        icon_path = f'{self.icons_folder()}/{name}.png'
        if self.save_icon_locally(name, icon_path):
            return icon_path

    def icon_local_for_key(self, issue_key):
        if '-' in issue_key:
            name = issue_key.split('-')[0]
            return self.icon_local(name)

    def all_icons_local(self):
        icons_local = []
        for icon_name in list(self.icons_urls().keys()):
            icons_local.append(self.icon_local(icon_name))
        return icons_local

    def icon_url(self, key: str):
        return self.icons_urls().get(key.upper())

    @cache
    def icons_urls(self):
        return self.jira_rest_api.projects_icons()

    def icons_folder(self):
        return folder_create(f'/tmp/{self.icons_folder_name}')

    def save_icon_locally(self, name, icon_path, force_reload=False):
        if file_not_exists(icon_path) or force_reload:
            icon_url = self.icon_url(name)
            if icon_url:
                icon_bytes = self.jira_rest_api.request_get(icon_url)
                save_bytes_as_file(icon_bytes, icon_path)
        return file_exists(icon_path)