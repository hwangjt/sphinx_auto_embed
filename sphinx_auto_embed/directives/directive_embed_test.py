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


class BaseDirectiveEmbedTest(Directive):
    """
    Directive for embedding a test code snippet and optionally the print output and plot.

    The 3 arguments are the module name, class name, and method name.
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
        py_file_path, class_name, method_name = args

        py_module = importlib.import_module(py_file_path)

        obj = getattr(py_module, class_name)
        method = getattr(obj, method_name)

        method_lines = inspect.getsource(method).split('\n')
        for imethod_line, method_line in enumerate(method_lines):
            if 'def' in method_line and method_name in method_line:
                imethod_line += 1
                break
        method_lines = method_lines[imethod_line:]

        first_line = method_lines[0]
        py_num_indent = first_line.find(first_line.strip())

        for imethod_line, method_line in enumerate(method_lines):
            method_lines[imethod_line] = method_line[py_num_indent:]

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

    def get_plot_block(self, embed_num_indent, method_lines, file_dir, file_name):
        joined_method_lines = '\n'.join(method_lines)
        plt.clf()
        with self.stdoutIO() as s:
            exec(joined_method_lines)

        abs_plot_name = file_dir + '/' + file_name[:-5] + '.png'
        plt.savefig(abs_plot_name)

        rel_plot_name = file_name[:-5] + '.png'

        lines = []
        lines.append(' ' * embed_num_indent + '.. figure:: {}\n'.format(rel_plot_name))
        lines.append(' ' * embed_num_indent + '  :scale: 80 %\n')
        lines.append(' ' * embed_num_indent + '  :align: center\n')
        return lines


class DirectiveEmbedTest(BaseDirectiveEmbedTest):

    NAME = 'embed-test'
    NUM_ARGS = 3

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args)
        lines = self.get_code_block(self, embed_num_indent, method_lines)
        return lines


class DirectiveEmbedPlot(BaseDirectiveEmbedTest):

    NAME = 'embed-plot'
    NUM_ARGS = 3

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args)
        lines = self.get_plot_block(embed_num_indent, method_lines, file_dir, file_name)
        return lines


class DirectiveEmbedTestPrint(BaseDirectiveEmbedTest):

    NAME = 'embed-test-print'
    NUM_ARGS = 3

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args)
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_print_block(embed_num_indent, method_lines))
        return lines


class DirectiveEmbedTestPlot(BaseDirectiveEmbedTest):

    NAME = 'embed-test-plot'
    NUM_ARGS = 3

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args)
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_plot_block(embed_num_indent, method_lines, file_dir, file_name))
        return lines


class DirectiveEmbedTestPrintPlot(BaseDirectiveEmbedTest):

    NAME = 'embed-test-print-plot'
    NUM_ARGS = 3

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args)
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_print_block(embed_num_indent, method_lines))
        lines.extend(self.get_plot_block(embed_num_indent, method_lines, file_dir, file_name))
        return lines


class DirectiveEmbedTestPlotPrint(BaseDirectiveEmbedTest):

    NAME = 'embed-test-plot-print'
    NUM_ARGS = 3

    def run(self, file_dir, file_name, embed_num_indent, args):
        method_lines = self.get_method_lines(args)
        lines = []
        lines.extend(self.get_code_block(embed_num_indent, method_lines))
        lines.extend(self.get_plot_block(embed_num_indent, method_lines, file_dir, file_name))
        lines.extend(self.get_print_block(embed_num_indent, method_lines))
        return lines
