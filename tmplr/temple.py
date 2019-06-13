'''Classes and functions for dealing with tmplr templates

Classes:
    Temple -- a template

Functions:
    make_Template -- generates a subclass of string.Template on the fly
    from_file -- Temple from file
    temples -- maps names to Temples in a directory
'''

import string
import re
import os
import os.path as path
import glob


def make_Template(name, **kwargs):
    '''make_Template(name, **kwargs) -> subclass of string.Template

    - name is the name of the subclass
    - kwargs is passed as the dict element to type
    '''
    return type(
            name,
            (string.Template,),
            kwargs)


class Temple(object):
    '''Template object for templr

    Temple(name, output, helptext, content, delim='%%') -> new Temple

    Methods:
        helptext() -- text for help on the Temple
        placeholders() -- a list of names needing values for render
        render(subs=None, **kwargs) -- render the template
                                  (see string.Template.safe_substitute)
        write(filename=None) -- write via output
    '''

    def __init__(self, name, output, helptext, content, delim='%%'):
        self.name = name
        self.output = output
        self.help = helptext
        self.content = content
        self.delim = delim
        self.placeholder_re = re.compile(re.escape(delim) + r'{?\w+}?')
        self.Template = make_Template(name, delimiter=delim)
        self.template = self.Template(content)

    def helptext(self):
        '''helptext() -> str

        Text suitable for display as help about the Temple
        '''
        return '%s : %s\nPlaceholders\n\t%s' % (
                self.name,
                self.help,
                '\n\t'.join(self.placeholders()))

    def placeholders(self):
        '''placeholders() -> list

        List of names needing values for render
        '''
        return _orderedset(
                map(
                    lambda p: p.lstrip(self.delim + '{').rstrip('}'),
                    self.placeholder_re.findall(self.template.template)))

    def render(self, subs=None, **kwargs):
        '''render(subs=None, **kwargs) -> str

        see string.Template.safe_substitute for the parameters
        '''
        self.rendered = self.template.safe_substitute(subs, **kwargs)
        return self.rendered

    def write(self, filename=None, stdout=False):
        '''write(filename=None) -> path

        Write via output.
            1. If any of
                - stdout is True
                - output is stdout
                - filename is None but {fname} is in output
                then print and return None
            2. Else, write to file(output) & return path written
                - {fname} will be substituted for filename
                - if path already exists, don't write, but return path
        '''
        stdout_conditions = (
                stdout,
                self.output is 'stdout',
                filename is None and '{fname}' in self.output,
                )
        if any(stdout_conditions):
            print(self.rendered, end='')
            return None
        else:
            fullpath = path.expanduser(
                    self.output.format(fname=filename))
            dirname = path.dirname(fullpath)
            if path.exists(fullpath):
                # silent
                return fullpath
            if not path.isdir(dirname):
                os.makedirs(dirname)
            with open(fullpath, mode='w', errors='strict') as f:
                f.write(self.rendered)
            return fullpath


def from_file(filename):
    '''from_file(filename) -> Temple

    Read filename to produce a Temple. see package documentation for details on
    the format.

    Take care--almost no error handling is done. Bad input will fail noisly.
    '''
    comment_char = ''
    directives = dict()
    content = ''
    with open(filename, mode='r', errors='strict') as f:
        firstline = f.readline()
        comment_char = firstline[0]
        for line in f:
            if line == firstline:
                break
            (directive, value) = map(
                    lambda s: s.strip(),
                    line.lstrip(comment_char).split(':'))
            directives[directive] = value
        content = f.read()
    return Temple(
            path.basename(filename),
            directives['output'],
            directives['help'],
            content,
            delim=directives['delim'])


def temples(tpath):
    '''temples(tpath) -> dict

    The result is a mapping of template names to Temple values.  If tpath is a
    directory, this mapping contains a Temple for each file in the directory.
    If it is a single file, it only contains that file.

    See also from_file.
    '''
    if not path.exists(tpath):
        return dict()
    elif path.isdir(tpath):
        files = glob.iglob(
                path.join(
                    path.expanduser(tpath),
                    '*'))
    elif path.isfile(tpath):
        files = [tpath]
    else:
        return dict()
    return {t.name: t
            for t in map(
                from_file,
                files)}


def _orderedset(keys):
    return list(dict.fromkeys(keys).keys())
