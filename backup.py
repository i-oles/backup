import os
import time
from os.path import expanduser, getmtime
import shutil
import glob
import pathlib

folder_name = 'your_folder_name'

# backup folder path on your desktop
backup_dir_path = os.path.join(expanduser("~"), 'Desktop', folder_name)
# source folder path on your pendrive
source_dir_path = os.path.join(pathlib.Path.cwd(), folder_name)

all_source_files = []

if os.path.exists(backup_dir_path):
    for path, subdirs, files in os.walk(source_dir_path):
        for name in files:
            all_source_files.append(os.path.join(path, name))

    for source_file in all_source_files:
        source_path = pathlib.Path(source_file)
        index = source_path.parts.index(folder_name)
        backup_file = pathlib.Path(os.path.join(expanduser("~"), 'Desktop', *source_path.parts[index:]))

        if not os.path.exists(backup_file):
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            shutil.copy(source_file, backup_file)
            print(f'new file created: {source_file}')
        else:
            source_file_date = time.ctime(os.path.getmtime(source_file))
            backup_file_date = time.ctime(os.path.getmtime(backup_file))
            if source_file_date > backup_file_date:
                os.makedirs(os.path.dirname(backup_file), exist_ok=True)
                shutil.copy(source_file, backup_file)
                print(f'updated file: {source_file}')
else:
    shutil.copytree(source_dir_path, backup_dir_path)