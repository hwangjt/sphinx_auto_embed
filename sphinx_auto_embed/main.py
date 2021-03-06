import os
import sys
import six
from sphinx_auto_embed.utils import get_rstx_file_paths, get_directives, read_embedrc


def main(args=None):
    """
    Find and process all rstx files and turn them into rst files with requested content embedded.

    This is what is run when sphinx_auto_embed is called from the command line.
    """
    if args is None:
        args = sys.argv[1:]

    cwd_abs_path = os.getcwd()

    custom_directives_dir = read_embedrc(cwd_abs_path)

    rstx_file_paths_list = get_rstx_file_paths(cwd_abs_path)
    directives_list = get_directives(custom_directives_dir)

    for file_dir, file_name in rstx_file_paths_list:
        file_path = file_dir + '/' + file_name
        new_file_path = file_path[:-5] + '.rst'

        with open(file_path, 'r') as f:
            old_lines = f.readlines()

        new_lines = []
        for iline, line in enumerate(old_lines):

            stripped_line = line.replace(' ', '')

            for directive in directives_list:
                if '..%s::' % directive.NAME in stripped_line:
                    lines = directive(file_dir, file_name, iline, line)
                    break
            else:
                lines = [line]

            new_lines.extend(lines)

        with open(new_file_path, 'w') as f:
            f.writelines(new_lines)
