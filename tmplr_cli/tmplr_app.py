'''tmplr's frontend orchestration'''

import argparse
import os.path as path

import tmplr
import tmplr.temple
import tmplr_cli.editor as editor


def parser():
    p = argparse.ArgumentParser(
            description='Holy template renderer',
            )
    p.add_argument('--version', action='version', version=tmplr.__version__)
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


def main():
    p = parser()
    args = p.parse_args()
    if args.stdout:
        args.no_edit = True
    temples = tmplr.temple.temples(args.dir)
    if args.temple not in temples:
        p.error('''No temple '{temple}'.

Create it with temples -e {temple}'''.format(
                    temple=args.temple))
    temple = tmplr.temple.from_file(path.join(args.dir, args.temple))
    # parse render_args
    # write should return path written, or None
    # write needs a stdout=False option
    print(args)


if __name__ == '__main__':
    main()
