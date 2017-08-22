import os
import importlib
import pkgutil
import inspect


def get_rstx_file_paths():
    """
    Get a list of files in this directory and all sub-directories.

    Returns
    -------
    list of (str, str)
        List of (file_dir, file_name) tuples where file_dir is the directory containing the
        file and file_name is the name of the file within that directory.
    """
    rstx_file_paths_list = []

    for file_dir, dirs, files in os.walk('.'):
        for file_name in files:
            if file_name[-5:] == '.rstx':
                rstx_file_paths_list.append((file_dir, file_name))

    return rstx_file_paths_list


def get_directives():
    """
    Get a list of custom directives that ship with sphinx_auto_embed.

    Returns
    -------
    list of func
        List of functions that process directives.
    """
    directives = []

    directives_module = importlib.import_module('sphinx_auto_embed.directives')
    directives_dir = os.path.dirname(directives_module.__file__)

    for file_name in os.listdir(directives_dir):
        if file_name[:9] == 'directive' and file_name[-3:] == '.py':
            module = importlib.import_module('sphinx_auto_embed.directives.%s' % file_name[:-3])

            for name, obj in inspect.getmembers(module):
                if name[:9] == 'Directive':
                    if inspect.isclass(obj) and hasattr(obj, 'NAME') and hasattr(obj, 'NUM_ARGS'):
                        directives.append(obj())

    return directives
