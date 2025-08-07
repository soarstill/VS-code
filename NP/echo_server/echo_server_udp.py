from socket import *

port = 5001
BUFFSIZE = 1024

class EchoServerUDP:
    def __init__(self, host='', port=5001):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.address = (self.host, self.port)
        self.socket.bind(self.address)
        print(f"Echo UDP server waiting for clients on port {self.port}...")

    def __del__(self):
        if self.socket is not None:
            self.socket.close()
        print("Echo UDP server socket closed.")

    def handle_client(self):
        while True:
            data, client_addr = self.socket.recvfrom(BUFFSIZE)
            if not data:
                print("No data received. Skipping.")
                continue
            print(f"Received data from {client_addr}: {data.decode()}")
            # Echo the data back to the client
            self.socket.sendto(data, client_addr)
            print(f"Sent data back to client: {data.decode()}")

    def start(self):
        print("UDP Echo server started.")
        try:
            self.handle_client()
        except Exception as e:
            print(f"Error occurred while handling client: {e}")
        finally:
            self.socket.close()
            print("UDP Echo server socket closed.")

if __name__ == "__main__":
    server = EchoServerUDP()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Echo UDP server is shutting down.")
    finally:
        del server
