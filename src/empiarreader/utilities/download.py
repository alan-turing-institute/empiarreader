"""_summary_
empiarreader download  --download my_search.txt --save_dir empiarreader_testing --verbose
"""

import os
import argparse

import urllib

def add_arguments(parser):
    # for searching EMPIAR
    parser.add_argument(
        "--download",
        help=(
            "Provide file path the newline separated files to download"
        ),
        type=str,
        default=None,
        required=True,
    )
    parser.add_argument(
        "--save_dir",
        help=(
            "Directory to store downloaded data in."
            " Defaults to /tmp"
        ),
        type=str,
        default="/tmp",
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
    return "download"


def main(args):
    """
    """
    # download files from a textfile list via urllib
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
                    os.path.join(
                        args.save_dir,
                        os.path.basename(filename.rstrip())
                    )
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
