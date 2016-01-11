"""Docstring to Markdown.

This piece of code is used within [Shed](https://www.github.com/cmry/shed) to
convert NumPy-styled Python docstrings to Markdown. In this way, only the
code documentation needs to be editted, and the Readthedocs is automatically
updated thereafter. To use it, simply type `python3 markdoc.py
somefile.py somedoc.md`. Check class help for Python usage. Don't forget to
also check the class notes (they are important for docstring format
guidelines).
"""

from sys import argv

# Author:       Chris Emmery
# License:      MIT
# pylint:       disable=W0142,R0201

ERR = '''
* list index out of range
- \"\"\" used for non-docstring strings.
- First Class or method Documentation line has newline after \"\"\".
  Fix with: \"\"\"This is the first line.

  Here comes the rest.
  \"\"\"

* Class parameters not showing in code blocks
- Class is not structed new-style (class SomeClass(object):)

* Code blocks not showing
- Code is in IPython style rather than vanilla (i.e. In [1]: instead of >>>)

* tuple index out of range
- Mistake in var : type lists (for example var: type).
- Description also contains a :.

* some table parts are not showing
- Probably included some seperators in there such as : or -----.

* methods are garbled
- Did you name a parameter 'class' or any other matches?
'''

MD_TABLE = '''

| {0}    | Type             | Doc             |
|:-------|:-----------------|:----------------|
'''
MD_TABLE_ROW = '| {0} | {1} | {2} | \n'

MD_TABLE_ALT = '''
| {0}    | Doc             |
|:-------|:----------------|
'''
MD_TABLE_ROW_ALT = '| {0} | {1} | \n'

MD_CODE = '``` python \n {0} \n```\n\n'


