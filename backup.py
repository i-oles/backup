"""System modules"""
import os
import time
import sys
from os.path import expanduser
import shutil
import pathlib

FOLDER_NAME = 'your_folder_name'

# backup folder path on your desktop
BACKUP_DIR_PATH = os.path.join(expanduser("~"), 'Desktop', FOLDER_NAME)
# source folder path on your pendrive
SOURCE_DIR_PATH = os.path.join(pathlib.Path.cwd(), FOLDER_NAME)


def parse_all_src_paths():
    """getting all source file paths"""
    all_src_files = []
    for path, subdirs, files in os.walk(SOURCE_DIR_PATH): #pylint: disable=unused-variable
        for name in files:
            all_src_files.append(os.path.join(path, name))
    return all_src_files


def validate_path_and_backup_file(src_path, dst_path):
    """creating all necessary dirs from destination path and backup file"""
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copy(src_path, dst_path)


def main():
    """main function for backup"""
    if os.path.exists(BACKUP_DIR_PATH):
        for src_path in parse_all_src_paths():
            src_path_obj = pathlib.Path(src_path)
            dir_index = src_path_obj.parts.index(FOLDER_NAME)
            backup_path = pathlib.Path(os.path.join(expanduser("~"), 'Desktop', *src_path_obj.parts[dir_index:]))# pylint: disable=line-too-long

            if not os.path.exists(backup_path):
                validate_path_and_backup_file(src_path, backup_path)
                print(f'new file created: {backup_path}')
            else:
                src_file_date = time.ctime(os.path.getmtime(src_path))
                backup_file_date = time.ctime(os.path.getmtime(backup_path))
                if src_file_date > backup_file_date:
                    validate_path_and_backup_file(src_path, backup_path)
                    print(f'updated file: {backup_path}')
    else:
        shutil.copytree(SOURCE_DIR_PATH, BACKUP_DIR_PATH)


if __name__ == '__main__':
    sys.exit(main())
