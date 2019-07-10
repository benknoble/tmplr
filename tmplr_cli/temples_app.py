'''temples' frontend orchestration'''

import argparse
import os
import os.path as path
import sys

import tmplr
import tmplr.temple
import tmplr_cli
import tmplr_cli.editor as editor


def parser():
    p = argparse.ArgumentParser(
            description='Queries temples',
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
            '-D',
            '--print-dir',
            help='Only print the temples dir. Compatible with -d',
            action='store_true',
            )
    p.add_argument(
            '-e',
            '--edit',
            action='store_true',
            help='Edit the temple',
            )
    p.add_argument(
            '-t',
            '--temple',
            help='Temple to query',
            # type=tmplr.temple.from_file,
            # can't do this because we depend on -d dir
            )
    p.add_argument(
            '-T',
            '--print-temple',
            help='only print path to temple. Requires -t',
            action='store_true',
            )
    return p


def main():
    p = parser()
    args = p.parse_args()
    temples = tmplr.temple.temples(args.dir)
    if args.print_dir:
        print(args.dir)
        sys.exit(0)
    elif args.temple is None:
        print('\n'.join(temples.keys()))
        sys.exit(0)
    # temple given
    else:
        temple = path.join(args.dir, args.temple)
        if args.print_temple:
            print(temple)
            sys.exit(0)
        elif args.edit:
            if not path.exists(args.dir):
                os.makedirs(args.dir)
            sys.exit(editor.edit(temple))
        else:
            if args.temple not in temples:
                p.error('''No temple "{temple}".

Create it with "temples -e -t {temple}".'''.format(temple=args.temple))
            temple = tmplr.temple.from_file(temple)
            print(temple.helptext())
            sys.exit(0)


if __name__ == '__main__':
    main()
