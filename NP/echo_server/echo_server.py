from socket import *

port = 5001
BUFFSIZE = 1024

class EchoServer:
    def __init__(self, host='', port=5001):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.address = (self.host, self.port)
        self.socket.bind(self.address)
        self.socket.listen(1)
        print(f"Echo server waiting for clients on port {self.port}...")

    def __del__(self):
        if not self.socket == None:
            self.socket.close()
        print("Echo server socket closed.")

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(BUFFSIZE)
            if not data:
                print("No data received. Closing connection.")
                break
            print(f"Received data: {data.decode()}")

            # Echo the data back to the client
            client_socket.sendall(data)
            print(f"Sent data back to client: {data.decode()}")

    def start(self):
        while True:
            print("Waiting for a client to connect...")
            client_socket, addr = self.socket.accept()
            print(f"Connection from {addr[0]} on port {addr[1]} has been established.")
            try:
                self.handle_client(client_socket)
            except Exception as e:
                print(f"Error occurred while handling client: {e}")
            finally:
#                client_socket.close()
                pass

if __name__ == "__main__":
    server = EchoServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Echo server is shutting down.")
    finally:
        del server