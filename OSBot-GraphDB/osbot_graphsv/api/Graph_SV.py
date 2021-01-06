from osbot_graphsv.api.File_System import File_System
from osbot_graphsv.api.Indexes import Indexes
from osbot_graphsv.api.Issues import Issues
from osbot_graphsv.api.Links import Links


class Graph_SV:

    def __init__(self,folder_root):
        self.file_system = File_System(folder_root)
        self.indexes     = Indexes(self.file_system)
        self.issues      = Issues(self.file_system)
        self.links       = Links(self.file_system)



    def link_add(self, from_key, link_type, to_key):
        return self.links.add_pair(from_key, link_type, to_key)

    def issue_add(self, issue_type_name, data):
        issue_type = self.file_system.issue_type(issue_type_name)
        return issue_type.issue_add(data)

