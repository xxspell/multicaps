# -*- coding: UTF-8 -*-
"""
Compatibility helpers.
"""

import os
from typing import TypeVar

T = TypeVar('T')


def enforce_types(obj: T) -> T:
    """No-op decorator by default.

    Runtime type enforcement can be enabled by setting
    MULTICAPS_ENABLE_ENFORCE_TYPES=1 and installing enforce-typing.
    """

    if os.getenv("MULTICAPS_ENABLE_ENFORCE_TYPES") == "1":
        try:
            from enforce_typing import enforce_types as _enforce_types  # type: ignore
        except ModuleNotFoundError:
            return obj
        return _enforce_types(obj)  # type: ignore

    return obj
