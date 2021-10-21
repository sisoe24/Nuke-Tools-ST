"""Send code from Sublime Text to Nuke to be executed over the tcp network."""

import os
import json
import socket
import logging
import configparser

NSS_CONFIG = os.path.join(
    os.path.expanduser('~'), '.nuke', 'NukeServerSocket.ini'
)


def nss_ip_port():
    """Get NukeServerSocket ip port from configuration file.

    Get the ip port from NukeServerSocket.ini inside the `$HOME/.nuke/` folder.
    If file does not yet exists or the configuration value is absent, will
    return a default value of: `54321`, that is also the default value of
    NukeServerSocket.

    Returns:
        int: tcp port value to connect the socket client.
    """
    try:
        config = configparser.ConfigParser()
        config.read(NSS_CONFIG)
        return int(config['server']['port'])
    except KeyError:
        # file doesn't exists yet or value is absent
        return 54321


def prepare_data(data, file=''):
    """Prepare the data to be send over the network.

    Data should be wrappend inside a stringified array with the key `text` with
    the code to execute and an optional key `file` for the file that is being
    executed.

    Args:
        data (str): The data to send.
        file (str): Optional. The file that is being executed.

    Returns:
        str: stringified array.
    """
    data = {"text": data, "file": file}
    return json.dumps(data)


def send_data(hostname, port, data):
    """Send data over tcp network.

    Send the current active file text via TCP to the host and port specified by
    user. If no settings are found then will fallback on the default which will
    be the localhost and the port from NukeServerSocket.ini.

    Once the output is ready, will be returned as a string.

    Returns:
        str: the returned data from the socket.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:

        # connection host and port must match whats inside Nuke
        try:
            _socket.connect((hostname, port))
        except ConnectionRefusedError:
            logging.warning(
                '[NukeToolsST] Connection refused. '
                'Check Sublime settings if you specified manually the address,'
                ' or check if plugin inside Nuke is connected.')

            # TODO: should raise Error? its to verbose and doesn't really help
            return 'ConnectionRefusedError'

        _socket.sendall(bytearray(data, encoding='utf-8'))

        # the returned data from NukeServerSocket
        data = _socket.recv(2048)

        return data.decode('utf-8')
