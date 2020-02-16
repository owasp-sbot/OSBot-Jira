from pbx_gs_python_utils.utils import Json
from pbx_gs_python_utils.utils.Files import *

def clear_local_cache_files(function):
    def wrapper(*args):
        params = list(args)
        self_obj = params.pop(0)
        class_name = self_obj.__class__.__name__
        path_pattern = '/tmp/local_cache_{0}*.*'.format(class_name)
        for path in Files.find(path_pattern):
            print('[clear_local_cache_files] deleting file: {0}'.format(path))
            os.remove(path)
        return function(*args)
    return wrapper


def get_local_cache_key(self_obj, function_obj, params):
    class_name      = self_obj.__class__.__name__
    if function_obj.__class__.__name__ == 'str':
        function_name = function_obj
    else:
        function_name = function_obj.__name__
    return '{0}_{1}_{2}'.format(class_name, function_name, '_'.join(str(x) for x in params));

def get_local_cache_path(self_obj, function_obj, params):
    cache_key     = get_local_cache_key(self_obj, function_obj, params)
    return '/tmp/local_cache_{0}.gz'.format(cache_key)

def get_local_cache_data(cache_path):
    return Json.load_json_gz(cache_path)

def save_local_cache_data(cache_path, data):
    Json.save_json_gz(cache_path,data)
    return data

def save_result_to_local_cache(function):
    def wrapper(*args):
        params     = list(args)
        self_obj   = params.pop(0)
        cache_path = get_local_cache_path(self_obj, function, params)
        return save_local_cache_data(cache_path, function(*args))
    return wrapper

def use_local_cache_if_available(function):
    def wrapper(*args):
        params        = list(args)
        self_obj      = params.pop(0)
        cache_path    = get_local_cache_path(self_obj, function, params)
        data          = get_local_cache_data(cache_path)
        if data:
            return data
        return save_local_cache_data(cache_path,function(*args))

    return wrapper
