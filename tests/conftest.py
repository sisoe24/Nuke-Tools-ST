"""Configuration file for pytest."""

import pytest

from src import main


@pytest.fixture(autouse=True)
def no_config(monkeypatch):
    """Monkeypatch the config file path."""
    monkeypatch.setattr(main, 'NSS_CONFIG', '')
