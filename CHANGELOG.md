# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Changed

- The port is now read from `~/.nuke/nukeserversocket.json`, the settings file written by NukeServerSocket 1.0 and later. `NukeServerSocket.ini` is no longer read.

### Fixed

- A malformed NukeServerSocket settings file no longer stops the command. The default port 54321 is used instead.
- The `nss_port` setting now overrides the NukeServerSocket settings file, which is no longer read when `nss_port` is set.

## [0.2.3] - 2026-11-04

### Added

- README section on setting up Nuke/Hiero Python stubs with LSP-pyright.

### Fixed

- Long Nuke output is no longer cut off after 2048 bytes.
- Nuke code that runs longer than 10 seconds no longer reports a timeout error.
- Connection errors while sending code or reading the reply now show a readable message instead of a traceback.
- Right-clicking in an unsaved tab no longer raises an error in the console.

## [0.2.2] - 2026-11-04

### Fixed

- Running code inside Nuke no longer freezes the Sublime Text UI when the host is slow or unreachable ([#2](https://github.com/sisoe24/Nuke-Tools-ST/issues/2)).

### Changed

- Moved the changelog from the README into its own file.

## [0.2.1] - 2022-02-17

### Changed

- Updated the README documentation.

## [0.2.0] - 2021-11-04

### Added

- New setting `nss_disable_context_menu` to hide the context menu entry.

### Changed

- The context menu entry shows only for `.py`, `.cpp` and `.blink` files.

### Removed

- Removed most of the commands, leaving only the context menu one.
- Removed the default key bindings.

## [0.1.0] - 2021-10-21

- Initial release.
