# -*- coding: utf-8 -*-
"""Paging model."""
from typing import Generic, Tuple, TypeVar

import typing as t
from copy import deepcopy
from uuid import uuid4


class Base(dict):
    """Base of all models, inheriting from dict."""

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._generate_default_values()
        self._generate_id(kwargs)
        self._check_required_attributes(kwargs)
        self._get_attributes(kwargs)

    def _generate_default_values(self) -> None:
        """Generate default values from class annotations."""
        for key in tuple(dir(self)):
            if key in self.__annotations__:
                value_default = getattr(self, key)
                self[key] = deepcopy(value_default)

    def _generate_id(self, kwargs: dict) -> None:
        # Create a new id if there's no id.
        if "id" in self.__annotations__:
            kwargs["id"] = kwargs.get("id", str(uuid4()))

    def _check_required_attributes(self, kwargs: dict) -> None:
        """Check if any required attribute is missing."""
        for key in kwargs:
            if key not in self.__annotations__ and key not in self:
                raise AttributeError(f"{self.__class__.__name__} does not have attribute: {key!r}")

    def _get_attributes(self, kwargs: dict) -> None:
        """Get all attributes from keyworded arguments."""
        for key in self.__annotations__:
            try:
                self[key] = kwargs[key]
            except KeyError as err:
                if key not in self:
                    raise AttributeError(f"{self.__class__.__name__} missing required attribute: {key!r}") from err

    def __getattribute__(self, name: str) -> t.Any:
        if name.startswith("_"):
            return super().__getattribute__(name)

        if name in self.__annotations__ and name in self:
            return self[name]

        return super().__getattribute__(name)

    def __getattr__(self, name: str) -> t.Any:
        try:
            return self[name]
        except KeyError as err:
            raise AttributeError(f"{self.__class__.__name__} does not have attribute: {name!r}") from err

    def __setattr__(self, name: str, value: t.Any) -> None:
        self[name] = value

    def __deepcopy__(self, memo):
        return self.__class__(**deepcopy(dict(self)))


DataType = TypeVar("DataType", bound=Base)


class PagingInfo(Base):
    """Paging info."""

    page_count: int = 1
    """How many pages."""

    page_number: int = 1
    """Current page."""

    page_size: int = 10
    """Current page size."""

    total_record_count: int = 1
    """Total amount of records."""


class Paging(Base, Generic[DataType]):
    """A Paging."""

    data: Tuple[DataType, ...]
    """The actual data."""

    paging: PagingInfo
    """Information on current paging."""

    def to_response(self):
        return {"data": self.data, "paging": self.paging}
