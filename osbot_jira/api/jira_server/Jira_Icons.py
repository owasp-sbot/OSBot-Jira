from osbot_utils.utils.Files                  import folder_create, file_exists, file_not_exists
from osbot_utils.utils.Http import GET_bytes_to_file


class Jira_Icons:
    def __init__(self):
        #self.jira_rest_api = API_Jira_Rest()
        self.icons_folder_name = 'jira_icons'
        self.icons_github_folder = 'https://github.com/filetrust/Squads-And-Maps/raw/master/jira/icons'

    def icon_local(self,name:str):
        name = name.upper()
        icon_path = f'{self.icons_folder()}/{name}.png'
        if self.save_icon_locally(name, icon_path):
            return icon_path

    def icon_local_for_key(self, issue_key):
        if '-' in issue_key:
            name = issue_key.split('-')[0]
            return self.icon_local(name)

    def all_icons_local(self):          # todo find a way to get this from GitHub
        icons_local = []
        from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
        icons_names = API_Jira_Rest().projects_icons().keys()
        for icon_name in icons_names:
            icons_local.append(self.icon_local(icon_name))
        return icons_local

    # def icon_url(self, key: str):
    #     return self.icons_urls().get(key.upper())
    #
    # @cache
    # def icons_urls(self):
    #     return self.jira_rest_api.projects_icons()

    # def save_icon_locally(self, name, icon_path, force_reload=False):     # this gets icons from Jira (which requires Auth)
    #     if file_not_exists(icon_path) or force_reload:
    #         icon_url = self.icon_url(name)
    #         if icon_url:
    #             icon_bytes = self.jira_rest_api.request_get(icon_url)
    #             save_bytes_as_file(icon_bytes, icon_path)
    #     return file_exists(icon_path)

    def icons_folder(self):
        return folder_create(f'/tmp/{self.icons_folder_name}')

    def github_url(self, name):
        return f'{self.icons_github_folder}/{name.upper()}.png'

    def save_icon_locally(self, name, icon_path, force_reload=False):
        if file_not_exists(icon_path) or force_reload:
            icon_url = self.github_url(name)
            GET_bytes_to_file(icon_url, icon_path)
        return file_exists(icon_path)