"""
"""

import sys
import unittest
import StringIO

# import twitter

import snitchbot
import test_data

from pprint import pprint


# Add the test data file to the command-line list
SYS_ARGS = ["snitch_tests.py", "test_data"]


class SnitchBotTests(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    # def _setup_file(self, content):
    #     self.content = cStringIO.StringIO()
    #     self.content.write(content)

    def test_comment_strings(self):
        self.assertEqual(
            snitchbot.process_comments(["# Basic line"]),
            ["Basic line"])
        self.assertEqual(
            snitchbot.process_comments(["#! Script syntax"]),
            [])
        self.assertEqual(
            snitchbot.process_comments(["#No preceding whitespace"]),
            ["No preceding whitespace"])
        self.assertEqual(snitchbot.process_comments(["#### Multiple hash"]),
            ["Multiple hash"])
        self.assertEqual(
            snitchbot.process_comments(["#     Proceeding whitespace"]),
            ["Proceeding whitespace"])
        self.assertEqual(
            snitchbot.process_comments(["# \n Newline"]),
            ["\n Newline"])
        self.assertEqual(
            snitchbot.process_comments(["# \t Tab"]),
            ["\t Tab"])
        self.assertEqual(
            snitchbot.process_comments(['"""Docstring"""']),
            [])

    def test_main__not_python_module(self):
        with self.assertRaises(SystemExit) as error:
            snitchbot.main(["not_a_python_module.txt"])
        self.assertEqual(error.exception.code, 1)

    def test_main__no_file(self):
        with self.assertRaises(SystemExit) as error:
            snitchbot.main([])
        self.assertEqual(error.exception.code, 1)



if __name__ == "__main__":
    unittest.main()
