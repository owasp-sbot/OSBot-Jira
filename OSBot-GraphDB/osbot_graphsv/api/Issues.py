from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json


class Issues:

    def __init__(self,file_system):
        self.file_system = file_system


    # def all(self):
    #     data = []
    #     file_filter = Files.path_combine(self.file_system.folder_data, '**/*.json')
    #     for path in Files.find(file_filter):
    #         if self.filename_metadata not in path:          # don't load metadata file
    #             data.append(Json.load_json(path))
    #     return data