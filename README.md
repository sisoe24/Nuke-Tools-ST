# 1. Nuke Tools ST README

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/522af2c16ed84926b77f2e095cfa8b87)](https://www.codacy.com/gh/sisoe24/Nuke-Tools-ST/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sisoe24/Nuke-Tools-ST&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/522af2c16ed84926b77f2e095cfa8b87)](https://www.codacy.com/gh/sisoe24/Nuke-Tools-ST/dashboard?utm_source=github.com&utm_medium=referral&utm_content=sisoe24/Nuke-Tools-ST&utm_campaign=Badge_Coverage)
[![DeepSource](https://deepsource.io/gh/sisoe24/Nuke-Tools-ST.svg/?label=active+issues&show_trend=true&token=Yrd2y9gG7y8h53JsDwyjQdFZ)](https://deepsource.io/gh/sisoe24/Nuke-Tools-ST/?ref=repository-badge)

[![PackageControl](https://img.shields.io/badge/Package%20Control-Download-informational)](https://packagecontrol.io/packages/NukeToolsST)


> This is a companion extension for: [NukeServerSocket](#nukeserversocket) and is based on [NukeTools](https://marketplace.visualstudio.com/items?itemName=virgilsisoe.nuke-tools).

A Sublime Text package that allows to send python or blinkscript code to be executed inside Nuke.

- [1. Nuke Tools ST README](#1-nuke-tools-st-readme)
  - [1.1. NukeServerSocket](#11-nukeserversocket)
  - [1.2. Features](#12-features)
  - [1.3. Installation](#13-installation)
  - [1.4. Usage](#14-usage)
  - [1.4. BlinkScript](#14-blinkscript)
  - [1.5. Connection](#15-connection)
  - [1.6. Package Settings](#16-package-settings)
    - [1.6.1. `nss_port`:`integer`](#161-nss_portinteger)
    - [1.6.2. `nss_hostname`:`string`](#162-nss_hostnamestring)
    - [1.6.3. `nss_disable_context_menu`:`bool`](#163-nss_disable_context_menubool)
    - [1.6.4. Example](#164-example)
  - [1.7. Commands](#17-commands)
  - [1.8. Key Bindings](#18-key-bindings)
  - [1.9. Changelog](#19-changelog)
  - [1.10. Overview](#110-overview)

## 1.1. NukeServerSocket

Download the companion plugin:

- [Github](https://github.com/sisoe24/NukeServerSocket/releases)
- [Nukepedia](http://www.nukepedia.com/python/misc/nukeserversocket)

## 1.2. Features

- Execute code inside Nuke from a machine in your local network.
  - Get output of Nuke code execution inside Sublime console.
  - When used locally (same machine) no configuration is required, just running the server inside Nuke.
  - Specify a custom address when connection is from/to another computer.
  - Multiple connections can be made to the same Nuke instance.
  - BlinkScript support.

## 1.3. Installation

The preferred method of installation is via the [Package Control](https://packagecontrol.io).

- [Package Link](https://packagecontrol.io/packages/NukeToolsST)
- Inside Sublime, invoke the **Command Palette** -> **Install Package** -> **NukeToolsST**.

## 1.4. Usage

[Demo](#110-overview)

Once NukeServerSocket is up and running, you can execute your python/blink file with the new [command](#17-commands).

## 1.4. BlinkScript

> NukeServerSocket >= 0.1.0 is needed in order for this to work.

The extension will take the name of the current active file and create a blinkscript node inside Nuke with the name as the current filename. If the node already exists, then will only modified its source code. Once done will recompile the source kernel.

The accepted file extension are `.cpp` or `.blink`.

## 1.5. Connection

No settings are necessary if connection is expected to be on the same computer.
NukeToolsST will automatically connect to the `localhost` and will use the port
configuration found inside _$HOME/.nuke/NukeServerSocket.ini_. The configuration value is updated automatically each time its changed inside the plugin.

However if connection is between different computers, port and hostname must be changed manually via the [package settings](#package-settings).

> Keep in mind that, once the addresses are specified manually, will always take over the defaults one. Its best to delete them if you only connect between the same computer.

**Note**: Attempting to connect to a manually specified host that is down (not reachable)
will result in a temporary freeze of the Sublime UI for 10 seconds.

## 1.6. Package Settings

### 1.6.1. `nss_port`:`integer`

A different port for the connection. Port should match the one from NukeServerSocket.

### 1.6.2. `nss_hostname`:`string`

Same as `nss_port`. Host could be the localhost or the local ip.

### 1.6.3. `nss_disable_context_menu`:`bool`

Disable Sublime context menu entry if not needed. Defaults to `false`.

### 1.6.4. Example

```json
{
  "nss_port": 54321,
  "nss_hostname": "192.168.1.60",
  "nss_disable_context_menu": true
}
```

## 1.7. Commands

The following command will be available: `run_nuke_tools`.

A new entry "Run Code inside Nuke" will be added to the context menu (right click) when the active file ends with one of the following extension:

- `.py`
- `.cpp`
- `.blink`

## 1.8. Key Bindings

The package does not include any key bindings by default but you can add them by following the [Sublime Text Key Bindings guide](https://www.sublimetext.com/docs/key_bindings.html).

Example

```json
[
    {
        "keys" : ["ctrl+alt+n"],
        "command" : "run_nuke_tools"
    }
]
```


## 1.9. Changelog

[0.2.0] 11-04-2021

- Removed most of the commands, leaving only the context menu one.
- Removed default key bindings.
- New configuration to hide context menu.
- Context menu options shows only on specific file extensions.

[0.1.0] 10-21-2021

- Initial release.

## 1.10. Overview

![example](example.gif)
