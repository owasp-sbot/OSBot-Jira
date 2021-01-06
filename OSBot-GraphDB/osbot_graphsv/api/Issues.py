from osbot_utils.utils.Files import Files
from osbot_utils.utils.Json import Json


class Issues:

    def __init__(self,file_system):
        self.file_system = file_system
        self.filename_metadata = 'metadata.json'

    def by_issue_type(self,issue_type_name, indexed_by=None):
        data = []
        file_filter = "{0}/{1}/{2}".format(self.file_system.folder_data, issue_type_name ,'*.json')
        for path in Files.find(file_filter):
            if self.filename_metadata not in path:          # don't load metadata file
                data.append(Json.load_file(path))
        if indexed_by is None:
            return data
        indexed_data = {}
        for item in data:
            key   = item.get('Key')
            index = item.get(indexed_by)
            if index:
                if indexed_data.get(index) is None: indexed_data[index] = {}
                indexed_data[index][key] = item
        return indexed_data

    def accounts             (self, indexed_by='Summary'): return self.by_issue_type('Account'             , indexed_by)
    def applications         (self, indexed_by='Summary'): return self.by_issue_type('Application'         , indexed_by)
    def capabilities         (self, indexed_by='Summary'): return self.by_issue_type('Capability'          , indexed_by)
    def business_assets      (self, indexed_by='Summary'): return self.by_issue_type('Business_Asset'      , indexed_by)
    def business_units       (self, indexed_by='Summary'): return self.by_issue_type('Business_Unit'       , indexed_by)
    def detections           (self, indexed_by='Summary'): return self.by_issue_type('Detection'           , indexed_by)
    def devices              (self, indexed_by='Summary'): return self.by_issue_type('Device'              , indexed_by)
    def functions            (self, indexed_by='Summary'): return self.by_issue_type('Function'            , indexed_by)
    def incident_facts       (self, indexed_by='Summary'): return self.by_issue_type('Incident_Fact'       , indexed_by)
    def incident_tasks       (self, indexed_by='Summary'): return self.by_issue_type('Incident_Task'       , indexed_by)
    def incidents            (self, indexed_by='Summary'): return self.by_issue_type('Incident'            , indexed_by)
    def investigation_threads(self, indexed_by='Summary'): return self.by_issue_type('Investigation_Thread', indexed_by)
    def teams                (self, indexed_by='Summary'): return self.by_issue_type('Team'                , indexed_by)
    def risks                (self, indexed_by='Summary'): return self.by_issue_type('Risk'                , indexed_by)
    def roles                (self, indexed_by='Summary'): return self.by_issue_type('Role'                , indexed_by)
    def persons              (self, indexed_by='Summary'): return self.by_issue_type('Person'              , indexed_by)
    def pillars              (self, indexed_by='Summary'): return self.by_issue_type('Pillar'              , indexed_by)
    def security_impacts     (self, indexed_by='Summary'): return self.by_issue_type('Security_Impact'     , indexed_by)
    def timeline_facts       (self, indexed_by='Summary'): return self.by_issue_type('Timeline_Fact'       , indexed_by)
    def vulnerabilities      (self, indexed_by='Summary'): return self.by_issue_type('Vulnerability'       , indexed_by)





    # def all(self):
    #     data = []
    #     file_filter = Files.path_combine(self.file_system.folder_data, '**/*.json')
    #     for path in Files.find(file_filter):
    #         if self.filename_metadata not in path:          # don't load metadata file
    #             data.append(Json.load_file(path))
    #     return data