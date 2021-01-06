from osbot_utils.utils.Files import Files
from osbot_utils.utils.Json import Json

from osbot_graphsv.api.Issues import Issues
from osbot_graphsv.api.Links import Links


class Indexes_Build:
    def __init__(self, file_system):
        self.file_system       = file_system
        self.folder_indexes    = self.file_system.folder_indexes
        self.issues            = Issues(self.file_system)
        self.links             = Links(self.file_system)
        self.filename_metadata = 'metadata.json'

    def create_all(self):
        self.create__by_key()
        self.create__by_fields_and_values()
        self.create__by_values()
        self.create__by_link_type()

    def create__by_key(self):
        all_data   = {}
        file_filter = Files.path_combine(self.file_system.folder_data, '**/*.json')
        for path in Files.find(file_filter):
            if self.filename_metadata not in path:  # don't load metadata file
                data = Json.load_file(path)
                key  = data.get('Key')
                all_data[key] = { 'path': path.replace(self.file_system.folder_data,'')[1:],
                                  'links': {}                                              ,
                                  'data': data                                             ,}

        for link in self.links.all():
            from_key  = link[0]
            link_type = link[1]
            to_key    = link[2]
            issue = all_data.get(from_key)
            if issue:
                links = issue.get('links')
                if links.get(link_type) is None: links[link_type]=[]
                links[link_type].append(to_key)


        Json.save_file_pretty(self.path__by_key(),all_data)
        return all_data

    def create__by_fields_and_values(self):
        issues = self.get__by_key()
        data   = {}
        for key, issue in issues.items():
            for field, value in issue.get('data').items():
                if field in ['Issue Type', 'Key']:
                    continue
                if data.get(field)        is None: data[field]        = {}
                if data[field].get(value) is None: data[field][value] = []
                data[field][value].append(key)
        Json.save_file_pretty(self.path__by_fields_and_values(), data)
        return data

    def create__by_values(self):
        issues = self.get__by_key()
        data   = {}
        for key,issue in issues.items():
            for field, value in issue.get('data').items():
                if field in ['Issue Type', 'Key']:
                    continue
                if data.get(value) is None: data[value] = []
                data[value].append((key , field ) )
        Json.save_file_pretty(self.path__by_values(), data)
        return data

    def create__by_link_type(self):
        data = {}
        for link in self.links.all():
            (from_key, link_type, to_key) = link
            if data.get(link_type)           is None: data[link_type] = {}
            if data[link_type].get(from_key) is None: data[link_type][from_key] = []

            data[link_type][from_key].append(to_key)
            Json.save_file_pretty(self.path__by_link_type(), data)
        return data

    def get_data_for(self,file_type):
        return Json.load_file(self.path_for(file_type))

    def path_for(self, file_type):
        return Files.path_combine(self.folder_indexes,file_type + '.json')

    def get__by_fields_and_values(self): return self.get_data_for('by_fields_and_values')
    def get__by_key              (self): return self.get_data_for('by_key')
    def get__by_values           (self): return self.get_data_for('by_values')
    def get__by_link_type           (self): return self.get_data_for('by_link_type')

    def path__by_fields_and_values(self): return self.path_for('by_fields_and_values')
    def path__by_key              (self): return self.path_for('by_key')
    def path__by_values           (self): return self.path_for('by_values')
    def path__by_link_type        (self): return self.path_for('by_link_type')


    # def get_issues(self, issues_ids):
    #     issues = {}
    #     return issues