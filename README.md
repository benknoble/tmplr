# tmplr

[![This project is considered stable](https://img.shields.io/badge/status-stable-success.svg)](https://benknoble.github.io/status/stable/)

Generate project files from templates on the command-line

## Installation

`tmplr` is on pip, so just

```bash
# python3 -m pip install tmplr
```

`tmplr` requires python 3 or greater.

## Usage

If you find yourself creating lots of similar scripts or files, and you usually
just do something like

```bash
# cp old new
# $EDITOR new
```

then `tmplr` is the solution.

Create temples (templates), then generate a file and start editing with

```bash
# tmplr sample-script var=value func_name=my_func -f script
```

See your templates, or edit them, using the `temples` command:

```bash
# temples
sample-script
vim-ftplugin
# temples -t sample-script
sample-script : sample sh script
Placeholders
	var
	func_name
# temples -e -t sample-script
```

(This is based on the example given at the end of the format description.)

See below for the temple file format.

By default, temples live in `~/.tmplr`, but this is configurable with the `-d`
switch to both programs.

Supply `-h` for more options.

# Temple-file format

A Temple file consists of two parts:
1. header
2. content

The header provides metadata specific to tmplr, and will be omitted when the
template is rendered into output.

The content is text, containing special template sequences which will be
substituted by render arguments upon output.

File extensions are ignored.

## Header format

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

## Temple metadata

The supported key-value pairs are:
- output
  The output directive can be a path (with `~` expansions), optionally
  containing the sequence `{fname}`. If the rendered template is written,
  it will be written to this path, with `{fname}` substituted for a
  filename by the engine (see `tmplr.temple.Temple.write`).

  If output is instead the string 'stdout', the rendered template will be
  printed to standard out.
- help
  The help directive provides a short description of the template
- delim
  The delim directive decides the special sequences that require render
  arguments.

  Any text of delim followed by name, or delim{name}, will be replaced by
  the render argument name (see `tmplr.temple.Temple.render`).

  Take care to choose a delim value that will not appear in the template
  except for in these escape sequences.

Unsupported values will be ignored, but not cause a parsing error.

### Example

```bash
###
# output : /tmp/tmplr-test-example-{fname}
# help : sample sh script
# delim : %%
###
#! /bin/sh

var=%%var
%%{func_name} () {
  echo do something
}

echo ${%%var}
```

### End Example

In this example, the comment character is '#' because the file is a shell
script. `%%var` will be replaced in both places (since `%%` is the delim) by the
`var` argument to render. Similarly `%%{func_name}` will be replaced the
`func_name` argument to render.

If `fname` is passed as, e.g., `templar`, the result will be written to
`/tmp/tmplr-test-example-templar`.
