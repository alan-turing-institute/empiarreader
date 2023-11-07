"""Download a list of files from EMPIAR via FTP or HTTP
empiarreader download
--download my_search.txt --save_dir EMPIAR_files --verbose
"""

import os
import argparse

import urllib


def add_arguments(parser):
    """Set out the arguments for the download utility

    Args:
        parser (argparse.ArgumentParser): argument parser

    Returns:
        argparse.ArgumentParser: argument parser
    """
    parser.add_argument(
        "--download",
        help="Provide file path the newline separated files to download",
        type=str,
        default=None,
        required=True,
    )
    parser.add_argument(
        "--save_dir",
        help="Directory to store downloaded data in",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--verbose",
        help="Increase verbosity to stdout",
        action="store_true",
        required=False,
    )

    return parser


def get_name():
    """Name the download utility

    Returns:
        str: utility name
    """
    return "download"


def main(args):
    """Download EMPIAR files from a list of HTTPS paths in a text file

    Args:
        args (argparse.ArgumentParser): argument parser with parsed args
    """
    if not os.path.isdir(args.save_dir):
        os.makedirs(args.save_dir)
        if args.verbose:
            print("Created save_dir: {}".format(args.save_dir))
    # download files from a textfile list via urllib
    with open(args.download, mode="r", encoding="utf-8") as download_files:
        for filename in download_files:
            try:
                if args.verbose:
                    print("Downloading {}".format(filename.rstrip()))
                urllib.request.urlretrieve(
                    filename.rstrip(),
                    os.path.join(
                        args.save_dir, os.path.basename(filename.rstrip())
                    ),
                )
            except (urllib.error.URLError, IOError) as url_err:
                print(url_err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser = add_arguments(parser)
    args = parser.parse_args()
    if args.verbose:
        for arg in vars(args):
            print("{}, {}".format(arg, getattr(args, arg)))
    main(args)
