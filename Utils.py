import os


def __mkdir_recursive__(path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        __mkdir_recursive__(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)

def mkdirs(path):
    __mkdir_recursive__(path)