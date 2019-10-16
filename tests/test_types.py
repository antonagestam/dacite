from enum import Enum, IntEnum
from typing import Any, Collection, Dict, Generic, List, NewType, Optional, TypeVar, Union

import pytest

from dacite.types import (
    extract_generic,
    extract_new_type,
    extract_optional,
    extract_origin_collection,
    is_generic,
    is_generic_collection,
    is_instance,
    is_new_type,
    is_optional,
    is_union,
    transform_value,
    is_enum,
)


def test_is_union_with_union():
    assert is_union(Union[int, float])


def test_is_union_with_non_union():
    assert not is_union(int)


def test_is_optional_with_optional():
    assert is_optional(Optional[int])


def test_is_optional_with_non_optional():
    assert not is_optional(int)


def test_is_optional_with_optional_of_union():
    assert is_optional(Optional[Union[int, float]])


def test_extract_optional():
    assert extract_optional(Optional[int]) == int


def test_extract_optional_with_wrong_type():
    with pytest.raises(ValueError):
        extract_optional(List[None])


def test_is_generic_with_generic():
    assert is_generic(Optional[int])


def test_is_generic_with_non_generic():
    assert not is_generic(int)


def test_is_generic_collection_with_generic_collection():
    assert is_generic_collection(List[int])


def test_is_generic_collection_with_non_generic_collection():
    assert not is_generic_collection(list)


def test_is_generic_collection_with_union():
    assert not is_generic_collection(Union[int, str])


def test_extract_generic_collection():
    assert extract_origin_collection(List[int]) == list


def test_is_new_type_with_new_type():
    assert is_new_type(NewType("NewType", int))


def test_is_new_type_with_non_new_type():
    assert not is_new_type(int)


def test_extract_new_type():
    assert extract_new_type(NewType("NewType", int)) == int


def test_is_instance_with_built_in_type_and_matching_value_type():
    assert is_instance(1, int)


def test_is_instance_with_built_in_type_and_not_matching_value_type():
    assert not is_instance("test", int)


def test_is_instance_with_union_and_matching_value_type():
    assert is_instance(1, Union[int, float])


def test_is_instance_with_union_and_not_matching_value_type():
    assert not is_instance("test", Union[int, float])


def test_is_instance_with_generic_collection_and_matching_value_type():
    assert is_instance([1], List[int])


def test_is_instance_with_generic_abstract_collection_and_matching_value_type():
    assert is_instance([1], Collection[int])


def test_is_instance_with_generic_collection_and_not_matching_value_type():
    assert not is_instance({1}, List[int])


def test_is_instance_with_any_type():
    assert is_instance(1, Any)


def test_is_instance_with_new_type_and_matching_value_type():
    assert is_instance("test", NewType("MyStr", str))


def test_is_instance_with_new_type_and_not_matching_value_type():
    assert not is_instance(1, NewType("MyStr", str))


def test_is_instance_with_not_supported_generic_types():
    T = TypeVar("T")

    class X(Generic[T]):
        pass

    assert not is_instance(X[str](), X[str])


def test_extract_generic():
    assert extract_generic(List[int]) == (int,)


def test_transform_value_without_matching_type():
    assert transform_value({}, str, 1) == 1


def test_transform_value_with_matching_type():
    assert transform_value({int: lambda x: x + 1}, int, 1) == 2


def test_transform_value_with_optional_and_not_none_value():
    assert transform_value({str: str}, Optional[str], 1) == "1"


def test_transform_value_with_optional_and_none_value():
    assert transform_value({str: str}, Optional[str], None) is None


def test_transform_value_with_optional_and_exact_matching_type():
    assert transform_value({Optional[str]: str}, Optional[str], None) == "None"


def test_transform_value_with_generic_sequence_and_matching_item():
    assert transform_value({str: str}, List[str], [1]) == ["1"]


def test_transform_value_with_generic_sequence_and_matching_sequence():
    assert transform_value({List[int]: lambda x: list(reversed(x))}, List[int], [1, 2]) == [2, 1]


def test_transform_value_with_generic_sequence_and_matching_both_item_and_sequence():
    assert transform_value({List[int]: lambda x: list(reversed(x)), int: int}, List[int], ["1", "2"]) == [2, 1]


def test_transform_value_without_matching_generic_sequence():
    assert transform_value({}, List[int], {1}) == {1}


def test_transform_value_with_nested_generic_sequence():
    assert transform_value({str: str}, List[List[str]], [[1]]) == [["1"]]


def test_transform_value_with_generic_abstract_collection():
    assert transform_value({str: str}, Collection[str], [1]) == ["1"]


def test_transform_value_with_generic_mapping():
    assert transform_value({str: str, int: int}, Dict[str, int], {1: "2"}) == {"1": 2}


def test_transform_value_with_nested_generic_mapping():
    assert transform_value({str: str, int: int}, Dict[str, Dict[str, int]], {1: {2: "3"}}) == {"1": {"2": 3}}


def test_transform_value_with_new_type():
    MyStr = NewType("MyStr", str)

    assert transform_value({MyStr: str.upper, str: str.lower}, MyStr, "Test") == "TEST"


def test_transform_value_with_enum():
    class A(Enum):
        B = "B"

    assert transform_value({}, A, "B") == A.B


def test_transform_invalid_enum_value_raises():
    class A(Enum):
        B = "B"

    with pytest.raises(ValueError):
        transform_value({}, A, "C")


def test_is_enum_detects_simple_enum():
    class P(Enum):
        Q = "R"

    assert is_enum(P)


def test_is_enum_detects_int_enum():
    class S(IntEnum):
        T = 1

    assert is_enum(S)


def test_is_enum_can_test_non_class_type():
    assert not is_enum(Union)
