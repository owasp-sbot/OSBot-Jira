from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json


class Links:
    def __init__(self, file_system):
        self.file_system = file_system
        self.link_pairs = {
            'has role'   : 'is role of'   , 'is role of'    : 'has role'  ,
            'reports to' : 'is manager of', 'is manager of' :'reports to'
        }

    def all(self):
        path = self.path_links()
        if Files.exists(path):
            return Json.load_json(path)
        return []

    def add(self,from_key, link_type, to_key):
        link = [from_key.strip(), link_type.strip(), to_key.strip()]
        links = self.all()
        if link in links:
            return {'status': 'error', 'data' : 'link already existed: {0}'.format(link)}
        links.append(link)
        self.save(links)
        return {'status': 'ok', 'data': 'link added: {0}'.format(link)}

    def add_pair(self, from_key, link_type, to_key):
        link_pair = self.link_pairs.get(link_type.strip())
        if link_pair is None: link_pair = "(opposite of) {0}".format(link_type)
        self.add(from_key,link_type, to_key)
        self.add(to_key, link_pair, from_key)
        return self

    def delete(self,from_key, link_type, to_key):
        link = [from_key, link_type, to_key]
        links = self.all()
        if link not in links:
            return {'status': 'error', 'data' : 'link not found: {0}'.format(link)}
        links.remove(link)
        self.save(links)
        return {'status': 'ok', 'data': 'link deleted: {0}'.format(link)}

    def save(self,links):
        path = self.path_links()
        Json.save_json_pretty(path, links)
        return self
    def path_links(self):
        return Files.path_combine(self.file_system.folder_data,'links.json')