#!/usr/bin/env python3

from unittest import IsolatedAsyncioTestCase

from plants.external import InvalidExternalCallError, external


@external
def my_module_method() -> None:
    pass


@external
async def my_async_module_method() -> None:
    pass


class TestExternal(IsolatedAsyncioTestCase):
    @external
    def my_instance_method(self) -> None:
        pass

    @external
    async def my_async_instance_method(self) -> None:
        pass

    @classmethod
    @external
    def my_class_method(cls) -> None:
        pass

    @classmethod
    @external
    async def my_async_class_method(cls) -> None:
        pass

    @staticmethod
    @external
    def my_static_method() -> None:
        pass

    @staticmethod
    @external
    async def my_async_static_method() -> None:
        pass

    def test_module_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            my_module_method()

    async def test_async_module_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            await my_async_module_method()

    def test_instance_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            self.my_instance_method()

    async def test_async_instance_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            await self.my_async_instance_method()

    def test_class_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            self.my_class_method()

    async def test_async_class_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            await self.my_async_class_method()

    def test_static_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            self.my_static_method()

    async def test_async_static_method(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            await self.my_async_static_method()

    def test_try_catch(self) -> None:
        with self.assertRaises(InvalidExternalCallError):
            try:
                external(lambda: None)()
            except Exception:
                pass
