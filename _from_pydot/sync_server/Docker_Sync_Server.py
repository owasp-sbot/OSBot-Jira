import shutil
from os.path import abspath, join

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from utils.Process import Process


class Docker_Sync_Server:
    def __init__(self):
        self.path_docker_folder = abspath(join(__file__               ,'../../../docker/sync-server'))
        self.path_docker_file   = abspath(join(self.path_docker_folder, 'Dockerfile'                ))

    def dockerfile(self):
        return Files.contents(self.path_docker_file)

    def build_image(self, no_cache = True, show_log = False):
        self.build_step__zip_src_folder()
        return self.build_step__create_image(no_cache, show_log)

    def build_step__create_image(self, no_cache, show_log):
        params = ['build']
        if no_cache: params.append('--no-cache')
        params += [ '-t', 'sync-server', '.']
        Dev.pprint(params)
        result = Process.run('docker', params, cwd=self.path_docker_folder)
        if show_log:
            Dev.pprint(result['stderr'])
            Dev.pprint(result['stdout'])
        return result

    def build_step__zip_src_folder(self):
        zip_file     = Files.path_combine(self.path_docker_folder,'src')
        src_folder    = Files.path_combine(self.path_docker_folder, '../../src')
        return shutil.make_archive(zip_file, "gztar", src_folder)


    def exec_in_image(self, cmd, cmd_params=[]):
        params = ['run', '--rm', 'sync-server', cmd] + cmd_params
        result = Process.run('docker', params, cwd=self.path_docker_folder)
        return result#['stdout'].strip()                                      # assumes that command executes ok
