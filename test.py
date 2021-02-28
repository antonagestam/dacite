from dataclasses import dataclass
from typing import Annotated

from dacite import from_dict
from dacite.rewrites import From, Composite, FromField, CompositeField


@dataclass(frozen=True)
class A:
    type_: Annotated[int, From["type"]]


a = from_dict(A, {"type": 123})
assert a == A(type_=123)
print(f"{a=}")


@dataclass(frozen=True)
class B:
    price: Annotated[tuple[float, str], Composite["amount", "currency"]]


b = from_dict(B, {"amount": 100.00, "currency": "SEK"})
print(f"{b=}")
assert b == B(price=(100.00, "SEK"))


@dataclass(frozen=True)
class C:
    type_: int = FromField("type")  # type: ignore[assignment]


c = from_dict(C, {"type": 123})
assert c == C(type_=123)
print(f"{c=}")


@dataclass(frozen=True)
class D:
    price: tuple[float, str] = CompositeField("amount", "currency")  # type: ignore[assignment]


d = from_dict(D, {"amount": 1000.00, "currency": "NOK"})
assert d == D(price=(1000.00, "NOK"))
print(f"{d=}")
