"""Test module for NukeTools."""
import re
import os
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


def test_settings_name(package):
    """Test that sublime settings name match correct name."""
    default_settings = ["nss_port", "nss_hostname"]

    main_file = os.path.join(package, 'nuke_tools.py')
    with open(main_file, encoding='utf-8') as file:
        content = file.read()
        settings = re.findall(r'(?<=settings.get\(")\w+', content, re.S)
        for setting in settings:
            assert setting in default_settings
