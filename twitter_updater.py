"""The definition of the TwitterUpdater class."""

import re
import time

from requests.exceptions import Timeout


class TwitterUpdater(object):

    _TIMEOUT_LIMIT = 60 * 5  # 5 minutes

    _UPDATE_LIMIT = 36      # 36 seconds

    # The following HTTP codes require special handling

    _UNAUTHORIZED_STATUS_CODES = [400, 401]

    _WAIT_STATUS_CODES = [420, 429, 502, 503, 504]

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
            pass
            # while True:
            #     try:
            #     # Only uncomment when ready
            #     # response = _update_status(comment)
            #     status = response.status_code
            #     if status == 200:
            #         break
            #     elif status in self._UNAUTHORIZED_STATUS_CODES:
            #         exit("Unauthorized to update status. Check your Twitter "
            #              "credentials.")
            #     elif status == self._WAIT_STATUS_CODES:
            #         print("Twitter encountered a problem. Trying again a"
            #               "little later.")
            #         time.sleep(self._TIMEOUT_LIMIT)
            # except TwitterAPI.TwitterError.TwitterConnectionError(value):
            #     pass
            # except TwitterAPI.TwitterError.TwitterRequestError(status_code):
            #     pass
            # except TwitterAPI.TwitterError.TwitterError:
            #     pass
            # except Timeout:
            #     time.sleep(self._TIMEOUT_LIMIT)

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
            exit("No comments found to post.", is_warn=True)

        return comments

    def _update_status(self, comment):
        response = self._account.request("statuses/update",
                                         {"status": comment})
        time.sleep(_UPDATE_LIMIT)

        return response
