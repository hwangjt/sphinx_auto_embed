class Directive(object):

    def exception(self, msg):
        raise Exception('In file {} line {}: {}'.format(self.file_path, self.iline + 1, msg))

    def __call__(self, file_dir, file_name, iline, line):
        self.file_path = file_path = file_dir + '/' + file_name
        self.iline = iline

        # Compute indentation
        embed_num_indent = line.find('.. %s' % self.NAME)

        # Make sure there are no characters before the directive call
        if line[:embed_num_indent] != ' ' * embed_num_indent:
            self.exception('there should only be white spaces before the directive.')

        # Remove spaces and newline character
        stripped_line = line.replace(' ', '').replace('\n', '')

        # Split out directive and args
        split_line = stripped_line.split('::')
        if len(split_line) > 2:
            self.exception('"::" should only appear once.')

        # Read args
        if split_line[1] == '':
            args = []
        else:
            args = split_line[1].split(',')

        # Get number of arguments
        num_args = len(args)
        if num_args != self.NUM_ARGS:
            self.exception('there should be {} arguments for directive "{}", separated by commas.'
                % (self.NUM_ARGS, self.NAME))

        return self.run(file_dir, file_name, embed_num_indent, args)
