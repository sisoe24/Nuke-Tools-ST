"""Configuration file for pytest."""

import os
import pytest

from src import nuke_tools


@pytest.fixture(scope='session')
def package():
    """Package directory path."""
    current_dir = os.path.dirname(__file__)
    package_dir = os.path.abspath(os.path.dirname(current_dir))
    yield package_dir


@pytest.fixture(autouse=True)
def no_config(monkeypatch):
    """Monkeypatch the config file path."""
    monkeypatch.setattr(nuke_tools, 'NSS_CONFIG', '')
