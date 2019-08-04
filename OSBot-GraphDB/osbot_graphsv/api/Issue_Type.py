from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json


class Issue_Type:
    def __init__(self,file_system, name):
        self.file_system       = file_system
        self.name              = name
        self.filename_metadata = 'metadata.json'

    def issue_add(self,data):
        if self.exists() is False:
            self.create()
        metadata   = self.metadata()
        issue_key   = "{0}-{1}".format(metadata.get('Key Id'),metadata.get('Next Key'))
        issue_path = self.path_issue(issue_key)
        metadata['Next Key'] += 1
        data['Key'       ] = issue_key
        data['Issue Type'] = self.name
        Json.save_json_pretty(issue_path, data)
        Json.save_json_pretty(self.path_metadata(), metadata)
        if Files.exists(issue_path):
            return { 'status': 'ok', 'data': 'Issue added ok', 'issue_key': issue_key}
        return { 'status': 'error', 'data': 'Issue not saved ok'}

    def issue_get(self, issue_key):
        issue_path = self.path_issue(issue_key)
        if Files.exists(issue_path):
            return Json.load_json(issue_path)

    def create(self):
        if self.exists() is True:
            return {'status': 'error', 'data':'issue type already existed: {0}'.format(self.name)}
        Files.folder_create(self.path())
        if self.create_metadata():
            return {'status': 'ok', 'data': 'issue type created: {0}'.format(self.name)}
        return {'status': 'error', 'data': 'issue type metadata file not created: {0}'.format(self.name)}

    def create_metadata(self):
        default_metadata = {  'Issue Type': self.name,
                              'Key Id'    : self.file_system.safe_string(self.name),
                              'Next Key'  : 1
                           }
        path_metadata    = self.path_metadata()
        Json.save_json_pretty(path_metadata, default_metadata)
        return Files.exists(path_metadata)

    def delete(self):
        """
        Delete Issue Type and all issues (be careful since this will delete all issues in this issue type)
        :return: Bool
        """
        if self.exists():
            return Files.folder_delete_all(self.path()) 
        return False

    def exists(self):
        return Files.folder_exists(self.path())

    def metadata(self):
        if self.exists():
            return Json.load_json(self.path_metadata())

    def path(self):
        return Files.path_combine(self.file_system.folder_data,self.file_system.safe_string(self.name))

    def path_metadata(self):
        return Files.path_combine(self.path(),self.filename_metadata)

    def path_issue(self,issue_key):
        file_name = "{0}.json".format(issue_key)
        return Files.path_combine(self.path(),file_name)

    def __str__(self):
        return 'Issue Type: {0}'.format(self.name)

    def __repr__(self):
        return self.__str__()