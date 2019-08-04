from pbx_gs_python_utils.utils.Files import Files

from osbot_graphsv.api.File_System import File_System
from osbot_graphsv.api.Indexes import Indexes


class Graph_SV:

    def __init__(self,folder_root):
        self.file_system = File_System(folder_root)
        self.indexes     = Indexes(self.file_system)


    def issue_add(self, issue_type, data):
        issue_type = self.file_system.issue_type(issue_type)
        return issue_type.issue_add(data)

