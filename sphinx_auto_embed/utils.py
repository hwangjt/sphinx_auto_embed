import os
import sys
import importlib
import pkgutil
import inspect


def read_embedrc():
    # Keep going up a directory until we find '.embedrc' or go all the way to the top
    orig_cwd = os.getcwd()
    cwd = os.getcwd()
    while not os.path.isfile(cwd + '/.embedrc'):
        os.chdir("..")
        new_cwd = os.getcwd()
        if new_cwd == cwd:
            break
        else:
            cwd = new_cwd
    embedrc_dir = cwd

    custom_directives_dir = None

    # If there is an '.embedrc':
    if os.path.isfile(embedrc_dir + '/.embedrc'):
        # Load the file
        with open(embedrc_dir + '/.embedrc', 'r') as f:
            lines = f.readlines()

        # Read in custom_directives_dir
        for iline, line in enumerate(lines):
            stripped_line = line.replace(' ', '')
            if stripped_line[:22] == 'custom_directives_dir=':
                custom_directives_dir = embedrc_dir + '/' + stripped_line[22:]

    return custom_directives_dir


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


def get_directives(custom_directives_dir):
    """
    Get a list of custom directives that ship with sphinx_auto_embed.

    Parameters
    ----------
    custom_directives_dir : str
        Absolute path to the directory containing custom directives for the current project.

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

    if custom_directives_dir is not None:
        for file_dir, dirs, files in os.walk(custom_directives_dir):
            for file_name in files:
                if file_name[:9] == 'directive' and file_name[-3:] == '.py':
                    sys.path.append(file_dir)
                    module = importlib.import_module(file_name[:-3])

                    for name, obj in inspect.getmembers(module):
                        if name[:9] == 'Directive':
                            if inspect.isclass(obj) and hasattr(obj, 'NAME') and hasattr(obj, 'NUM_ARGS'):
                                directives.append(obj())

    return directives
