#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from .logger import Logger, log_func, hidden_text
from functools import partial

logger = Logger().get_logger(__file__)
log_func = partial(log_func, logger=logger)


@log_func()
def request(**kwargs):
    try:
        responses = requests.request(**kwargs)
        logger.debug(hidden_text(responses.text))
    except Exception as e:
        logger.error(e)
        raise
    return responses
