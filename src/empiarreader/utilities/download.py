"""Download a list of files from EMPIAR via FTP or HTTP
empiarreader download
--download my_search.txt --save_dir EMPIAR_files --verbose
"""

# NOTE: There's a bunch of better ways to grab (potentially
# multiple) files (at once) via ftp with fpath globbing via
# curl (and/or) wget. Refactor when time

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
    # try using wget to grab a file via ftp link
    # else try curl to grab a file via ftp link
    # else download files from a textfile list via urllib
    with open(args.download, mode="r", encoding="utf-8") as download_files:
        for filename in download_files:
            try_again = True
            # get a version of filename for ftpserver instead of https
            ftp_link = filename.replace("https://", "ftp://")
            if args.verbose:
                print("Trying ftp download via wget of: {}\n".format(ftp_link))
            wget_command = "wget --directory-prefix {} {}".format(
                args.save_dir,
                ftp_link,
            )
            if os.system(wget_command) == 0:
                try_again = False

            if try_again:
                if args.verbose:
                    print(
                        "Trying ftp download via curl of: {}\n".format(
                            ftp_link
                        )
                    )
                curl_command = "curl -O --output-dir {} {}".format(
                    args.save_dir,
                    ftp_link,
                )
                if os.system(curl_command) == 0:
                    try_again = False

            if try_again:
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
