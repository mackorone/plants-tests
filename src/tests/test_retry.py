#!/usr/bin/env python3

from unittest import IsolatedAsyncioTestCase, mock

from plants.retry import retry
from plants.unittest_utils import UnittestUtils


class MyException(Exception):
    pass


class TestExternal(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # Patch the logger to suppress log spew
        self.mock_logger = UnittestUtils.patch(
            self,
            "plants.retry.logger",
            new_callable=mock.Mock,
        )
        self.mock_sleep = UnittestUtils.patch(
            self,
            "plants.retry.sleep",
            new_callable=mock.AsyncMock,
        )

    async def test_failure(self) -> None:
        my_method = mock.AsyncMock()
        my_method.side_effect = MyException
        with self.assertRaises(MyException):
            with retry(my_method, num_attempts=3, sleep_seconds=1.1) as func:
                await func()
        self.mock_sleep.assert_has_calls([mock.call(1.1)] * 2)

    async def test_success_on_first_attempt(self) -> None:
        my_method = mock.AsyncMock()
        my_method.return_value = None
        with retry(my_method, num_attempts=3, sleep_seconds=1) as func:
            await func()
        self.mock_sleep.assert_not_called()

    async def test_success_on_third_attempt(self) -> None:
        my_method = mock.AsyncMock()
        my_method.side_effect = UnittestUtils.side_effect(
            [
                MyException(),
                MyException(),
                None,
            ]
        )
        with retry(my_method, num_attempts=3, sleep_seconds=1.1) as func:
            await func()
        self.mock_sleep.assert_has_calls([mock.call(1.1)] * 2)
