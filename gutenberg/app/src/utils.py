import os


def allowed_files(fname, allowed_list):
    return os.path.splitext(fname)[-1] in allowed_list