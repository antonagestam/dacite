from __future__ import annotations
from dataclasses import Field
from typing import Final

from dacite.data import Data


class _FromMarker:
    def __init__(self, source: str) -> None:
        self.source = source

    def __repr__(self) -> str:
        return f"<_FromMarker source={self.source!r}>"

    def rewrite(self, data: Data) -> object:
        return data[self.source]


class _FromFactory:
    def __getitem__(self, source: str) -> _FromMarker:
        return _FromMarker(source)


From: Final = _FromFactory()
del _FromFactory


class _CompositeMarker:
    def __init__(self, *sources: str) -> None:
        self.sources = sources

    def __repr__(self) -> str:
        return f"<_CompositeMarker sources={self.sources!r}>"

    def rewrite(self, data: Data) -> tuple[object, ...]:
        return tuple(data[source] for source in self.sources)


class _CompositeFactory:
    def __getitem__(self, sources: tuple[str]) -> _CompositeMarker:
        return _CompositeMarker(*sources)


Composite: Final = _CompositeFactory()
del _CompositeFactory


def extract(annotated: type) -> _FromMarker | _CompositeMarker:
    item, = annotated.__metadata__
    assert isinstance(item, (_FromMarker, _CompositeMarker))
    return item


def rewrite(annotated: type, field: Field, data: Data) -> object:
    if annotated == field.type:
        return data[field.name]
    marker = extract(annotated)
    return marker.rewrite(data)
