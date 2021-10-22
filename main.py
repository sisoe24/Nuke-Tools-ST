"""Init module for Sublime package."""

import sublime
import sublime_plugin

from .src import nuke_tools


class RunNukeToolsCommand(sublime_plugin.TextCommand):
    """Sublime API interface class."""

    def run(self, edit):
        """Run sublime main command."""
        settings = sublime.load_settings("Preferences.sublime-settings")

        hostname = settings.get("nss_hostname", "127.0.0.1")
        port = settings.get("nss_port", nuke_tools.nss_ip_port())

        file_content = self.view.substr(sublime.Region(0, self.view.size()))
        data = nuke_tools.prepare_data(file_content, self.view.file_name())

        output = nuke_tools.send_data(hostname, port, data)
        print(output)