class MarkDoc(object):

    r"""Documentation to Markdown.

    This class converts a Python file with properly formed NumPy-styled
    docstrings to a markdown file that can be used in for example Readthedocs
    or Jekyll.

    Parameters
    ----------
    file_in : str
        Python (.py) file from where the docstrings should be taken.

    file_out : str
        Markdown (.md) file where the documentation should be written.

    cold : boolean, optional, default False
        If you want to start the class without starting the reader, set True.

    Attributes
    ----------
    markdown : str
        The entire Markdown file that will be appended to and written out.

    Examples
    --------

    Use of the package should just be from commandline with `python3 markdoc.py
    in.py out.md`. However, if for some reason it is required to load it as a
    class, you can just do:

    >>> from markdoc import MarkDoc
    >>> md = MarkDoc('some/dir/file.py', '/some/otherdir/doc.md')

    The string of the markdown can be accessed by:

    >>> print(md.markdown)

    Notes
    -----
    List of common errors and styleguide conflicts:

    #### list index out of range?
    - \"\"\" used for non-docstring strings.
    - First Class or method Documentation line has newline after \"\"\".
      Fix with: \"\"\"This is the first line.

      Here comes the rest.
      \"\"\"

    #### Class parameters not showing in code blocks?
    - Class is not structed new-style (object after class).

    #### Code blocks not showing?
    - Code is IPython style rather than vanilla (i.e. In [1]: instead of >>>).

    #### tuple index out of range?
    - Mistake in var : type lists (for example var: type).
    - Description also contains a :.

    #### some table parts are not showing?
    - Probably included some seperators in there such as : or \-\-\-\-\-.

    #### methods are garbled?
    - Did you name a parameter 'class' or any other matches?
    """

    def __init__(self, file_in, file_out, cold=False):
        """Handle in/out to readers and parsers."""
        self.markdown = ''
        if not cold:
            self.read(file_in, file_out)
        # FIXME: code does not handle staticmethods yet?

    def read(self, file_in, file_out):
        """Open Python code file, spit out markdown file."""
        with open(file_in, 'r') as file_in:
            # get rid of special docstring parts
            classes = file_in.read().replace('r"""', '"""').split('\nclass ')
            self.markdown = [self.md_title(classes.pop(0))]  # top of the file
            self.handle_classes(classes)
        with open(file_out, 'w') as file_out:
            file_out.write('\n'.join(self.markdown))

    def handle_classes(self, classes):
        """Given class docs only, write out their docs and methods."""
        for class_code in classes:
            class_code = " class " + class_code  # got cut-off in split
            class_parts = class_code.split('"""\n')[:-1]
            # process all the class information
            class_doc = class_parts.pop(0)  # class docstring, rest is methods
            self.markdown.append(
                self.md_class_doc(self.structure_doc(class_doc)))
            # replace object part with __init__ params
            self.markdown[1] = \
                self.md_class_method(self.markdown[1], class_parts)
            # start handling methods
            self.markdown.append(
                self.md_methods_doc([self.structure_doc(method)
                                     for method in class_parts]))

    def find_declaration(self, lines):
        """Find `class Bla(object):` or `def method(params):` across lines."""
        declaration, found_start = '', False
        # skip lines until class/def, end if :
        while ':' not in declaration:
            if lines[0].startswith(' class ') or \
               lines[0].startswith('    def '):
                found_start = True
            line = lines.pop(0)
            if found_start:
                declaration += line
        return declaration

    def structure_doc(self, doc):
        """Produce a structured dictionary from docstring.

        The key is the part of the documentation (name, title, params,
        attributes, etc.), and value is a list of lines that make up this part.
        Is used to handle the order and different parses of different sections.

        Parameters
        ----------
        doc : str
            Flat string structure of a docstring block.

        Returns
        -------
        X_doc : dict
            Class or method doc, a structure dict with section; lines.
        """
        lines = [x for x in doc.split('\n') if x]
        parts = {'name': self.find_declaration(lines)}
        buffer_to = 'title'

        # if ----- is found, set title to above, else buffer to name
        for i in range(0, len(lines)):
            line = lines[i]
            if '---' in line:  # get tile
                buffer_to = lines[i-1]
                continue
            if not parts.get(buffer_to):  # buffer to 'title' by default
                parts[buffer_to] = [buffer_to]
            if parts.get(buffer_to) and line:
                parts[buffer_to].append(line)

        # if line is shorter than 3, likely that there is no previous section
        return {k.replace('  ', ''):
                (v[:-1] if len(v) > 2 else v)[1:] for k, v in parts.items()}

    def md_title(self, title_part, class_line=False):
        """Handle title and text parts for main and class-specific.

        Pretty convoluted but delicate method that seperates the top part
        that should not be part of the title docstring off the document,
        handles correct punctuation of titles, for both classes and methods.
        Also detects if there's a description under the first line.

        Parameters
        ----------
        title_part : str
            Part of the document that starts with triple quotes and is below
            any line seperators.

        class_line : bool, optional, default False
            The first line of the docstring by default servers as a title
            header. However, for classes it should be formed into a normal
            description. Thefefore, the # marker is removed and a . is added.

        Returns
        -------
        line_buffer : str
            Correctly formated markdown from the buffer.
        """
        line_buffer, start_buffer, description = [], False, False
        for line in title_part.split('\n'):
            line = line.replace('  ', '')
            if line.count('"""') == 2:  # one liner
                return '# ' + line.replace('"""', '')[:-1]  # title
            elif line.startswith('"""') and not start_buffer:
                title = '# ' + line.replace('"""', '')[:-1]  # title
                if class_line:
                    title = title[2:] + '.'  # normal description
                line_buffer.append(title)
                start_buffer = True
            elif line.startswith('"""') and start_buffer:  # handle top of file
                return '\n'.join(line_buffer)
            elif start_buffer:
                if not description and not line.startswith('\n'):
                    line = "\n" + line
                    description = True
                line_buffer.append(line)

        return '\n'.join(line_buffer)

    def md_table(self, doc, name):
        r"""Place parameters and attributes in a table overview.

        The documentation parts that are typed by 'var : type \n description'
        can be splitted into a table. The same holds true for a list of class
        methods. These are handled by this method. Table structures are on
        the top of this Python file.

        Parameters
        ----------
        doc : str
            Flat string structure of a docstring block.

        name : str
            Indicator for the table, can be for example Parameters or
            Attributes.

        Returns
        -------
        table : str
            Markdown-type table with filled rows and formatted name.
        """
        var_type, line_buffer, lines = '', (), []
        table = MD_TABLE.format(name)

        # given var : type \n description, splits these up into 3 cellss
        if not doc:
            return ''

        for row in doc:
            if ':' in row and line_buffer:  # if we hit the next, store table
                line_buffer += (''.join(lines), )
                table += MD_TABLE_ROW.format(*line_buffer)
                line_buffer = ()
                lines = []
            if ':' in row and not line_buffer:  # it's var : type
                var_type = row.split(' : ')
                for part in var_type:
                    line_buffer += (part, )
            elif line_buffer:  # if no next, keep appending rows
                lines.append(row.replace('\n', ' '))

        if line_buffer:  # empty the buffer
            line_buffer += (''.join(lines), )
            table += MD_TABLE_ROW.format(*line_buffer)

        return table

    def md_code_text(self, doc, name, flat=False):
        """Section text and/or code in the example part of the doc.

        If some code related beginnings (>>>, ...) is founds buffer to code,
        else we regard it as text. Record order so that multiple consecutive
        blocks of text and code are possible.

        Parameters
        ----------
        doc : str
            Flat string structure of a docstring block.
        name : str
            Name of the section (Examples, Notes).
        flat : bool, optional, default False
            If there are no code blocks, flat can be used to stop parsing them.

        Returns
        -------
        code : str
            Formatted block of fenced markdown code-snippets and flat text.

        Notes
        -----
        Please note that this method assumes markdown is uses so-called
        fenced codeblocks that are commonly accepted by Readthedocs, GitHub,
        Bitbucket, and Jekyll (for example with Redcarpet).

        This current implementation does NOT allow for IPython styled code
        examples. (In [1]: Out[1]: etc.)
        """
        head = '\n\n------- \n\n##{1}\n\n{0}'
        order, text, code = [], '', ''

        if not doc:
            return ''

        # if code marker, store to code, else store to text
        for row in doc:
            if not flat and ('>>>' in row or '...' in row):
                if text:
                    order.append(text)
                    text = ''
                row = row.replace('    >>>', '>>>')
                row = row.replace('    ...', '...')
                code += row + '\n'
            else:
                if code:
                    # if we found code, encapsulate in ``` python ``` blocks.
                    order.append(MD_CODE.format(code))
                    code = ''
                row = row.replace('  ', '')
                text += row + '\n' + ('\n' if any([row.endswith(x) for x
                                      in ('!', '?', '.', ':')]) else '')

        if text:  # empty the buffer
            order.append(text.replace('\\', ''))
        if code:
            order.append(MD_CODE.format(code))

        return head.format('\n'.join(order).replace('.\n', '.\n\n'), name)

    def md_class_method(self, doc, class_parts):
        """Replace `class ...(object)` with `__init__` arguments.

        In NumPy-style, each class is represented as it's name, along with
        the parameters accepted in `__init__` as its parameters, as you would
        call the method in Python. The markdown therefore needs to fill the
        (object) tag that is assigned to classes with the `__init__` params.

        Parameters
        ----------
        doc : str
            Flat string structure of a docstring block.

        class_parts : list
            List with parts that the docstring constituted of. First line
            should be the class name and can therefore be replaced.

        Returns
        -------
        doc : str
            Same as doc, only now (object) has been replaced with `__init__`
            parameters.

        Notes
        -----
        Please note that this implementation assumes you're using new-style
        class declarations where for example `class SomeClass:` should be
        written as `class SomeClass(object):`.
        """
        # FIXME: does not seem to work for consecutive classes!

        init_doc = self.structure_doc(class_parts.pop(0))['name']
        init_doc = init_doc.replace('  ', '')
        init_doc = init_doc.replace(' def __init__(self, ', '(')

        # FIXME: (object) screws up other class inherrits, make general regex
        return doc.replace('(object)', init_doc)

    def md_methods_doc(self, method_doc):
        """Merge all method elements in one string.

        This method will scan each method docstring and extract parameters,
        returns and descriptions. It will append them to the method table
        and link (TODO) them in the doc.

        Parameters
        ----------
        method_doc : list
            Lower part of the class docstrings that holds a method docstring
            per entry.

        Returns
        -------
        methods : str
            Formatted markdown string with all method information.

        Notes
        -----
        On the bottom, dict calls are being done to order several parts of
        the docstring. If you use more than Parameters and Returns, please make
        sure they are added in the code there.
        """
        mark_doc, mark_head = '', '\n--------- \n\n## Methods \n\n {0} \n {1}'
        method_table = MD_TABLE_ALT.format('method')

        for method in method_doc:
            # isolate only the name of the function (without def and params)
            name = method['name'].replace('(', ' (').split()[1]
            title = self.md_title('\n'.join(method['title']), class_line=True)

            # name and first line of description are added to method_table
            method_table += MD_TABLE_ROW_ALT.format(name, title.split('\n')[0])
            mark_doc += '\n\n### ' + name + '\n\n'

            # show the method call with parameters
            code = MD_CODE.format(method['name'].replace('def ', ''))
            code = code.replace('self', '').replace('(, ', '(')

            mark_doc += code
            mark_doc += '\n' + title

            # add to sections here if more blocks are possible!
            mark_doc += self.md_table(method.get('Parameters'), 'Parameters')
            mark_doc += self.md_table(method.get('Returns'), 'Returns')
            mark_doc += self.md_code_text(method.get('Notes'), '## Notes')

        return mark_head.format(method_table, mark_doc)

    def md_class_doc(self, class_doc):
        """Merge all class section elements in one string.

        This will piece together the descriptions contained in the docstring
        of the class. Currently, they are written *below* the top of the
        Python file, and not put into any subfiles per class.

        Parameters
        ----------
        class_doc : str
            Flat text containing the class docstring part.

        Returns
        -------
        mark_doc : str
            Markdown formatted class docstring, including all subsections.

        Notes
        -----
        On the bottom, dict calls are being done to order several parts of
        the docstring. If you use more than Parameters, Attributes, Examples,
        and Notes, please make sure they are added in the code there.
        """
        mark_doc = ''

        # class name is being used as title
        mark_doc += '\n\n# {0} \n\n'.format(
            class_doc['name'].replace('(', ' (').split()[1])
        mark_doc += MD_CODE.format(class_doc['name'])

        # frist docstring line for a class is just written as a sentence
        mark_doc += self.md_title('\n'.join(class_doc['title']),
                                  class_line=True)

        # add to sections here if more blocks are possible!
        mark_doc += self.md_table(class_doc.get('Parameters'), 'Parameters')
        mark_doc += self.md_table(class_doc.get('Attributes'), 'Attributes')
        mark_doc += self.md_code_text(class_doc.get('Examples'), 'Examples')
        mark_doc += self.md_code_text(class_doc.get('Notes'), 'Notes',
                                      flat=True)

        return mark_doc

if __name__ == '__main__':
    try:
        D2M = MarkDoc(argv[1], argv[2])
        print("Succesfully converted!")
    except Exception as err:
        exit("-"*10 + "\nERROR! Malformed code \n\nTraceback: \n\n{1} \n\n\n\
Some common errors: \n{0}".format(ERR, err))
