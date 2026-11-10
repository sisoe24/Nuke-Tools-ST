"""Send code from Sublime Text to Nuke to be executed over the tcp network."""

import os
import json
import socket

from datetime import datetime

NSS_CONFIG = os.path.join(
    os.path.expanduser('~'), '.nuke', 'nukeserversocket.json'
)


def format_output(text):
    """Format output to send at console.

    Example: `[17:49:25] [NukeTools] Hello World`

    Args:
        text (str): str to be formatted.

    Returns:
        str: formatted string.
    """
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    return "[{}] [NukeTools] {}".format(time, text)


def nss_ip_port():
    """Get NukeServerSocket ip port from configuration file.

    Get the ip port from nukeserversocket.json inside the `$HOME/.nuke/`
    folder. If file does not yet exists, is malformed, or the configuration
    value is absent or invalid, will return a default value of: `54321`, that
    is also the default value of NukeServerSocket.

    Returns:
        int: tcp port value to connect the socket client.
    """
    try:
        with open(NSS_CONFIG, encoding='utf-8') as file:
            return int(json.load(file)['port'])
    except (OSError, ValueError, KeyError, TypeError):
        # file is missing, malformed, or has no valid port value
        return 54321


def prepare_data(data, file=''):
    """Prepare the data to be send over the network.

    Data should be wrapped inside a stringified array with the key `text` with
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


def _err_msg(err, hostname, port):
    """Generate template error message.

    Generate a template error message with the hostname and the port:
    `ConnectionError. 192.168.1.50:55555`.

    Args:
        err (str): Error message to add.
        hostname (str): hostname.
        port (str|int): port.

    Returns:
       str: the error message created.
    """
    err = (
        "{}. {}:{}.\n".format(err, hostname, port)
        + 'Check Sublime settings if you specified manually the address,'
        ' or check if plugin inside Nuke is connected.'
    )
    return err


def send_data(hostname, port, data, timeout=10.0):
    """Send data over tcp network.

    Send some text data via TCP connection to the host and port specified. Once
    the output is ready, will be returned as a string.

    Args:
        hostname (str): The name of the host.
        port (int): The port number.
        data (data): The data to send.
        timeout (float): Timeout for the connection only, not for the reply.
            Defaults to: 10.0.

    Returns:
        str: If socket succeeded will return the received data, otherwise a
        status message signaling what went wrong.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:

        # set a connection timeout in case host is down.
        _socket.settimeout(timeout)

        try:
            # connection host and port must match whats inside Nuke
            _socket.connect((hostname, port))

            # no limit on the reply: Nuke code can run for any length of time.
            _socket.settimeout(None)
            _socket.sendall(bytearray(data, encoding='utf-8'))

            # NukeServerSocket closes the connection after the reply: read until then.
            output = b''.join(iter(lambda: _socket.recv(4096), b'')).decode('utf-8')
        except ConnectionRefusedError:
            output = _err_msg("ConnectionRefusedError", hostname, port)
        except socket.timeout:
            output = _err_msg("ConnectionTimeoutError", hostname, port)
        except socket.error as err:
            output = _err_msg("UnknownError: {}".format(err), hostname, port)
        except Exception as err:
            output = "UnknownException: {}".format(err)

        return format_output(output)
