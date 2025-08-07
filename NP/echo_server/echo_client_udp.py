from socket import *
import time
import unittest

BUFFSIZE = 1024

class EchoClientUDP:
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.address = (self.host, self.port)
        print(f"Connected to Echo server (UDP) at {self.address}")

    def __del__(self):
        self.close()

    def send_request(self, message):
        self.socket.sendto(message.encode(), self.address)
        print(f"Sent message to server: {message}")

    def receive_response(self):
        response, _ = self.socket.recvfrom(BUFFSIZE)
        print(f"Received response from server: {response.decode()}")
        return response.decode()
    
    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
        print("Connection closed.")

class TestEchoClientUDP(unittest.TestCase):
    def setUp(self):
        self.client = EchoClientUDP()
        print("Echo UDP client initialized.")

    def test_send_receive(self):
        for i in range(5):
            test_message = f"{i}: Test message"
            self.client.send_request(test_message)
            echo_message = self.client.receive_response()
            self.assertEqual(test_message, echo_message)
            time.sleep(1)

    def tearDown(self):
        if self.client is not None:
            self.client.close()
        print("Test completed and client closed.")
        self.assertIsNone(self.client.socket, "Socket should be None after closing")

if __name__ == "__main__":
    unittest.main()
