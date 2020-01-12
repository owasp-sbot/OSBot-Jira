import json
import gzip
import os

class Json:

    @staticmethod
    def load_json(path):
        if os.path.exists(path) is False:
            return None
        with open(path, "rt") as fp:
            data = fp.read()
            return json.loads(data)


    @staticmethod
    def load_json_and_delete(path):
        if os.path.exists(path) is False:
            return None
        with open(path, "rt") as fp:
            data = json.loads(fp.read())
        os.remove(path)
        return data

    @staticmethod
    def load_json_gz(path):
        if os.path.exists(path) is False:
            return None
        with gzip.open(path, "rt") as fp:
            data = fp.read()
            return json.loads(data)

    @staticmethod
    def save_json_gz(path, data):
        json_dump = json.dumps(data)
        with gzip.open(path, 'w') as fp:
            fp.write(json_dump.encode())
        return path

    @staticmethod
    def save_json_gz_pretty(path, data):
        json_dump = json.dumps(data,indent=2)
        with gzip.open(path, 'w') as fp:
            fp.write(json_dump.encode())
        return path

    @staticmethod
    def save_json(path, data):
        json_dump = json.dumps(data)
        with open(path, 'w') as fp:
            fp.write(json_dump)
        return path

    @staticmethod
    def save_json_pretty(path, data):
        json_dump = json.dumps(data,indent=2)
        with open(path, 'w') as fp:
            fp.write(json_dump)
        return path