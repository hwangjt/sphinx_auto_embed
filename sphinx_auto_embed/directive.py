class Directive(object):

    def exception(self, msg):
        """
        Raise an exception because a directive call was made incorrectly.

        Parameters
        ----------
        msg : str
            Descriptive error message to show in addition to the file name and line number.
        """
        raise Exception('In file {} line {}: {}'.format(self.file_path, self.iline + 1, msg))

    def __call__(self, file_dir, file_name, iline, line):
        """
        Perform the task associated with the current directives.

        This involves taking the given line and returning a list of replacement lines with
        any desired content dynamically generated and embedded.

        Parameters
        ----------
        file_dir : str
            Absolute path to the directory containing the rstx file being parsed.
        file_name : str
            Name of the rstx file being parsed.
        iline : int
            Line number of the line being parsed; this is used for error messages.
        line : str
            A single string representing the raw line from the rstx file.
            This contains leading spaces and the end-of-line character, '\n'.

        Returns
        -------
        list of str
            List of lines to replace the incoming line with.
        """
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
            self.exception(
                'there should be {} arguments for directive "{}", separated by commas.'.format(
                    self.NUM_ARGS, self.NAME))

        return self.run(file_dir, file_name, embed_num_indent, args)
