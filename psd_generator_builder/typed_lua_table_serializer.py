from logging import getLogger
import re
from typing import Any


logger = getLogger(__name__)


def deserialize(
    obj: Any, *, type_key="type", raise_when_key_missing: bool = False
) -> str:
    """Deserialize dict to typed lua-table-like string

    Parameters
    ----------
    obj : Any
        must contain "type" key if dict.

    Returns
    -------
    str
        typed lua-like string.
        Example:


    Raises
    ------
    ValueError
        Key 'type' is missing. Raises only when raise_when_key_missing is True.
    """

    if not isinstance(obj, dict):
        return f'"{obj}"'

    result = ""
    if not type_key in obj:
        if raise_when_key_missing:
            raise ValueError("obj must contain 'type' key.")
        logger.warning(f"Key 'type' is missing from {obj}")
    elif s := str(obj[type_key]):
        result += s + " "
    result += "{ "
    for key, value in obj.items():
        if key == "type":
            continue
        if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", key):
            result += key + " = "
        else:
            result += f'["{key}"] = '
        result += deserialize(value)
        result += ", "
    result += " }"
    return result
