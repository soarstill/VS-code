import socket
import time
import unittest


class TimeClient:
    def __init__(self, host='localhost', port=5000):
        self.address = (host, port)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect(self.address)  
    def __del__(self):
        print("클라이언트 소켓이 닫힙니다.")
        self.__sock.close()

    def get_time(self):
        self.__sock.sendall(b'GET TIME')
        current_time = self.__sock.recv(1024)
        if not current_time:
            print("서버로부터 응답을 받지 못했습니다.")
            return
        print("현재시각: ", current_time.decode())


class TestTimeClient(unittest.TestCase):
    def test_get_time(self):
        client = TimeClient()
        for i in range(5):
            client.get_time()
            time.sleep(3)
            
        self.assertIsNotNone(client.__sock, "Socket should not be None after connection")
        client.__del__()