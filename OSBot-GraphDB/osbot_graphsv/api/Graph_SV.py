from pbx_gs_python_utils.utils.Files import Files

from osbot_graphsv.api.File_System import File_System


class Graph_SV:

    def __init__(self,folder_root):
        self.file_system = File_System(folder_root)


    def issue_add(self, issue_type, data):
        issue_type = self.file_system.issue_type(issue_type)
        return issue_type.issue_add(data)

