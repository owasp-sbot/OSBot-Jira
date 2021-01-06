import re

from osbot_utils.utils.Files import Files

from osbot_graphsv.api.Issue_Type import Issue_Type


class File_System:

    def __init__(self, folder_root):
        self.folder_root       = folder_root
        self.folder_data       = Files.path_combine(self.folder_root, 'data')
        self.folder_indexes    = Files.path_combine(self.folder_root, 'indexes')


    def safe_string(self,value,join_char='_'):
        return join_char.join(re.findall("[.a-zA-Z0-9_-]+", value))


    def issue_type(self,name):
        issue_type = Issue_Type(self,name)
        if issue_type.exists():
            return issue_type
        if issue_type.create().get('status') == 'ok':
            return issue_type






