from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Files import current_temp_folder, path_combine, create_folder, safe_file_name, file_not_exists, \
    file_exists, file_delete
from osbot_utils.utils.Json import json_save_file, json_load_file


class Local_Cache:

    DEFAULT_CACHES_NAME = "_cache_data"

    def __init__(self, cache_name, caches_name=None):
        self.caches_name = caches_name or Local_Cache.DEFAULT_CACHES_NAME
        self.cache_name = safe_file_name(cache_name)
        self._data      = None

    def add(self, key, value):
        self.data()[key] = value
        self.save()
        return self

    def cache_delete(self):
        return file_delete(self.path_cache_file())

    def cache_exists(self):
        return file_exists(self.path_cache_file())

    def create(self):
        if not self.cache_exists():
            self.save()
        return self

    def has_key(self, key):
        return key in self.keys()

    def save(self):
        data = self.data() or {}
        json_save_file(data, self.path_cache_file())
        return self

    def data(self):
        if self._data is None:
            self._data = json_load_file(self.path_cache_file())
        return self._data

    def get(self, key, default_value=None):
        return self.data().get(key, default_value)

    def name(self):
        return self.cache_name

    def keys(self):
        return self.data().keys()

    @cache_on_self
    def path_root_folder(self):
        path_root_folder = path_combine(current_temp_folder(), self.caches_name)
        create_folder(path_root_folder)                          # create if it doesn't exist
        return path_root_folder

    @cache_on_self
    def path_cache_file(self):
        return path_combine(self.path_root_folder(), f"{self.cache_name}.json")

    def setup(self):
        self.create()
        return self


    def remove(self, key):
        if key in self.keys():
            del self.data()[key]
            self.save()
            return True
        return False

    def values(self):
        return self.data().values()

    def __repr__(self):
        return f"Local_Cache: {self.cache_name}"

    # extra methods alias

    #add = set