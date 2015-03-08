"""A set of helper objects and functions for SnitchBot."""

import sys

from TwitterAPI import TwitterAPI, TwitterOAuth


USAGE = """
Usage: python snitchbot.py PYTHON_FILE
  
Example: python snitchbot.py really_secret_document.py

Notes: This fully supports processing Python files only.
"""


# --- Helper Functions --------------------------------------------------------

def setup_twitter():
    """Prepares a twitter account to use for posting.

    @param   message: A message to display as part of the program exit.
    @type    message: str | None
    @param   is_warn: Print a warning as opposed to an error.
    @type    is_warn: boolean
    @param:  usage: A message on the usage of the tool.
    @type:   usage: boolean
    """
    oauth = TwitterOAuth.read_file("keys.txt")
    account = TwitterAPI(consumer_key=oauth.consumer_key,
                         consumer_secret=oauth.consumer_secret,
                         access_token_key=oauth.access_token_key,
                         access_token_secret=oauth.access_token_secret)

    return account


def snitch_exit(message=None, is_warn=False, usage=False):
    """Gracefully exits the script.

    @param   message: A message to display as part of the program exit.
    @type    message: str | None
    @param   is_warn: Print a warning as opposed to an error.
    @type    is_warn: boolean
    @param:  usage: A message on the usage of the tool.
    @type:   usage: boolean
    """
    if message:
        if is_warn:
            prefix = "WARN: {}\n"
        else:
            prefix = "ERROR: {}\n"
        print(prefix.format(message))
    if usage:
        print(USAGE)
        
    sys.exit(1)
