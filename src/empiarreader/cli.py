"""CLI for empiarreader
"""

import os
import argparse
import sys
from typing import List, Dict

import numpy as np
import urllib

from empiarreader.empiar.empiar import EmpiarSource

def arg_setup(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
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
        help="Wildcard path to select file(s) or directory within entry",
        type=str,
        default="*",
        required=False,
    )

    parser.add_argument(
        "--regexp",
        help=(
            "Whether 'select' is regex-style instead of bash-style."
            "Defaults to bash-style"
        ),
        action="store_true",
        required=False,
    )
    # NOTE NOT IMPLEMENTED
    parser.add_argument(
        "--persistent",
        help="Whether to store downloaded data to disk",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--cache_dir",
        help=(
            "Directory to store downloaded data in"
            "If 'persistent' arg supplied and 'cache dir' not supplied,"
            "data is stored in default cache dir"
        ),
        type=str,
        default="/tmp",
        required=False,
    )

    parser.add_argument(
        "--search",
        help="Print what is in selected EMPIAR directory",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--verbose",
        help="Increase verbosity to stdout",
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
        "--download",
        help=(
            "Provide file path the newline separated files to download"
        ),
        type=str,
        default=None,
        required=False,
    )


def conquer_empiar(args: List) -> None:
    # Search the EMPIAR archive
    if args.select:
        # search EMPIAR instead of download data
        if args.search:
            ds = EmpiarSource(
                args.entry,
                directory=args.dir,
                filename=args.select,
                regexp=args.regexp,
            )
            filelist = ds._parse_data_dir(ds.data_directory_url)
            matching_files = [
                    url for url in filelist if ds.image_url_regexp.match(url)
                ]
            for filename in matching_files:
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
            unique_dirs = np.unique(
                np.array(
                    [os.path.dirname(datadir) for datadir in filelist],
                    dtype=str
                )
            )
            for dir in sorted(unique_dirs):
                print("Subdirectories are: {}".format(dir))
                
        # download some data via intake cache
        else:
            ds = EmpiarSource(
                args.entry,
                directory=args.dir,
                file=args.select,
            )

    # download files from a textfile list via urllib
    if args.download:
        with open(
            args.download,
            mode="r",
            encoding="utf-8"
        ) as download_files:
            for filename in download_files:
                try:
                    if args.verbose:
                        print("Downloading {}".format(filename.rstrip()))
                    urllib.request.urlretrieve(
                        filename.rstrip(),
                        args.cache_dir
                    )
                    filename.strip()
                except (urllib.error.URLError, IOError) as url_err:
                    print(url_err.reason)


def main():
    # parse command line args
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter,
    )
    arg_setup(parser)
    args = parser.parse_args()
    if args.verbose:
        for arg in vars(args):
            print("{}, {}".format(arg, getattr(args, arg)))

    # formulate the data request and grab data via intake
    conquer_empiar(args)
    
if __name__ == "__main__":
    main()
