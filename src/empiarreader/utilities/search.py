"""Searches EMPIAR to return HTTPS filepaths of files
empiarreader search --entry 10934  --select "*.xml" --save_search my_search.txt
Use --verbose to make the output more user friendly
"""

import os
import argparse

import numpy as np

from empiarreader.empiar.empiar import EmpiarSource


def add_arguments(parser):
    """Set out the arguments for the search utility

    Args:
        parser (argparse.ArgumentParser): argument parser

    Returns:
        argparse.ArgumentParser: argument parser
    """
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
        "--save_search",
        help="File name to save search results as newline separated text",
        default=None,
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="Increase verbosity to stdout",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--keep_all",
        help="Keep apache-related files returned by query",
        action="store_true",
        required=False,
    )

    return parser


def get_name():
    """Name the search utility

    Returns:
        str: utility name
    """
    return "search"


def main(args):
    """Search a directory in an EMPIAR entry for files and optionally write
    HTTPS paths to a file ready for download utility/other use

    Args:
        args (argparse.ArgumentParser): argument parser with parsed args
    """
    ds = EmpiarSource(
        args.entry,
        directory=args.dir,
        filename=args.select,
        regexp=args.regexp,
    )

    filelist = ds._parse_data_dir(ds.data_directory_url)
    if ~args.keep_all:
        # filter out apache display-related results
        filelist = [f for f in filelist if "?C=N;O=D" not in f]
        filelist = [f for f in filelist if "?C=M;O=A" not in f]
        filelist = [f for f in filelist if "?C=S;O=A" not in f]
        filelist = [f for f in filelist if "?C=D;O=A" not in f]
        # filter out repeated path
        filelist = [
            f for f in filelist if f.split("/").count("world_availability") < 2
        ]

    matching_files = [
        url for url in filelist if ds.image_url_regexp.match(url)
    ]

    if args.verbose:
        for i, filename in enumerate(sorted(matching_files)):
            print("Matching path #{}: {}".format(i, filename))
    else:
        for filename in sorted(matching_files):
            print(filename)

    # save a file with the matching search results
    # which can be used with --download
    if args.save_search:
        with open(
            args.save_search, mode="wt", encoding="utf-8"
        ) as search_record:
            search_record.write("\n".join(matching_files))

    # Let user know subdirectories.These are not saved to file
    # as long as user is careful with wildcard usage
    if args.verbose:
        unique_dirs = np.unique(
            np.array(
                [os.path.dirname(datadir) for datadir in filelist], dtype=str
            )
        )
        for dir in sorted(unique_dirs):
            print("Subdirectories are: {}".format(dir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser = add_arguments(parser)
    args = parser.parse_args()
    if args.verbose:
        for arg in vars(args):
            print("{}, {}".format(arg, getattr(args, arg)))
    main(args)
