import os

from osbot_utils.utils.Files import folder_exists


def folder_delete(target_folder):
    if folder_exists(target_folder):
        try:
            os.rmdir(target_folder)
            return True
        except OSError:
            pass
    return False
