#! /usr/bin/env python

from __future__ import absolute_import, print_function

import os
import re
import sys
import time

from requests.exceptions import Timeout
from TwitterAPI import TwitterAPI

###
from pprint import pprint
###

# Update this to Python 3 to get away from unicode problems


USAGE = """
Usage: python snitchbot.py PYTHON_FILE

Example: python snitchbot.py really_secret_document.py

Notes: This fully supports processing Python files only.
"""


def exit(message=None, usage=True):
    """Gracefully exits the script.

    @param   message: The comments to be posted to the Twitter service.
    @type    message: str, else None
    @param:  usage: A message on the usage of the tool.
    @type:   usage: boolean
    """
    if message:
        print("ERROR: {}\n".format(message))
    if usage:
        print(USAGE)
    sys.exit(1)


def main(fname):
    """Opens a Python file as command-line argument and runs the process.

    @param   fname: The command-line arguments ran with this script.
    @type    fname: list of str
    """
    if not fname.endswith(".py"):
        exit("Not a python file.")
    elif not os.path.isfile(fname):
        exit("File does not exist.")
    else:
        with open(fname) as f:
            account = TwitterAPI(consumer_key=consumer_key
                                 consumer_secret=consumer_secret,
                                 access_token_key=access_token_key,
                                 access_token_secret=access_token_secret)

            updater = TwitterUpdater(account)
            comments = updater.process_comments(f.readlines())
            posted = updater.post_comments(comments)


class TwitterUpdater(object)

    self._TIMEOUT_LIMIT = 60 * 5  # 5 minutes

    self._TWITTER_LIMIT = 36      # 36 seconds

    # The following HTTP codes require special handling

    self._UNAUTHORIZED_STATUS_CODES = [400, 401]

    self._WAIT_STATUS_CODES = [420, 429, 502, 503, 504]

    def __init__(self, account):
        self._account = account

    def post_comments(comments):
        """Authenticates and updates the status with the aggregated comments.

        @param   comments: The comments to be posted to the Twitter service.
        @type    comments: list of str
        @return: True if successful
        @rtype:  bool
        """
        for comment in comments:
            while True:
                try:
                # Only uncomment when ready
                # response = _update_status(comment)
                status = response.status_code
                if status == 200:
                    break
                elif status in self._UNAUTHORIZED_STATUS_CODES:
                    exit("Unauthorized to update status. Check your Twitter "
                         "credentials.")
                elif status == self._WAIT_STATUS_CODES:
                    print("Twitter encountered a problem. Trying again a"
                          "little later.")
                    time.sleep(self._TIMEOUT_LIMIT)
            except TwitterAPI.TwitterError.TwitterConnectionError(value):
                pass
            except TwitterAPI.TwitterError.TwitterRequestError(status_code):
                pass
            except TwitterAPI.TwitterError.TwitterError:
                pass
            except Timeout:
                time.sleep(self._TIMEOUT_LIMIT)

    def process_comments(content):
        """Collects all comments in the read Python module.

        @param   content: The contents of a Python module.
        @type    content: list of str
        @return: Only the lines that denote comments.
        @rtype:  list of str
        """
        # Match all hashes followed by a character. If it is an !, don't match.
        # Filter the string down (only remove whitespace afterwards).
        comment_matcher = re.compile(r'^#+[^\!]_*?')
        comment_filter = re.compile(r'^#+[^ ]*?')
        max_comment_length = 140
        comments = []

        for line in content:
            if re.match(comment_matcher, line):
                comment = re.sub(comment_filter, "", line)\
                            .lstrip(" ")\
                            .rstrip("")
                if len(comment) > max_comment_length:
                    print("Processed comment is too long. Truncating comment.")
                    comments.append(comment[:140])
                else:
                    comments.append(comment)
        if not comments:
            exit("No comments found to post.")

        return comments

    def _update_status(comment):
        response = self._account.request("statuses/update",
                                         {"status": comment})
        time.sleep(TWITTER_LIMIT)

        return response


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        exit("Must send in a Python file.", usage=True)
    main(fname=args[1])
