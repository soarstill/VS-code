#include <iostream>
#include <string>
#include <thread>
#include <cstring>

#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "ws2_32.lib")
#else
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
#endif

class TimeClient {
private:
#ifdef _WIN32
    SOCKET sock;
#else
    int sock;
#endif
public:
    TimeClient(const char* host, int port) {
#ifdef _WIN32
        WSADATA wsaData;
        WSAStartup(MAKEWORD(2,2), &wsaData);
#endif
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (
#ifdef _WIN32
            sock == INVALID_SOCKET
#else
            sock < 0
#endif
        ) {
            std::cerr << "소켓 생성 실패\n";
            exit(1);
        }

        sockaddr_in serverAddr = {};
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(port);
        inet_pton(AF_INET, host, &serverAddr.sin_addr);

        if (connect(sock, (sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
            std::cerr << "서버 연결 실패\n";
#ifdef _WIN32
            closesocket(sock);
            WSACleanup();
#else
            close(sock);
#endif
            exit(1);
        }
        std::cout << "서버에 연결되었습니다.\n";
    }

    void getTime() {
        const char* msg = "GET TIME";
        send(sock, msg, strlen(msg), 0);

        char buffer[1024] = {0};
        int bytes = recv(sock, buffer, sizeof(buffer)-1, 0);
        if (bytes <= 0) {
            std::cout << "서버로부터 응답을 받지 못했습니다.\n";
            return;
        }
        buffer[bytes] = '\0';
        std::cout << "현재시각: " << buffer << std::endl;
    }

    void close() {
#ifdef _WIN32
        closesocket(sock);
        WSACleanup();
#else
        close(sock);
#endif
        std::cout << "클라이언트 소켓이 닫힙니다.\n";
    }
};

int main() {
    TimeClient client("127.0.0.1", 5000);
    for (int i = 0; i < 5; ++i) {
        client.getTime();
        std::this_thread::sleep_for(std::chrono::seconds(3));
    }
    client.close();
    return 0;
}