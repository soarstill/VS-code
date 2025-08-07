
import socket
import time

class TimeServer:
    def __init__(self, host='', port=5000, backlog=5):
        self.address = (host, port)
        self.backlog = backlog
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind(self.address)
        self.__sock.listen(self.backlog)

    def __del__(self):
        print("서버 소켓이 닫힙니다.")
        self.__sock.close()
        print("서버 소켓이 닫혔습니다.")

    def handle_client(self, client_socket):
        client_socket.settimeout(10)  # 클라이언트 소켓에 타임아웃 설정
        try:
            while True:
                message = client_socket.recv(1024)  # 클라이언트로부터 데이터를 받음
                if message == b'GET TIME':
                    print("클라이언트로부터 'GET TIME' 요청을 받았습니다.")
                else:
                    print("알 수 없는 요청을 받았습니다.")
                    return
                current_time = time.ctime()
                client_socket.sendall(current_time.encode())
        
        except socket.timeout:
            print("클라이언트 연결이 타임아웃되었습니다.")
        
        finally:
            print("클라이언트와의 연결을 종료합니다.")
            return
                

    def serve_forever(self):
        print(f"Time server is running on {self.address}...")
        while True:
            client_socket, addr = self.__sock.accept()

            print(f"Connection from {addr} has been established.")

            self.handle_client(client_socket)
            client_socket.close()
            print(f"Connection from {addr} has been closed.")


if __name__ == "__main__":
    server = TimeServer()
    server.serve_forever()

