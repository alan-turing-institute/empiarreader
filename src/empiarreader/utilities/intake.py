"""_summary_
"""

import argparse

from empiarreader.empiar.empiar import EmpiarSource


def add_arguments(parser):
    # for searching EMPIAR
    parser.add_argument(
        "--entry",
        help="EMPIAR entry #",
        type=int,
        default=None,
        required=True,
    )
    parser.add_argument(
        "--dir",
        help="Directory in EMPIAR entry to query",
        type=str,
        default="",
        required=False,
    )
    parser.add_argument(
        "--select",
        help="Wildcard path to select file(s) and/or directories within entry",
        type=str,
        default=None,
        required=True,
    )
    parser.add_argument(
        "--regexp",
        help=(
            "Whether 'select' is regex-style instead of bash-style."
            " Defaults to bash-style"
        ),
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="Increase verbosity to stdout",
        action="store_true",
        required=False,
    )

    return parser


def get_name():
    return "intake"


def main(args):
    """ """

    ds = EmpiarSource(
        args.entry,
        directory=args.dir,
        filename=args.select,
    )
    print(ds.data_directory_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser = add_arguments(parser)
    args = parser.parse_args()
    if args.verbose:
        for arg in vars(args):
            print("{}, {}".format(arg, getattr(args, arg)))
    main(args)
