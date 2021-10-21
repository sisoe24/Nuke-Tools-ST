"""Test module for NukeTools."""

from src import main


def test_ip_port_is_int():
    """Test the ip port is always an integer."""
    port = main.nss_ip_port()
    assert isinstance(port, int)


def test_default_port():
    """Test default port value if not file is found."""
    port = main.nss_ip_port()
    assert port == 54321


def test_prepare_data():
    """Test if the data returns a stringified dictionary."""
    data = main.prepare_data('hello', 'test.py')
    assert data == '{"text": "hello", "file": "test.py"}'
