# -*- coding: UTF-8 -*-
"""
Cloudflare Turnstile solving example for multibot.in
"""

import os

from multicaps import CaptchaSolver, CaptchaSolvingService, exceptions  # type: ignore

API_KEY = os.getenv('API_KEY_MULTIBOT', default='<PLACE_YOUR_API_KEY_HERE>')
PAGE_URL = 'https://turnstile.zeroclover.io/'
SITE_KEY = '0x4AAAAAAAEwzhD6pyKkgXC0'


if __name__ == '__main__':
    with CaptchaSolver(CaptchaSolvingService.MULTIBOT, API_KEY) as solver:
        try:
            solved = solver.solve_turnstile(
                site_key=SITE_KEY,
                page_url=PAGE_URL
            )
            print(solved.solution.token)
        except exceptions.UnicapsException as exc:
            print(f'Turnstile solving exception: {str(exc)}')
