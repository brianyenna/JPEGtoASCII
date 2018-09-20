import os
import glob
import functools
import threading
import sys
import time
import functools
import itertools

def safe_mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_all_files(dir_path, file_ext):
    '''
    Purpose: If file_ext is not None, returns in a [LIST] all files in the directory dir_path that have                 file_ext. Else, returns in a [LIST] all files in the directory dir_path
    Input: dir_path [STRING]: directory to be examined
           file_ext [STRING]: a dot must be placed in the string (e.g. '.jpg')
    '''
    if file_ext:
        if dir_path[-1] in ['/', '\\']:
            return glob.glob(dir_path+'*{}'.format(file_ext))
        else: 
            return glob.glob(dir_path+'/*{}'.format(file_ext))
    else: 
        return os.listdir(dir_path)

def animate(func):
    @functools.wraps(func)
    def animated_func(*args, **kwargs):        
        try: 
            loading_item_name = ' ' + kwargs['loading_name']
            del kwargs['loading_name']
        except:
            loading_item_name = ' '

        process_done = False
        def loading_animation():
            for c in itertools.cycle(['|', '/', '-', '\\']):
                if process_done: 
                    break
                sys.stdout.write('\rLoading{} {}'.format(loading_item_name, c))
                sys.stdout.flush()
                time.sleep(0.1)
        
        t = threading.Thread(target=loading_animation)
        t.setDaemon(True) #This ensures that should the main thread terminate, the animation() thread will terminate as well
        t.start()

        func(*args, **kwargs)
        process_done = True
        print('\rLoading Done!' + ' '*len(loading_item_name))
    return animated_func