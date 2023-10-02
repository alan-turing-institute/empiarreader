"""CLI for empiarreader
"""

import argparse

import empiarreader.utilities.search
import empiarreader.utilities.download


def main():
    # parse command line args
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="",
    )
    subparsers.required = True

    modules = [
        empiarreader.utilities.search,
        empiarreader.utilities.download,
    ]

    helptext = [
        "",
        "",
    ]

    for help, module in zip(helptext, modules):
        new_parser = subparsers.add_parser(
            module.get_name(),
            help=help,
        )
        module.add_arguments(new_parser)
        new_parser.set_defaults(func=module.main)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
