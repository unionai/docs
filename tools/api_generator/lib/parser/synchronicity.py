import inspect
from typing import Any, Optional
from lib.parser.docstring import parse_docstring
from lib.parser.methods import do_parse_method
from lib.ptypes import MethodInfo


def is_synchronicity_method(name: str, member: object) -> bool:
    try:
        return (
            str(member.__dict__["_synchronizer"]).index(
                "synchronicity.synchronizer.Synchronizer"
            )
            != -1
        )
    except (AttributeError, ValueError, KeyError):
        return False


def parse_synchronicity_method(name: str, member: Any) -> Optional[MethodInfo]:
    return do_parse_method(name, member, "synchronicity")
