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
    data = nuke_tools.send_data(LOCALHOST, FREE_PORT, 'hello')
    assert 'ConnectionRefusedError' in data
