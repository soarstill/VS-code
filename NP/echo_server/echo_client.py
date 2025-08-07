from socket import *
import time

BUFFSIZE = 1024

class EchoClient:
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.address = (self.host, self.port)
        self.socket.connect(self.address)
        print(f"Connected to Echo server at {self.address}")

    def __del__(self):
       self.close()

    def send_message(self, message):
        self.socket.sendall(message.encode())
        print(f"Sent message to server: {message}")

    def receive_response(self):
        response = self.socket.recv(BUFFSIZE)
        print(f"Received response from server: {response.decode()}")
        return response.decode()
    
    def is_connected(self):
        try:
            self.socket.send(b'')
            return True
        except (BrokenPipeError, OSError):
            return False
        
    def close(self):
        if not self.socket == None:
            self.socket.close()
            self.socket = None
        print("Connection closed.")


import unittest
class TestEchoClient(unittest.TestCase):
    def setUp(self):
        self.client = EchoClient()
        if not self.client.is_connected():
            self.client = None
            print("Failed to connect to Echo server.")
        else:
            print("Echo client initialized and connected.")

    def test_send_receive(self):
        for i in range(5):
            test_message = f"{i}: Test message"
            self.client.send_message(test_message)
            echo_message = self.client.receive_response()
            self.assertEqual(test_message, echo_message)    
            time.sleep(1)  # Wait for 1 second before the next iteration

    def tearDown(self):
        if not self.client == None:  
            self.client.close()
        print("TestEchoClient completed and client closed.")
        self.assertIsNone(self.client.socket, "Socket should be None after closing")

        
if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        print("Echo UDP client is down.")
    finally:
        pass

