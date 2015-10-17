#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.config
-------------------

Global configuration handling
"""

from __future__ import unicode_literals
import copy
import io
import json
import logging
import os

from .exceptions import ConfigDoesNotExistException
from .exceptions import InvalidConfiguration


logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'cookiecutters_dir': os.path.expanduser('~/.cookiecutters/'),
    'replay_dir': os.path.expanduser('~/.cookiecutter_replay/'),
    'default_context': {}
}


def get_yaml_parser():

    # Try to get the best YAML library
    use_yaml = True
    try:
        import yaml
    except ImportError:
        # Fall back to ruamel.yaml if it exists
        try:
            import ruamel.yaml as yaml
        except ImportError:
            raise


def get_config(config_path):
    """
    Retrieve the config from the specified path, returning it as a config dict.
    """

    if not os.path.exists(config_path):
        raise ConfigDoesNotExistException

    try:
        yaml = get_yaml_parser()
    except ImportError:
        yaml = None

    logger.debug('config_path is {0}'.format(config_path))

    with io.open(config_path, encoding='utf-8') as file_handle:
        if yaml:
            try:
                config_dict = yaml.safe_load(file_handle)
            except yaml.scanner.ScannerError as e:
                raise InvalidConfiguration(
                    '{0} is not a valid YAML file: line {1}: {2}'.format(
                        config_path,
                        e.problem_mark.line,
                        e.problem))
        else:  # Use json
            config_dict = json.loads(file_handle)

    config_dict = copy.copy(DEFAULT_CONFIG)
    config_dict.update(config_dict)

    return config_dict


def get_user_config():
    """
    Retrieve config from the user's ~/.cookiecutterrc, if it exists.
    Otherwise, return None.
    """

    # TODO: test on windows...
    USER_CONFIG_PATH = os.path.expanduser('~/.cookiecutterrc')

    if os.path.exists(USER_CONFIG_PATH):
        return get_config(USER_CONFIG_PATH)
    return copy.copy(DEFAULT_CONFIG)
