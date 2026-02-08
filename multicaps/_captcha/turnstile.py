# -*- coding: UTF-8 -*-
"""
Cloudflare Turnstile
"""

from dataclasses import dataclass
from typing import Optional

from .._compat import enforce_types

from .base import BaseCaptcha, BaseCaptchaSolution


@enforce_types
@dataclass
class TurnstileCaptcha(BaseCaptcha):
    """Cloudflare Turnstile CAPTCHA."""

    site_key: str
    page_url: str
    action: Optional[str] = None
    data: Optional[str] = None
    page_data: Optional[str] = None


@enforce_types
@dataclass
class TurnstileCaptchaSolution(BaseCaptchaSolution):
    """Cloudflare Turnstile solution."""

    token: str
