# -*- coding: UTF-8 -*-
"""
CaptchaSolver tests
"""
from unittest.mock import Mock

import pytest
from multicaps import CaptchaSolver, CaptchaSolvingService
from multicaps.captcha import CaptchaType
from multicaps._service.sctg import Service as SCTGService

API_KEY = 'TEST_API_KEY'


@pytest.fixture(scope="module")
def captcha_solver():
    return CaptchaSolver('2captcha.com', API_KEY)


@pytest.fixture()
def mocked_captcha_solver(captcha_solver, monkeypatch):
    monkeypatch.setattr(captcha_solver, '_service', Mock())
    return captcha_solver


def test_solver_init():
    service = CaptchaSolvingService.ANTI_CAPTCHA
    solver = CaptchaSolver(service, API_KEY)

    assert solver.service_name == service
    assert solver.api_key == API_KEY


def test_solver_init_from_string():
    solver = CaptchaSolver('2captcha.com', API_KEY)

    assert solver.service_name == CaptchaSolvingService.TWOCAPTCHA
    assert solver.api_key == API_KEY


def test_solver_bad_init():
    with pytest.raises(ValueError):
        CaptchaSolver('2captcha', API_KEY)


def test_solver_bad_init2():
    with pytest.raises(ValueError):
        CaptchaSolver(b'2captcha.com', API_KEY)


def test_sctg_softid_auto_append():
    service = SCTGService(API_KEY)
    assert service.api_key == API_KEY + '|SOFTID697985346'


def test_sctg_softid_not_duplicated():
    key_with_softid = API_KEY + '|SOFTID697985346'
    service = SCTGService(key_with_softid)
    assert service.api_key == key_with_softid


def test_sctg_keeps_other_suffixes_and_adds_softid():
    service = SCTGService(API_KEY + '|offfast|onlyxevil')
    assert service.api_key == API_KEY + '|offfast|onlyxevil|SOFTID697985346'


# @pytest.mark.parametrize("captcha_type", CaptchaType)
def test_call_solve_func(mocked_captcha_solver, captcha_instance):
    mapping = {
        CaptchaType.IMAGE: 'image_captcha',
        CaptchaType.TEXT: 'text_captcha',
        CaptchaType.RECAPTCHAV2: 'recaptcha_v2',
        CaptchaType.RECAPTCHAV3: 'recaptcha_v3',
        CaptchaType.HCAPTCHA: 'hcaptcha',
        CaptchaType.FUNCAPTCHA: 'funcaptcha',
        CaptchaType.KEYCAPTCHA: 'keycaptcha',
        CaptchaType.GEETEST: 'geetest',
        CaptchaType.CAPY: 'capy_puzzle',
        CaptchaType.TIKTOK: 'tiktok',
        CaptchaType.GEETESTV4: 'geetest_v4',
        CaptchaType.TURNSTILE: 'turnstile'
    }

    func = getattr(mocked_captcha_solver, f'solve_{mapping[captcha_instance.get_type()]}')
    func(
        **{k: v for k, v in captcha_instance.__dict__.items() if not k.startswith('_')}
    )
