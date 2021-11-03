# Nuke Tools ST README

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/522af2c16ed84926b77f2e095cfa8b87)](https://www.codacy.com/gh/sisoe24/Nuke-Tools-ST/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sisoe24/Nuke-Tools-ST&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/522af2c16ed84926b77f2e095cfa8b87)](https://www.codacy.com/gh/sisoe24/Nuke-Tools-ST/dashboard?utm_source=github.com&utm_medium=referral&utm_content=sisoe24/Nuke-Tools-ST&utm_campaign=Badge_Coverage)
[![DeepSource](https://deepsource.io/gh/sisoe24/Nuke-Tools-ST.svg/?label=active+issues&show_trend=true&token=Yrd2y9gG7y8h53JsDwyjQdFZ)](https://deepsource.io/gh/sisoe24/Nuke-Tools-ST/?ref=repository-badge)

> This is a companion extension for: [NukeServerSocket](#nukeserversocket) and is based on [NukeTools](https://marketplace.visualstudio.com/items?itemName=virgilsisoe.nuke-tools).

A Sublime Text package that allows to send python or blinkscript code to be executed inside Nuke.

## Features

* Execute code inside Nuke from a machine in your local network.
  * Get output of Nuke code execution inside Sublime console.
  * When used locally (same machine) no configuration is required, just running the server inside Nuke.
  * Specify a custom address when connection is from/to another computer.
  * Multiple connections can be made to the same Nuke instance.
  * BlinkScript support.

## Installation

> TODO: add section after it has been approved to Package Control.

## BlinkScript

> [NukeServerSocket](#nukeserversocket) >= 0.1.0 is needed in order for this to work.

You can execute code from the text editor directly inside a Nuke BlinkScript node.

The extension will take the name of the current active file and create a blinkscript node inside Nuke with the name as the current filename. If the node already exists then will only modified its source code. Once done will recompile the source kernel.

The accepted file extension are `.cpp` or `.blink`.

## Connection

No settings are necessary if connection is expected to be on the same computer.
NukeToolsST will automatically connect to the `localhost` and will use the port
configuration found inside _$HOME/.nuke/NukeServerSocket.ini_. The configuration value is updated automatically each time its changed inside the plugin.

However if connection is between different computers, port and hostname must be changed manually.

> Keep in mind that, once the addresses are specified manually, will always take over the defaults one. Its best to delete them if you want to just use it one the same computer.

### Note

Attempting to connect to a manually specified host that is down (not reachable)
will result in a temporary freeze of the Sublime UI for 10 seconds.

## Package Settings

### `nss_port`:`integer`

A different port for the connection. Port should match the one from NukeServerSocket.

### `nss_hostname`:`string`

Same as `nss_port`. Host could be the localhost or the local ip.

### `nss_disable_context_menu`:`bool`

Disable Sublime context menu entry if not needed (clean up). Defaults to `false`.

### Example

```json
{
  "nss_port": 54321,
  "nss_hostname": "192.168.1.60",
  "nss_disable_context_menu": true
}
```

## Commands

The following command will be available:

```json
{
    "caption":"Run Code inside Nuke",
    "command": "run_nuke_tools" 
}
```

The command can be invoked from the context menu (right click) when the active file ends with the following extension:

* `.py`
* `.cpp`
* `.blink`

## Key Bindings

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

## NukeServerSocket

Download the companion plugin: [Git](https://github.com/sisoe24/NukeServerSocket/releases), [Nukepedia](http://www.nukepedia.com/python/misc/nukeserversocket).

## Changelog

[0.1.0] 10-21-2021

* Initial release.
