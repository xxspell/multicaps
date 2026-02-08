# -*- coding: UTF-8 -*-
"""
multibot.in service
"""

from .base import HTTPService
from .._transport.http_transport import HTTPRequestJSON  # type: ignore
from .. import exceptions
from .._captcha import CaptchaType

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'HCaptchaTaskRequest', 'HCaptchaSolutionRequest',
    'RecaptchaV2TaskRequest', 'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest', 'RecaptchaV3SolutionRequest',
    'TurnstileCaptchaTaskRequest', 'TurnstileCaptchaSolutionRequest',
]


class Service(HTTPService):
    """Main service class for multibot."""

    BASE_URL = 'https://api.multibot.in'

    def _post_init(self):
        """Init captcha polling settings."""

        for captcha_type in self.settings:
            self.settings[captcha_type].polling_interval = 5
            self.settings[captcha_type].solution_timeout = 180

            if captcha_type == CaptchaType.RECAPTCHAV2:
                self.settings[captcha_type].polling_delay = 20
                self.settings[captcha_type].solution_timeout = 300
            elif captcha_type == CaptchaType.RECAPTCHAV3:
                self.settings[captcha_type].polling_delay = 15
            else:
                self.settings[captcha_type].polling_delay = 5


class Request(HTTPRequestJSON):
    """Common request class for multibot."""

    def parse_response(self, response) -> dict:
        """Parse response and map service errors to library exceptions."""

        response_data = super().parse_response(response)
        status = response_data.get("status")

        # "userinfo" responses do not contain "status".
        if status is None:
            return response_data

        if status in (1, "1", "ready", True):
            return response_data

        error_code = response_data.get("request") or response_data.get("errorCode") or str(status)
        error_msg = f"{error_code}: {response_data.get('error_text', '')}"

        if error_code == 'CAPCHA_NOT_READY':
            raise exceptions.SolutionNotReadyYet()
        if error_code == 'ERROR_WRONG_USER_KEY':
            raise exceptions.AccessDeniedError(error_msg)
        if error_code == 'ERROR_ZERO_BALANCE':
            raise exceptions.LowBalanceError(error_msg)
        if error_code in ('ERROR_NO_SLOT_AVAILABLE',):
            raise exceptions.ServiceTooBusy(error_msg)
        if error_code in ('MAX_USER_TURN',) or str(error_code).startswith('ERROR:'):
            raise exceptions.TooManyRequestsError(error_msg)
        if error_code in ('WRONG_CAPTCHA_ID',):
            raise exceptions.MalformedRequestError(error_msg)
        if error_code in ('WRONG_RESULT',):
            raise exceptions.UnableToSolveError(error_msg)
        if error_code in ('ERROR_BAD_PROXY', 'ERROR_PROXY_CONNECTION_FAILED'):
            raise exceptions.ProxyError(error_msg)
        if error_code in (
            'ERROR_METHOD_DOES_NOT_EXIST', 'WRONG_METHOD', 'ERROR_BAD_DATA',
            'WRONG_REQUESTS_LINK', 'WRONG_LOAD_PAGEURL', 'ERROR_SITEKEY',
            'SITEKEY_IS_INCORRECT', 'HCAPTCHA_NOT_FOUND', 'TURNSTILE_NOT_FOUND'
        ):
            raise exceptions.BadInputDataError(error_msg)

        raise exceptions.ServiceError(error_msg)


class InRequest(Request):
    """Request class for requests to /in.php."""

    def prepare(self, **kwargs) -> dict:
        """Prepare multipart/form-data request."""

        request = super().prepare(**kwargs)
        request.update(
            dict(
                method="POST",
                url=self._service.BASE_URL + "/in.php",
                files=dict(
                    key=(None, self._service.api_key),
                    json=(None, "1"),
                )
            )
        )
        return request


class ResRequest(Request):
    """Request class for requests to /res.php."""

    def prepare(self, **kwargs) -> dict:
        """Prepare request."""

        request = super().prepare(**kwargs)
        request.update(
            dict(
                method="GET",
                url=self._service.BASE_URL + "/res.php",
                params=dict(
                    key=self._service.api_key,
                    json=1
                )
            )
        )
        return request


