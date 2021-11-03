"""Init module for Sublime package."""
import os

import sublime
import sublime_plugin

from .src import nuke_tools


class RunNukeToolsCommand(sublime_plugin.TextCommand):
    """Sublime API interface class."""

    def run(self, _edit):
        """Run sublime main command."""
        settings = sublime.load_settings("Preferences.sublime-settings")

        hostname = settings.get("nss_hostname", "127.0.0.1")
        port = settings.get("nss_port", nuke_tools.nss_ip_port())

        file_content = self.view.substr(sublime.Region(0, self.view.size()))
        data = nuke_tools.prepare_data(file_content, self.view.file_name())

        output = nuke_tools.send_data(hostname, port, data)

        # XXX: should probably use the logging module?
        print(output)

    def is_visible(self):
        """Show command in the menu based on the current file extension.

        Command will be shown only if active file ends with `.py`, `.cpp`,
        `.blink` extension and if settings `nss_disable_context_menu` is false.

        Returns:
            bool - True if command should be shown, False otherwise.
        """
        settings = sublime.load_settings("Preferences.sublime-settings")
        if settings.get("nss_disable_context_menu", False):
            return False

        _, file_ext = os.path.splitext(self.view.file_name())
        return file_ext in ('.py', '.cpp', '.blink')
