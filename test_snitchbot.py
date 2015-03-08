#! /usr/bin/env python3

"""The SnitchBot unit tests."""

import logging
import sys
import unittest
from unittest.mock import patch

from TwitterAPI.TwitterError import TwitterConnectionError

import snitchbot
from snitch_helpers import snitch_exit, setup_twitter
from twitter_updater import TwitterUpdater


# Disable external logging
logging.disable(logging.FATAL)


class SnitchExitTests(unittest.TestCase):
    
    def test_snitch_exit(self):
        with self.assertRaises(SystemExit) as err:
            snitch_exit()
        self.assertEqual(err.exception.code, 1)


class PostCommentsTests(unittest.TestCase):

    @patch("twitter_updater.TwitterUpdater.update_status", return_value=200)
    def test_post_comments(self, mock_update):
        updater = TwitterUpdater("fake_account")
        posted = updater.post_comments(["test_comment"])
        self.assertEqual(posted, True)

    @patch("twitter_updater.snitch_exit")
    @patch("twitter_updater.TwitterUpdater.update_status", return_value=400)
    def test_post_comments(self, mock_update, mock_exit):
        updater = TwitterUpdater("fake_account")
        posted = updater.post_comments(["test_comment"])
        mock_exit.assert_called_with("Unauthorized to update status. Check "
                                     "your Twitter credentials.")

    @patch("twitter_updater.snitch_exit")
    @patch("twitter_updater.TwitterUpdater.sleep")
    @patch("twitter_updater.TwitterUpdater.update_status", return_value=420)
    def test_post_comments(self, mock_update, mock_sleep, mock_exit):
        updater = TwitterUpdater("fake_account")
        posted = updater.post_comments(["test_comment"])
        mock_sleep.assert_called_with()

    @patch("twitter_updater.snitch_exit")
    @patch("twitter_updater.TwitterUpdater.update_status", return_value=302)
    def test_post_comments(self, mock_update, mock_exit):
        updater = TwitterUpdater("fake_account")
        posted = updater.post_comments(["test_comment"])
        mock_exit.assert_called_with("Failed to post all comments.")

    @patch("twitter_updater.snitch_exit")
    @patch("twitter_updater.TwitterUpdater.update_status",
           side_effect=TwitterConnectionError("mock_value"))
    def test_post_comments__TwitterConnectionError(self, mock_update, mock_exit):
        updater = TwitterUpdater("fake_account")
        posted = updater.post_comments(["test_comment"])
        mock_exit.assert_called_with("Failed to post all comments.")


class ProcessCommentsTests(unittest.TestCase):

    def test_process_comments(self):
        updater = TwitterUpdater("fake_account")

        def _check_comments(comment, expected, raise_error=False):
            if raise_error:
                with self.assertRaises(SystemExit) as err:
                    self.assertEqual(updater.process_comments(comment),
                                     expected)
            else:
                self.assertEqual(updater.process_comments(comment), expected)

        _check_comments(["# Basic line"], ["Basic line"])
        _check_comments(["#! Script syntax"], [], raise_error=True)
        _check_comments(["#No preceding whitespace"],
                        ["No preceding whitespace"])
        _check_comments(["#### Multiple hashes"], ["Multiple hashes"])
        _check_comments(["#     Proceeding whitespace"],
                        ["Proceeding whitespace"])
        _check_comments(["# \n Newline"], ["\n Newline"])
        _check_comments(["# \t Tab"], ["\t Tab"])
        _check_comments(['"""Docstring"""'], [], raise_error=True)


class MainTests(unittest.TestCase):

    @patch("snitchbot.TwitterUpdater.post_comments")
    @patch("snitchbot.TwitterUpdater.process_comments", return_value=True)
    @patch("snitchbot.setup_twitter")
    def test_main(self, mock_setup, mock_process, mock_post):
        snitchbot.main("test_data.py")
        mock_setup.assert_called_with()
        mock_process.assert_called_with(['# "Just a valid test file"\n'])
        mock_post.assert_called_with(True)

    @patch("snitchbot.snitch_exit")
    def test_main__not_Python_module(self, mock_exit):
        snitchbot.main("not_a_python_module.txt")
        mock_exit.assert_called_with("Not a python file.")

    @patch("snitchbot.snitch_exit")
    def test_main__no_file(self, mock_exit):
        snitchbot.main("")
        mock_exit.assert_called_with("Not a python file.")

    @patch("snitchbot.snitch_exit")
    def test_main__not_exist(self, mock_exit):
        snitchbot.main("invalid_python_module.py")
        mock_exit.assert_called_with("File does not exist.")


if __name__ == "__main__":
    unittest.main(buffer=True)
