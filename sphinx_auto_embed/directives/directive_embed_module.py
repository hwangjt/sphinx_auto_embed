import os, sys
import inspect
import importlib
import contextlib
try:
    from StringIO import StringIO
except:
    from io import StringIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sphinx_auto_embed.directive import Directive


class DirectiveEmbedModule(Directive):
    """
    Directive for embedding all the code from a module.

    The 3 arguments are the module name, class name, and method name.
    """

    NAME = 'embed-module'
    NUM_ARGS = 1

    def get_method_lines(self, args):
        py_file_path = args

        py_module = importlib.import_module(py_file_path)

        method_lines = inspect.getsource(py_module).split('\n')

        return method_lines

    def run(self, file_dir, file_name, embed_num_indent, args):
        py_file_path = args[0]

        py_module = importlib.import_module(py_file_path)

        method_lines = inspect.getsource(py_module).split('\n')

        lines = []
        lines.append(' ' * embed_num_indent + '.. code-block:: python\n')
        lines.append('\n')
        lines.extend([
            ' ' * embed_num_indent + ' ' * 2 + method_line + '\n'
            for method_line in method_lines
        ])
        return lines
