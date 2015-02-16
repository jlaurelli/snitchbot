import mock
import sys
import unittest

import snitchbot
from twitter.error import TwitterError

from pprint import pprint


class ExitCommentsTests(unittest.TestCase):
    
    def test_exit(self):
        with self.assertRaises(SystemExit) as err:
            snitchbot.exit()
        self.assertEqual(err.exception.code, 1)


class PostCommentsTests(unittest.TestCase):

    def test_post_comments(self):
        with mock.patch("twitter.Api") as api:
            posted = snitchbot.post_comments(["test_comment"])
            self.assertEqual(posted, True)

    def test_post_comments__twitter_error(self):
        with mock.patch("twitter.Api.VerifyCredentials", side_effect=TwitterError) as verify:
            posted = snitchbot.post_comments(["test_comment"])
            self.assertEqual(posted, True)


class ProcessCommentsTests(unittest.TestCase):

    def test_comment_strings(self):
        def _check_comments(comment, expected):
            self.assertEqual(snitchbot.process_comments(comment), expected)

        _check_comments(["# Basic line"], ["Basic line"])
        _check_comments(["#! Script syntax"], [])
        _check_comments(["#No preceding whitespace"],
                        ["No preceding whitespace"])
        _check_comments(["#### Multiple hashes"], ["Multiple hashes"])
        _check_comments(["#     Proceeding whitespace"],
                        ["Proceeding whitespace"])
        _check_comments(["# \n Newline"], ["\n Newline"])
        _check_comments(["# \t Tab"], ["\t Tab"])
        _check_comments(['"""Docstring"""'], [])


class MainTests(unittest.TestCase):

    def test_main(self):
        with mock.patch("snitchbot.process_comments", return_value=True) \
        as process, mock.patch("snitchbot.post_comments", return_value=True) \
        as post:
            snitchbot.main("test_data.py")
            process.assert_called_with(['"Just a valid test file"\n'])
            post.assert_called_with(True)

    def test_main__not_Python_module(self):
        with mock.patch("snitchbot.exit", return_value=True) as exit:
            snitchbot.main("not_a_python_module.txt")
            exit.assert_called_with("Not a python file")

    def test_main__no_file(self):
        with mock.patch("snitchbot.exit", return_value=True) as exit:
            snitchbot.main("")
            exit.assert_called_with("Not a python file")

    def test_main__not_exist(self):
        with mock.patch("snitchbot.exit", return_value=True) as exit:
            snitchbot.main("invalid_python_module.py")
            exit.assert_called_with("File does not exist")


if __name__ == "__main__":
    unittest.main(buffer=True)
