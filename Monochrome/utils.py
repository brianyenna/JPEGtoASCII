import os

def safe_mkdir(dir_path):
    '''
    Purpose: Checks whether the directory exists at dir_path. If it does not exist, then the directory is created.
    '''
    if os.path.isdir(dir_path):
        pass
    else:
        os.mkdir(dir_path)

def get_all_files(dir_path, file_ext=None):
    '''
    Purpose: Gets the full paths of all files in the directory specified.
    Inputs: dir_path: <String>
            file_ext: <String>
    Returns: A <List> of <Strings>. Each string is the full path of each file in the directory
    '''
    files_fullpath = []
    for file in os.listdir(dir_path):
        if file_ext:
            if file.endswith(file_ext):
                files_fullpath.append(os.path.join(dir_path, file))
        else:
            files_fullpath.append(os.path.join(dir_path, file))
    return files_fullpath