"""The definition of the TwitterUpdater class."""

import re
import time

from TwitterAPI.TwitterError import TwitterConnectionError

from snitch_helpers import snitch_exit


class TwitterUpdater(object):

    _MAX_ATTEMPTS = 5

    _TIMEOUT_LIMIT = 60 * 5  # 5 minutes

    _UPDATE_LIMIT = 36       # 36 seconds

    # The following HTTP codes require special handling

    _UNAUTHORIZED_STATUS_CODES = [400, 401]

    _WAIT_STATUS_CODES = [420, 429]

    def __init__(self, account):
        """Initializes a new TwitterUpdater object.

        @param   account: The twitter account object to use for posting.
        @type    account: C{TwitterAPI}
        """
        self._account = account

    def post_comments(self, comments):
        """Authenticates and updates the status with the aggregated comments.

        @param   comments: The comments to be posted to the Twitter service.
        @type    comments: list[str]
        @return: True if successful
        @rtype:  bool
        """
        for comment in comments:
            for attempt in range(1, self._MAX_ATTEMPTS + 1):
                try:
                    status = self.update_status(comment)
                except TwitterConnectionError:
                    print("Twitter connection was lost. Attempted {} of {} "
                          "times.".format(attempt, self._MAX_ATTEMPTS))
                    continue

                if status == 200:
                    print("Comment successfully posted!")
                    break
                elif status in self._UNAUTHORIZED_STATUS_CODES:
                    snitch_exit("Unauthorized to update status. Check "
                                "your Twitter credentials.")
                    break
                elif status in self._WAIT_STATUS_CODES:
                    print("Twitter encountered a problem. Retrying a "
                          "little later.")
                    self.sleep()
                    continue
                else:
                    print("Twitter responded with a status code of {}."
                          .format(status))
                    continue
            else:
                snitch_exit("Failed to post all comments.")

        print("All comments successfully posted!")
        return True

    def process_comments(self, content):
        """Collects all comments in the read Python module.

        @param   content: The contents of a Python module.
        @type    content: list[str]
        @return: Only the lines that denote comments.
        @rtype:  list[str]
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
            snitch_exit("No comments found to post.", is_warn=True)

        return comments

    def sleep(self):
        """Sets a longer-than-usual sleep timer after this attempt."""
        time.sleep(self._TIMEOUT_LIMIT)

    def update_status(self, comment):
        """Attempts to update the Twitter account's status.

        @param   comment: The comment to use as status material.
        @type    comment: str
        @return: The status of the attempt.
        @rtype:  int
        @raises TwitterConnectionError: If the connection to Twitter is lost.
        """
        response = self._account.request("statuses/update",
                                         {"status": comment})
        time.sleep(self._UPDATE_LIMIT)

        return response.status_code
