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
    return p


def main():
    p = parser()
    args = p.parse_args()
    if args.temple is None:
        temples = tmplr.temple.temples(args.dir)
        print('\n'.join(temples.keys()))
        sys.exit(0)
    elif args.edit:
        if not path.exists(args.dir):
            os.makedirs(args.dir)
        temple = path.join(args.dir, args.temple)
        sys.exit(editor.edit(temple))
    else:
        temples = tmplr.temple.temples(args.dir)
        if args.temple not in temples:
            p.error('''No temple "{temple}".

Create it with "temples -e -t {temple}".'''.format(temple=args.temple))
        temple = tmplr.temple.from_file(path.join(args.dir, args.temple))
        print(temple.helptext())
        sys.exit(0)


if __name__ == '__main__':
    main()
