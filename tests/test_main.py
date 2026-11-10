"""Test module for NukeTools."""
import re
import os
import sys
import types
import importlib

import pytest

from src import nuke_tools


def _load_plugin(package):
    """Import `main.py` with stub `sublime` modules, as Sublime would load it."""
    sublime = types.ModuleType('sublime')
    sublime.load_settings = lambda _: {}
    sublime_plugin = types.ModuleType('sublime_plugin')
    sublime_plugin.TextCommand = type(
        'TextCommand', (), {'__init__': lambda self, view: setattr(self, 'view', view)}
    )
    sys.modules.update(sublime=sublime, sublime_plugin=sublime_plugin)

    # main.py uses a relative import, so load it as part of a package
    plugin_package = types.ModuleType('nuketools_plugin')
    plugin_package.__path__ = [package]
    sys.modules['nuketools_plugin'] = plugin_package
    return importlib.import_module('nuketools_plugin.main')


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


def test_menu_hidden_for_unsaved_view(package):
    """Test the context menu on a view without a file does not raise."""
    plugin = _load_plugin(package)
    view = types.SimpleNamespace(file_name=lambda: None)
    assert plugin.RunNukeToolsCommand(view).is_visible() is False


def test_config_port(tmp_path, monkeypatch):
    """Test the port is read from the NukeServerSocket json file."""
    config = tmp_path / 'nukeserversocket.json'
    config.write_text('{"port": 55555}')
    monkeypatch.setattr(nuke_tools, 'NSS_CONFIG', str(config))
    assert nuke_tools.nss_ip_port() == 55555


@pytest.mark.parametrize('content', [
    'port = 54321',
    '{"port": "not-a-number"}',
    '{"port": null}',
    '{"server_timeout": 3600000}',
    '[54321]',
])
def test_malformed_config_uses_default_port(tmp_path, monkeypatch, content):
    """Test a malformed json falls back to the default port."""
    config = tmp_path / 'nukeserversocket.json'
    config.write_text(content)
    monkeypatch.setattr(nuke_tools, 'NSS_CONFIG', str(config))
    assert nuke_tools.nss_ip_port() == 54321


def test_port_setting_skips_config(package, monkeypatch):
    """Test the `nss_port` setting is used without reading the config."""
    plugin = _load_plugin(package)
    sublime = plugin.sublime
    sent = []
    monkeypatch.setattr(
        sublime, 'load_settings', lambda _: {'nss_port': 12345}
    )
    monkeypatch.setattr(sublime, 'Region', lambda *_: None, raising=False)
    monkeypatch.setattr(
        sublime, 'set_timeout_async', lambda func: func(), raising=False
    )

    def broken_config():
        raise AssertionError('config must not be read when nss_port is set')

    monkeypatch.setattr(plugin.nuke_tools, 'nss_ip_port', broken_config)
    monkeypatch.setattr(
        plugin.nuke_tools, 'send_data', lambda *args: sent.append(args)
    )
    view = types.SimpleNamespace(
        size=lambda: 0, substr=lambda _: '', file_name=lambda: 'test.py'
    )
    plugin.RunNukeToolsCommand(view).run(None)
    assert sent[0][1] == 12345
