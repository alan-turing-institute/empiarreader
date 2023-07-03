"""_summary_
"""

import os
import argparse

import numpy as np

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

    return parser


def get_name():
    return "search"


def main(args):
    """
    """
    ds = EmpiarSource(
        args.entry,
        directory=args.dir,
        filename=args.select,
        regexp=args.regexp,
    )
    filelist = ds._parse_data_dir(ds.data_directory_url)
    print(filelist)
    matching_files = [
            url for url in filelist if ds.image_url_regexp.match(url)
        ]
    for filename in sorted(matching_files):
        print("{}".format(filename))
    
    # save a file with the matching search results
    # which can be used with --download
    if args.save_search:
        with open(
            args.save_search,
            mode="wt",
            encoding="utf-8"
        ) as search_record:
            search_record.write()
    
    # Let user know subdirectories.These are not saved to file
    # as long as user is careful with wildcard usage
    if args.verbose:
        unique_dirs = np.unique(
            np.array(
                [os.path.dirname(datadir) for datadir in filelist],
                dtype=str
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
