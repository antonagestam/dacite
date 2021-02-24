from dataclasses import dataclass
from decimal import Decimal
from typing import Annotated, NamedTuple

from dacite import from_dict, Config
from dacite.rewrites import From, Composite


@dataclass(frozen=True)
class A:
    type_: Annotated[int, From["type"]]


inst = from_dict(A, {"type": 123})
assert inst == A(type_=123)
print(f"{inst=}")


@dataclass(frozen=True)
class B:
    price: Annotated[tuple[float, str], Composite["amount", "currency"]]


inst = from_dict(B, {"amount": 100.00, "currency": "SEK"})
print(f"{inst=}")
assert inst == B(price=(100, "SEK"))