class GetBalanceRequest(ResRequest):
    """GetBalance request class."""

    def prepare(self) -> dict:
        request = super().prepare()
        request["params"].update(dict(action="userinfo"))
        return request

    def parse_response(self, response) -> dict:
        return {'balance': float(super().parse_response(response)["balance"])}


class GetStatusRequest(GetBalanceRequest):
    """GetStatus request class."""

    def parse_response(self, response) -> dict:
        try:
            return super().parse_response(response)
        except exceptions.UnicapsException:
            return {}


class ReportGoodRequest(ResRequest):
    """ReportGood request class."""

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        request = super().prepare(solved_captcha=solved_captcha)
        request["params"].update(
            dict(
                action="reportgood",
                id=solved_captcha.captcha_id
            )
        )
        return request


class ReportBadRequest(ResRequest):
    """ReportBad request class."""

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        request = super().prepare(solved_captcha=solved_captcha)
        request["params"].update(
            dict(
                action="reportbad",
                id=solved_captcha.captcha_id
            )
        )
        return request


class TaskRequest(InRequest):
    """Common task request class."""

    # pylint: disable=arguments-differ,unused-argument
    def prepare(self, captcha, proxy, user_agent, cookies):
        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        if proxy:
            request['files']['proxy'] = (None, proxy.get_string())

        return request

    def parse_response(self, response) -> dict:
        response_data = super().parse_response(response)
        return dict(
            task_id=response_data.pop("request"),
            extra=response_data
        )


class SolutionRequest(ResRequest):
    """Common solution request class."""

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        request = super().prepare(task=task)
        request["params"].update(dict(id=task.task_id))
        return request

    def parse_response(self, response) -> dict:
        response_data = super().parse_response(response)
        solution_class = self.source_data['task'].captcha.get_solution_class()
        return dict(
            solution=solution_class(response_data["request"]),
            cost=response_data.get("price"),
            extra=response_data
        )


class RecaptchaV2TaskRequest(TaskRequest):
    """reCAPTCHA v2 task request."""

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )
        request['files'].update(
            dict(
                method=(None, "userrecaptcha"),
                googlekey=(None, captcha.site_key),
                pageurl=(None, captcha.page_url),
            )
        )
        if captcha.is_enterprise:
            request['files']['enterprise'] = (None, "1")
        return request


class RecaptchaV2SolutionRequest(SolutionRequest):
    """reCAPTCHA v2 solution request."""


class RecaptchaV3TaskRequest(TaskRequest):
    """reCAPTCHA v3 task request."""

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )
        request['files'].update(
            dict(
                method=(None, "userrecaptcha"),
                version=(None, "v3"),
                googlekey=(None, captcha.site_key),
                pageurl=(None, captcha.page_url),
            )
        )
        if captcha.action:
            request['files']['action'] = (None, captcha.action)
        if captcha.is_enterprise:
            request['files']['enterprise'] = (None, "1")
        return request


class RecaptchaV3SolutionRequest(SolutionRequest):
    """reCAPTCHA v3 solution request."""


class HCaptchaTaskRequest(TaskRequest):
    """hCaptcha task request."""

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )
        request['files'].update(
            dict(
                method=(None, "hcaptcha"),
                sitekey=(None, captcha.site_key),
                pageurl=(None, captcha.page_url),
            )
        )
        return request


class HCaptchaSolutionRequest(SolutionRequest):
    """hCaptcha solution request."""


class TurnstileCaptchaTaskRequest(TaskRequest):
    """Turnstile task request."""

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )
        request['files'].update(
            dict(
                method=(None, "turnstile"),
                sitekey=(None, captcha.site_key),
                pageurl=(None, captcha.page_url),
            )
        )
        if captcha.action:
            request['files']['action'] = (None, captcha.action)
        if captcha.data:
            request['files']['data'] = (None, captcha.data)
        if captcha.page_data:
            request['files']['pagedata'] = (None, captcha.page_data)
        return request


class TurnstileCaptchaSolutionRequest(SolutionRequest):
    """Turnstile solution request."""
