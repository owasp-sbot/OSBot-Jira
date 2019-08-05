from osbot_graphsv.api.Indexes_Build import Indexes_Build


class Indexes:
    def __init__(self, file_system):
        self.file_system = file_system
        self.indexes_build = Indexes_Build(self.file_system)

    def by_fields_and_values(self): return self.indexes_build.get__by_fields_and_values()
    def by_key              (self): return self.indexes_build.get__by_key()
    def by_values           (self): return self.indexes_build.get__by_values()
    def by_link_types       (self): return self.indexes_build.get__by_link_type()

    def rebuild(self):
        self.indexes_build.create_all()