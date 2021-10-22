"""Test tcp connection.

Connection will happen on localhost and at a random free port.
"""
import socket
import threading
import socketserver

import pytest

from src import nuke_tools

LOCALHOST = '127.0.0.1'

with socketserver.TCPServer((LOCALHOST, 0), None) as s:
    FREE_PORT = s.server_address[1]


def socket_server():
    """Create a Server that listen for incoming requests."""
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    _socket.bind((LOCALHOST, FREE_PORT))

    _socket.listen(1)

    while True:
        conn, _ = _socket.accept()

        try:
            data = conn.recv(2048)
            conn.sendall(data)
            break

        except Exception:
            break

    _socket.close()
    conn.close()


@pytest.fixture()
def tcp_server():
    """Start the tcp server in a thread to allow async operation."""
    server = threading.Thread(target=socket_server)
    server.daemon = True
    server.start()
    yield server
    server.join()


def test_send_data(tcp_server):
    """Test that send data method returns expected value."""
    data = nuke_tools.send_data(LOCALHOST, FREE_PORT, 'hello')

    assert isinstance(data, str)
    assert '[NukeTools] hello' in data


def test_connection_refused():
    """Test sending data when server is not listening."""
    data = nuke_tools.send_data(LOCALHOST, FREE_PORT, 'hello', 0.1)
    assert f'ConnectionRefusedError. {LOCALHOST}:{FREE_PORT}' in data


def test_connection_timeout():
    """Test connection timeout."""
    hostname = '192.168.1.99'
    data = nuke_tools.send_data('192.168.1.99', FREE_PORT, 'hello', 0.1)
    assert f'ConnectionTimeoutError. {hostname}:{FREE_PORT}' in data


def test_connection_socket_error():
    """Test connection base exception.

    Wrong hostname and port to force socket error.
    """
    data = nuke_tools.send_data('111.111.1.11', 0, 'hello', 0.1)
    assert 'UnknownError:' in data


def test_connection_generic_exception():
    """Test connection base exception.

    Convert port to string to force exception.
    """
    data = nuke_tools.send_data(LOCALHOST, str(FREE_PORT), 'hello', 0.1)
    assert 'UnknownException:' in data
