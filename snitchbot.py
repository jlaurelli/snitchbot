#! /usr/bin/env python

from __future__ import absolute_import, print_function

import argparse
import os
import re
import sys

import twitter

from keys import (ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY,
                  CONSUMER_SECRET)

###
from pprint import pprint
###


USAGE = """
Usage: python snitchbot.py PYTHON_FILE

Example: python snitchbot.py really_secret_document.py

Notes: This fully supports reading Python files only.
"""


def post_comments(comments):
    """
    Authenticates and updates the status with the aggregated comments.

    @param   comments: The comments to be posted to the Twitter service.
    @type    comments: list of str
    @return: True if successful, False if not.
    @rtype:  bool
    """
    acct = twitter.Api(consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token_key=ACCESS_TOKEN_KEY,
                       access_token_secret=ACCESS_TOKEN_SECRET)
    try: 
        acct.VerifyCredentials()

        pprint(acct.GetRateLimitStatus())

        # Rate limit is 15 updates per 15 minutes

        if len(comments) > acct.GetRateLimitStatus()["remaining_hits"]:
            print("ERROR: File will break the rate limit. Try again later.")
            return False
        for comment in comments:
            # Only un-comment when ready
            # acct.PostUpdates(message)
            pass
    except twitter.error.TwitterError as exc:
        print("ERROR: {}".format(exc["message"]))
        return False
    finally:
        acct.ClearCredentials()

    return True


def process_comments(content):
    """
    Collects all comments in the read Python module.

    @param   content: The contents of a Python module.
    @type    content: list of str
    @return: Only the lines that denote comments.
    @rtype:  list of str
    """
    # Match all hashes followed by a character.  If it is an !, don't match.
    # Filter the string down (only remove whitespace afterwards).
    RE_MATCH = r'^#+[^\!]_*?'
    RE_FILTER = r'^#+[^ ]*?'
    COMMENT_MATCHER = re.compile(RE_MATCH, re.MULTILINE)
    COMMENT_FILTER = re.compile(RE_FILTER)
    comments = []

    # TODO: Needs to handle lines that could be greater than 140 characters.
    # ADDENDUM: api.PostUpdates() already splits up messages that are longer
    # than 140 characters

    for line in content:
        if re.match(COMMENT_MATCHER, line):
            # Match and strip:
            #   - whitespace before the string (but not metacharacters)
            #   - whitespace after the string
            #   - ignore docstrings
            #   ? Combine consecutive lines if no blank spaces?
            # Otherwise, just use .strip()
            comment = re.sub(COMMENT_FILTER, "", line)\
                        .lstrip(" ")\
                        .rstrip("")
            # comment = line.lstrip(' ').rstrip()
            comments.append(comment)

    return comments


def main(argv):
    """
    Takes a Python file as command-line argument and starts the entire process.

    @param   argv: The command-line arguments ran with this script.
    @type    argv: list of str
    """
    argv_len = len(argv)
    if argv_len < 2 or not argv[1].endswith(".py"):
        sys.exit("ERROR: Did not supply a Python module.\n" + USAGE)
    elif argv_len > 2:
        print("WARNING: More than one argument supplied. Ignoring all extra"
              "arguments.\n")

    fname = argv[1]
    with open(fname) as f:
        comments = process_comments(f.readlines())
        posted = post_comments(comments)
        # assert(type(posted) == bool, "Pushing comments encountered errors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    main(argv=sys.argv)
