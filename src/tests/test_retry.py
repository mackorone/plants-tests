#!/usr/bin/env python3

from unittest import IsolatedAsyncioTestCase, mock

from plants.retry import AttemptFactory, retry
from plants.unittest_utils import UnittestUtils


class MyException(Exception):
    pass


class TestRetry(IsolatedAsyncioTestCase):
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
        my_method.assert_has_calls([mock.call(), mock.call(), mock.call()])
        self.mock_sleep.assert_has_calls([mock.call(1.1), mock.call(1.1)])

    async def test_success_on_first_attempt(self) -> None:
        my_method = mock.AsyncMock()
        my_method.return_value = None
        with retry(my_method, num_attempts=3, sleep_seconds=1) as func:
            await func()
        my_method.assert_called_once_with()
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
        my_method.assert_has_calls([mock.call(), mock.call(), mock.call()])
        self.mock_sleep.assert_has_calls([mock.call(1.1), mock.call(1.1)])


class TestAttemptFactory(IsolatedAsyncioTestCase):
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
            for attempt in AttemptFactory(num_attempts=3, sleep_seconds=1.1):
                async with attempt:
                    await my_method()
        my_method.assert_has_calls([mock.call(), mock.call(), mock.call()])
        self.mock_sleep.assert_has_calls([mock.call(1.1), mock.call(1.1)])

    async def test_success_on_first_attempt(self) -> None:
        my_method = mock.AsyncMock()
        my_method.return_value = None
        for attempt in AttemptFactory(num_attempts=3, sleep_seconds=1):
            async with attempt:
                await my_method()
        my_method.assert_called_once_with()
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
        for attempt in AttemptFactory(num_attempts=3, sleep_seconds=1.1):
            async with attempt:
                await my_method()
        my_method.assert_has_calls([mock.call(), mock.call(), mock.call()])
        self.mock_sleep.assert_has_calls([mock.call(1.1), mock.call(1.1)])
