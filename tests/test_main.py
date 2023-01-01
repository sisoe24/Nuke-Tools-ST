"""Test module for NukeTools."""
import re
import os

from src import nuke_tools


def test_ip_port_is_int():
    """Test the ip port is always an integer."""
    port = nuke_tools.nss_ip_port()
    assert isinstance(port, int)


def test_default_port():
    """Test default port value if not file is found."""
    port = nuke_tools.nss_ip_port()
    assert port == 54321


def test_prepare_data():
    """Test if the data returns a stringified dictionary."""
    data = nuke_tools.prepare_data('hello', 'test.py')
    assert data == '{"text": "hello", "file": "test.py"}'


def test_format_output():
    """Test the format output return."""
    output = nuke_tools.format_output('hello')
    assert re.search(r'\[\d\d:\d\d:\d\d\] \[NukeTools\] hello', output)


def test_settings_name(package):
    """Test that sublime settings name match correct name."""
    default_settings = ["nss_port", "nss_hostname", "nss_disable_context_menu"]

    main_file = os.path.join(package, 'main.py')
    with open(main_file, encoding='utf-8') as file:
        content = file.read()
        settings = re.findall(r'(?<=settings.get\(")\w+', content, re.S)
        for setting in settings:
            assert setting in default_settings
