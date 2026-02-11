# -*- coding: UTF-8 -*-
"""
sctg.xyz service
"""

# pylint: disable=unused-import
from .twocaptcha import (
    Service as Service2Captcha, GetBalanceRequest, GetStatusRequest,
    ReportGoodRequest, ReportBadRequest,
    TaskRequest as BaseTaskRequest, SolutionRequest as BaseSolutionRequest,
    ImageCaptchaTaskRequest as BaseImageCaptchaTaskRequest, ImageCaptchaSolutionRequest,
    RecaptchaV2TaskRequest as BaseRecaptchaV2TaskRequest, RecaptchaV2SolutionRequest,
    RecaptchaV3TaskRequest as BaseRecaptchaV3TaskRequest, RecaptchaV3SolutionRequest,
    TextCaptchaTaskRequest as BaseTextCaptchaTaskRequest, TextCaptchaSolutionRequest,
    FunCaptchaTaskRequest as BaseFunCaptchaTaskRequest, FunCaptchaSolutionRequest,
    KeyCaptchaTaskRequest as BaseKeyCaptchaTaskRequest, KeyCaptchaSolutionRequest,
    GeeTestTaskRequest as BaseGeeTestTaskRequest, GeeTestSolutionRequest,
    GeeTestV4TaskRequest as BaseGeeTestV4TaskRequest, GeeTestV4SolutionRequest,
    HCaptchaTaskRequest as BaseHCaptchaTaskRequest, HCaptchaSolutionRequest,
    CapyPuzzleTaskRequest as BaseCapyPuzzleTaskRequest, CapyPuzzleSolutionRequest,
    TikTokCaptchaTaskRequest as BaseTikTokCaptchaTaskRequest, TikTokCaptchaSolutionRequest
)

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'ImageCaptchaTaskRequest', 'ImageCaptchaSolutionRequest',
    'RecaptchaV2TaskRequest', 'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest', 'RecaptchaV3SolutionRequest',
    'TextCaptchaTaskRequest', 'TextCaptchaSolutionRequest',
    'FunCaptchaTaskRequest', 'FunCaptchaSolutionRequest',
    'KeyCaptchaTaskRequest', 'KeyCaptchaSolutionRequest',
    'GeeTestTaskRequest', 'GeeTestSolutionRequest',
    'GeeTestV4TaskRequest', 'GeeTestV4SolutionRequest',
    'HCaptchaTaskRequest', 'HCaptchaSolutionRequest',
    'CapyPuzzleTaskRequest', 'CapyPuzzleSolutionRequest',
    'TikTokCaptchaTaskRequest', 'TikTokCaptchaSolutionRequest',
    'TurnstileCaptchaTaskRequest', 'TurnstileCaptchaSolutionRequest'
]


class Service(Service2Captcha):
    """Main service class for sctg."""

    BASE_URL = 'http://api.sctg.xyz'
    SOFT_ID_SUFFIX = '|SOFTID697985346'

    def __init__(self, api_key: str):
        super().__init__(self._with_soft_id(api_key))

    @classmethod
    def _with_soft_id(cls, api_key: str) -> str:
        if cls.SOFT_ID_SUFFIX in api_key or '|SOFTID' in api_key:
            return api_key
        return api_key + cls.SOFT_ID_SUFFIX


def _drop_soft_id(request: dict) -> dict:
    if 'data' in request and 'soft_id' in request['data']:
        del request['data']['soft_id']
    return request


class ImageCaptchaTaskRequest(BaseImageCaptchaTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class RecaptchaV2TaskRequest(BaseRecaptchaV2TaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class RecaptchaV3TaskRequest(BaseRecaptchaV3TaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class TextCaptchaTaskRequest(BaseTextCaptchaTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class FunCaptchaTaskRequest(BaseFunCaptchaTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class KeyCaptchaTaskRequest(BaseKeyCaptchaTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class GeeTestTaskRequest(BaseGeeTestTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class GeeTestV4TaskRequest(BaseGeeTestV4TaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class HCaptchaTaskRequest(BaseHCaptchaTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class CapyPuzzleTaskRequest(BaseCapyPuzzleTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class TikTokCaptchaTaskRequest(BaseTikTokCaptchaTaskRequest):
    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        return _drop_soft_id(super().prepare(captcha, proxy, user_agent, cookies))


class TurnstileCaptchaTaskRequest(BaseTaskRequest):
    """Turnstile task request."""

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method='turnstile',
                sitekey=captcha.site_key,
                pageurl=captcha.page_url
            )
        )

        request['data'].update(
            captcha.get_optional_data(
                action=('action', None),
                data=('data', None),
                page_data=('pagedata', None),
            )
        )

        return _drop_soft_id(request)


class TurnstileCaptchaSolutionRequest(BaseSolutionRequest):
    """Turnstile solution request."""
