from msgspec._core import NODEFAULT, UNSET, DecodeError, EncodeError
from msgspec._core import Field as _Field
from msgspec._core import (
    Meta,
    MsgspecError,
    Raw,
    Struct,
    UnsetType,
    ValidationError,
    convert,
    defstruct,
    to_builtins,
)


def field(*, default=NODEFAULT, default_factory=NODEFAULT, name=None):
    return _Field(default=default, default_factory=default_factory, name=name)


field.__doc__ = _Field.__doc__


from importlib.metadata import PackageNotFoundError, version

from setuptools_scm import get_version  # type: ignore

from msgspec import inspect, json, msgpack, structs, toml, yaml


def current_version() -> str:
    """Returns the currently installed version of msgspec."""
    try:
        version_ = version('msgspec')
    except PackageNotFoundError:  # pragma: no cover
        version_ = str(get_version(root='..', relative_to=__file__))
    return version_


__version__ = current_version()
del current_version
