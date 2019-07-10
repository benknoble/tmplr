'''tmplr's frontend orchestration'''

import argparse
import os.path as path
import sys

import tmplr
import tmplr.temple
import tmplr_cli
import tmplr_cli.editor as editor


def parser():
    p = argparse.ArgumentParser(
            description='Holy template renderer',
            )
    p.add_argument(
            '--version',
            action='version',
            version=tmplr_cli.__version__,
            )
    p.add_argument(
            '-d',
            '--dir',
            default=path.expanduser(path.join('~', '.tmplr')),
            help='Directory of temples: default ~/.tmplr',
            )
    p.add_argument(
            '--no-edit',
            action='store_true',
            help='Do not edit the rendered temple--just generate it',
            )
    p.add_argument(
            '--stdout',
            action='store_true',
            help='Write rendered temple to stdout; implies --no-edit',
            )
    p.add_argument(
            '-f',
            '--file',
            help='''Provide a filename for {fname}. If no filename is given for
                    {fname}, implies --stdout''',
            )
    p.add_argument(
            '-F',
            '--print-file',
            help='''Do not render temple. Print filename for rendered
                    template (including -f values). Not compatible with any
                    other render options.''',
            action='store_true',
            )
    p.add_argument(
            'temple',
            help='Temple to render',
            # type=tmplr.temple.from_file,
            # can't do this because we depend on -d dir
            )
    p.add_argument(
            'render_args',
            nargs='*',
            help='var=value substitutions to be rendered',
            )
    return p


def parse_kv(kv):
    key, *vals = kv.split('=')
    val = '='.join(vals)
    return (key, val)


def main():
    p = parser()
    args = p.parse_args()
    if args.stdout:
        args.no_edit = True
    temples = tmplr.temple.temples(args.dir)
    if args.temple not in temples:
        p.error('''No temple "{temple}".

Create it with "temples -e -t {temple}".'''.format(temple=args.temple))
    temple = tmplr.temple.from_file(path.join(args.dir, args.temple))
    if args.print_file:
        print(temple.filename(args.file))
        sys.exit(0)
    subs = dict(
            map(
                lambda kv: parse_kv(kv),
                args.render_args))
    if not all(
            key in subs
            for key in temple.placeholders()):
        p.error('''Missing placeholder value.

Run "temples -t {temple}" to see available keys.'''.format(temple=args.temple))
    temple.render(subs)
    written = temple.write(filename=args.file, stdout=args.stdout)
    if written:
        if args.no_edit:
            # log file for application usage
            print(written)
            exit = 0
        else:
            exit = editor.edit(written)
    else:
        exit = 0
    sys.exit(exit)


if __name__ == '__main__':
    main()
