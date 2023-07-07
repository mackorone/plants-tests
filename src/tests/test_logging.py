#!/usr/bin/env python3

import logging
from unittest import IsolatedAsyncioTestCase

from plants.logging import Color, LogFormatter


class TestFormat(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._record = logging.LogRecord(
            name="logger_name",
            level=logging.INFO,
            pathname="foo.bar",
            lineno=101,
            msg="one\ntwo\nthree",
            args=None,
            exc_info=None,
        )

    def test_no_colors(self) -> None:
        formatter = LogFormatter(
            colorize=False, escape_newlines=False, auto_indent=False
        )
        content = formatter.format(self._record)
        self.assertTrue(content.endswith("[INFO] one\ntwo\nthree"))

    def test_escape_newlines(self) -> None:
        formatter = LogFormatter(
            colorize=False, escape_newlines=True, auto_indent=False
        )
        content = formatter.format(self._record)
        self.assertTrue(content.endswith("[INFO] one\\ntwo\\nthree"))

    def test_success(self) -> None:
        formatter = LogFormatter(
            colorize=True, escape_newlines=False, auto_indent=False
        )
        content = formatter.format(self._record)
        self.assertTrue(content.endswith("\u001b[92m[INFO]\u001b[0m one\ntwo\nthree"))


class TestGetLevelColor(IsolatedAsyncioTestCase):
    def test_debug(self) -> None:
        self.assertEqual(
            LogFormatter._get_level_color(logging.DEBUG),
            Color.TURQUOISE,
        )

    def test_info(self) -> None:
        self.assertEqual(
            LogFormatter._get_level_color(logging.INFO),
            Color.LIGHT_GREEN,
        )

    def test_warning(self) -> None:
        self.assertEqual(
            LogFormatter._get_level_color(logging.WARNING),
            Color.LIGHT_YELLOW,
        )

    def test_error(self) -> None:
        self.assertEqual(
            LogFormatter._get_level_color(logging.ERROR),
            Color.LIGHT_RED,
        )

    def test_critical(self) -> None:
        self.assertEqual(
            LogFormatter._get_level_color(logging.CRITICAL),
            Color.LIGHT_PURPLE,
        )
