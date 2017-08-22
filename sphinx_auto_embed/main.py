import sys
import six

from sphinx_auto_embed.utils import get_rstx_file_paths, get_directives


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    rstx_file_paths_list = get_rstx_file_paths()
    directives_list = get_directives()

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
