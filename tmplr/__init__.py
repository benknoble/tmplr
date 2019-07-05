'''The holiest cli template system

tmplr provides modules for working with tmplr templates, called Temples. Most
Temples are represented by actual files on disk, so a convenience function is
provided to create a Temple from a path. Programmatic access is also provided.

Modules:
    temple -- provides the Temple class and helper functions

Temple-file format
------------------

A Temple file consists of two parts:
    1. header
    2. content

The header provides metadata specific to tmplr, and will be omitted when the
template is rendered into output.

The content is text, containing special template sequences which will be
substituted by render arguments upon output.

Header format
=============

The first line of the header must consist of the same character repeated
thrice. We call this the "comment character" because, if you use a character
considered a comment for the normal file content, editors will not choke on
Temple headers.

The next lines consist of metadata and all follow this format:
    {comment character} key : value

A value ends once the line is terminated by a newline character.

After the metadata is the last line of the header--it is a carbon copy of the
first line of the header.

Anything after the second sequence of 3 comment characters is considered
content and read literally.

Temple metadata
===============

The supported key-value pairs are:
    - output
        The output directive can be a path (with ~ expansions), optionally
        containing the sequence {fname}. If the rendered template is written,
        it will be written to this path, with {fname} substituted for a
        filename by the engine (see tmplr.temple.Temple.write).

        If output is instead the string 'stdout', the rendered template will be
        printed to standard out.
    - help
        The help directive provides a short description of the template
    - delim
        The delim directive decides the special sequences that require render
        arguments.

        Any text of delim followed by name, or delim{name}, will be replaced by
        the render argument name (see tmplr.temple.Temple.render).

        Take care to choose a delim value that will not appear in the template
        except for in these escape sequences.

Unsupported values will be ignored, but not cause a parsing error.

*** Example ***

###
# output : /tmp/tmplr-test-example-{fname}
# help : tmux config script
# delim : %%
###
#! /bin/sh
content...
%%var
%%{func_name}
%%var
...etc.

*** End Example ***

In this example, the comment character is '#' because the file is a shell
script. %%var will be replaced in both places (since %% is the delim) by the
var argument to render. Similarly %%{func_name} will be replaced the func_name
argument to render.

If fname is passed as, e.g., templar, the result will be written to
/tmp/tmplr-test-example-templar.
'''

__version__ = '0.0.3'
