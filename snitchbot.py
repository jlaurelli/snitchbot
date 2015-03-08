#! /usr/bin/env python3

"""Starts the SnitchBot script."""

import os
import sys

from snitch_helpers import snitch_exit, setup_twitter
from twitter_updater import TwitterUpdater


def main(fname):
    """Opens a Python file as command-line argument and runs the process.

    @param   fname: The command-line arguments ran with this script.
    @type    fname: list[str]
    """
    if not fname.endswith(".py"):
        snitch_exit("Not a python file.")
    elif not os.path.isfile(fname):
        snitch_exit("File does not exist.")
    else:
        with open(fname) as f:
            # Get the required twitter credentials and run
            account = setup_twitter()
            updater = TwitterUpdater(account)
            comments = updater.process_comments(f.readlines())
            posted = updater.post_comments(comments)


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        snitch_exit("Must send in a Python file.", usage=True)
    main(fname=args[1])
