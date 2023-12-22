#!/usr/bin/env python3


from plants.typing import (
    ImmutableJsonArray,
    ImmutableJsonObject,
    MutableJsonArray,
    MutableJsonObject,
    as_json_array,
    as_json_object,
)


def take_immutable_json_array(value: ImmutableJsonArray) -> None:
    pass


def take_immutable_json_object(value: ImmutableJsonObject) -> None:
    pass


def take_mutable_json_array(value: MutableJsonArray) -> None:
    pass


def take_mutable_json_object(value: MutableJsonObject) -> None:
    pass


def check() -> None:
    # This is not a unit test. This method exists soley for Pyre to analyze.

    # Pyre does not infer the type of nested JSON to be wide enough, and thus
    # the inferred type only works with code that promises not to mutate it.
    # The "as" methods provide a convenient way to convert between the
    # Pyre-inferred type and the wide, mutable type.

    val1 = ["a", {"b": None}]
    take_immutable_json_array(val1)
    take_mutable_json_array(val1)  # pyre-ignore[6]
    take_mutable_json_array(as_json_array(val1))

    val2 = {"a": 123, "b": [None]}
    take_immutable_json_object(val2)
    take_mutable_json_object(val2)  # pyre-ignore[6]
    take_mutable_json_object(as_json_object(val2))
