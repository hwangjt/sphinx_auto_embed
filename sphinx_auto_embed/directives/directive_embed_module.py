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


class BaseDirectiveEmbedModule(Directive):
    """
    Directive for embedding all the code from a module and optionally the print output and plot.
    """

    @contextlib.contextmanager
    def stdoutIO(self, stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    def get_method_lines(self, args):
        py_file_path = args

        py_module = importlib.import_module(py_file_path)

        method_lines = inspect.getsource(py_module).split('\n')

        return method_lines

    def get_code_block(self, embed_num_indent, method_lines):
        lines = []
        lines.append(' ' * embed_num_indent + '.. code-block:: python\n')
        lines.append('\n')
        lines.extend([
            ' ' * embed_num_indent + ' ' * 2 + method_line + '\n'
            for method_line in method_lines
        ])
        return lines

    def get_print_block(self, embed_num_indent, method_lines):
        joined_method_lines = '\n'.join(method_lines)
        with self.stdoutIO() as s:
            exec(joined_method_lines)

        output_lines = s.getvalue().split('\n')

        lines = []
        if len(output_lines) > 1:
            lines.append(' ' * embed_num_indent + '::\n')
            lines.append('\n')
            lines.extend([
                ' ' * embed_num_indent + ' ' * 2 + output_line + '\n'
                for output_line in output_lines
            ])
        return lines

    def get_plot_block(self, embed_num_indent, method_lines, file_dir, file_name, size):
        joined_method_lines = '\n'.join(method_lines)
        plt.close()
        plt.figure(figsize=(8, 6))
        with self.stdoutIO() as s:
            exec(joined_method_lines)

        rel_plot_name = '{}.png'.format(file_name[:-5])

        abs_plot_name = file_dir + '/' + rel_plot_name
        plt.savefig(abs_plot_name)

        lines = []
        lines.append(' ' * embed_num_indent + '.. figure:: {}\n'.format(rel_plot_name))
        lines.append(' ' * embed_num_indent + '  :scale: {} %\n'.format(size))
        lines.append(' ' * embed_num_indent + '  :align: center\n')
        return lines


class DirectiveEmbedModule(BaseDirectiveEmbedModule):

    NAME = 'embed-module'
    NUM_ARGS = 1

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args[0])
        lines = self.get_code_block(embed_num_indent, method_lines)
        return lines


class DirectiveEmbedModulePrint(BaseDirectiveEmbedModule):

    NAME = 'embed-module-print'
    NUM_ARGS = 1

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args[0])
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_print_block(embed_num_indent, method_lines))
        return lines


class DirectiveEmbedModulePlot(BaseDirectiveEmbedModule):

    NAME = 'embed-module-plot'
    NUM_ARGS = 2

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args[0])
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_plot_block(embed_num_indent, method_lines, file_dir, file_name, args[1]))
        return lines


class DirectiveEmbedModulePrintPlot(BaseDirectiveEmbedModule):

    NAME = 'embed-module-print-plot'
    NUM_ARGS = 2

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args[0])
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_print_block(embed_num_indent, method_lines))
        lines.extend(self.get_plot_block(embed_num_indent, method_lines, file_dir, file_name, args[1]))
        return lines


class DirectiveEmbedModulePlotPrint(BaseDirectiveEmbedModule):

    NAME = 'embed-module-plot-print'
    NUM_ARGS = 2

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args[0])
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_plot_block(embed_num_indent, method_lines, file_dir, file_name, args[1]))
        lines.extend(self.get_print_block(embed_num_indent, method_lines))
        return lines
